import requests
import re
import datetime
import calendar
import sys
import json
from flask import request, jsonify
from DefaultInfo import *
from datetime import date, timedelta

URL = URL_SCHOOL_MEAL_SERVICE_INFO

quick = [
            {
                "action": "message",
                "label": "월요일",
                "messageText": "월요일"
            },
            {
                "action": "message",
                "label": "화요일",
                "messageText": "화요일"
            },
            {
                "action": "message",
                "label": "수요일",
                "messageText": "수요일"
            },
            {
                "action": "message",
                "label": "목요일",
                "messageText": "목요일"
            },
            {
                "action": "message",
                "label": "금요일",
                "messageText": "금요일"
            },            
        ]

def SchoolMealServiceInfo():
    requestURL = URL + KEY_IDF + AUTHORIZATION_KEY_NEIS + AND + GET_TYPE + AND + EDUCATION_OFFICE_CODE + AND + SCHOOL_CODE + AND
    weekly = {0:"월", 1:"화", 2:"수", 3:"목", 4:"금", 5:"토", 6:"일"}
    args  = ""
    req = request.get_json() 
    
    if bool('sys_date_period' in req['action']['detailParams']) == True:    
        loadedJson =  json.loads(req['action']['detailParams']['sys_date_period']['value'])
        fromDate = str(loadedJson['from']['date'])
        toDate = str(loadedJson['to']['date'])
        fromList = fromDate.split('-')
        toList = toDate.split('-')
        fromDate = fromList[0] + fromList[1] + fromList[2]
        toDate = toList[0] + toList[1] + toList[2]
        requestParameter_FROM = "MLSV_FROM_YMD=" + fromDate
        requestParameter_TO = "MLSV_TO_YMD=" + toDate
        args = requestURL + AND + requestParameter_FROM + AND + requestParameter_TO

    elif bool('sys_date' in req['action']['detailParams']) == True:
        loadedJson =  json.loads(req['action']['detailParams']['sys_date']['value'])
        print(str(loadedJson), file=sys.stderr)
        targetDate = str(loadedJson['date'])

        if 'None' == targetDate:
            Error = {
                "version": "2.0",
                "data": {
                    'OnlineClass_Info': "입력이 잘못되었습니다."
                }
            }
            return jsonify(Error) 

        targetList = targetDate.split('-')
        targetDate = targetList[0] + targetList[1] + targetList[2]
        requestParameter_DATE = "MLSV_YMD=" + targetDate
        args = requestURL + AND + requestParameter_DATE
    else:
        Error = {
            "version": "2.0",
            "data": {
                'Meal_Info': "입력이 잘못되었습니다."
            }
        }
        return jsonify(Error)               

    errorRet ={}
    if IsCanRequest(args, errorRet) == False:
        Error = {
            "version": "2.0",
            "data": {
                'Meal_Info': errorRet
            }
        }
        return jsonify(Error)

    req = requests.get(args)
    reqJson = req.json()
    if str(reqJson).find("INFO-200") != -1:   
        CantFind = {
            "version": "2.0",
            "data": {
                'Meal_Info': "해당하는 데이터가 없습니다."
            }
        }
        return jsonify(CantFind)    
    text = ""
    print(str(reqJson), file=sys.stderr)

    i = 0
    max = len(reqJson['mealServiceDietInfo'][1]['row'])
    for j in range(len(reqJson['mealServiceDietInfo'][1]['row'])):
        date = str(reqJson['mealServiceDietInfo'][1]['row'][j]['MLSV_YMD'])
        yearValue = str(date[:4])
        monthValue = str(date[4:6]).lstrip("0")
        dayValue = str(date[6:]).lstrip("0")

        weekday = datetime.date(int(yearValue), int(monthValue), int(dayValue)).weekday()
        add = ""
        if(i == max - 1):
            add = ""
        else:
            add = "<br/><br/>"
        tempText = str(reqJson['mealServiceDietInfo'][1]['row'][j]['DDISH_NM']) + add
        tempText = re.sub("[0-9.:\",]","", tempText)
        tempDate = str(monthValue).zfill(2) + "월" + " " + str(dayValue).zfill(2) + "일" + " " + "(" + weekly[weekday] + ")" + "\n-"
        text = text + tempDate + tempText
        i = i + 1
    text = re.sub("[.:\",]","", text)
    text = text.replace("<br/><br/>", "$$$$")
    text = text.replace("<br/>", "\n-")
    text = text.replace("$$$$", "\n\n")
    text = text.replace("(중)", "")
    print(str(text), file=sys.stderr)
 
    responseData = {
        "version": "2.0",
        "data": {
            'Meal_Info': text
        }
    }
    return jsonify(responseData)






