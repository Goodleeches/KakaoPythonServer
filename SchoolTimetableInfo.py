import requests
import re
import datetime
import sys
from flask import request, jsonify
from DefaultInfo import *
from datetime import timedelta

URL = URL_MIS_SCHOOL_TIMETABLE_INFO

def SchoolTimetableInfo():
    requestURL = URL + KEY_IDF + AUTHORIZATION_KEY_NEIS + AND + GET_TYPE + AND + EDUCATION_OFFICE_CODE + AND + SCHOOL_CODE + AND
    print("requestURL: ", file=sys.stderr)
    print(str(requestURL), file=sys.stderr)

    weekly2 = {0:"월", 1:"화", 2:"수", 3:"목", 4:"금", 5:"토", 6:"일"}
    print("weekly2:", file=sys.stderr)
    print(str(weekly2), file=sys.stderr)

    dict = {
        'Timetable_Date_0' : '-',
        'Timetable_Date_1' : '-', 
        'Timetable_Date_2' : '-', 
        'Timetable_Date_3' : '-', 
        'Timetable_Date_4' : '-',
        'Timetable_Info_0' : '해당하는 데이터가 없습니다.',
        'Timetable_Info_1' : '해당하는 데이터가 없습니다.', 
        'Timetable_Info_2' : '해당하는 데이터가 없습니다.', 
        'Timetable_Info_3' : '해당하는 데이터가 없습니다.', 
        'Timetable_Info_4' : '해당하는 데이터가 없습니다.'        
        }
    print("dict: ", file=sys.stderr)
    print(str(dict), file=sys.stderr)

    args  = ""
    
    req = request.get_json() 
    print("req: ", file=sys.stderr)
    print(str(req), file=sys.stderr)
    if bool('grade' in req['action']['detailParams']) == True and bool('class' in req['action']['detailParams']) == True:   
        print("grade is not null: " + str('grade' in req['action']['detailParams']), file=sys.stderr)
        print("class is not null: " + str('class' in req['action']['detailParams']), file=sys.stderr) 
        Grade = req['action']['detailParams']['grade']['value']
        Class =  req['action']['detailParams']['class']['value']
        print("학년:" + str(Grade) + " " + "반:" + str(Class), file=sys.stderr)
        Grade = re.sub(r'[^0-9]', '', Grade)
        Class = re.sub(r'[^0-9]', '', Class)
        print(str(Grade) + str(Class), file=sys.stderr)
        weekly = {
            0:datetime.date(1,1,1), 
            1:datetime.date(1,1,1), 
            2:datetime.date(1,1,1), 
            3:datetime.date(1,1,1), 
            4:datetime.date(1,1,1), 
            5:datetime.date(1,1,1), 
            6:datetime.date(1,1,1)
        } 
        
        today = datetime.date.today()
        print("today: " + str(today), file=sys.stderr)
        weekly[today.weekday()] = today # if next + 7 timedelta

        for key, value in weekly.items():
            if value == datetime.date(1,1,1):
                offsetDay = key - today.weekday()
                weekly[key] = today + timedelta(days=offsetDay)
                print("weekly" + "[" + str(key) + "]" + "의 날짜: " + "today(" + str(today) + ") " + "timeDelta차이값(" + str(timedelta(days=offsetDay)) + ")", file=sys.stderr)

        targetDay_FROM  = datetime.date(weekly[0].year, weekly[0].month, weekly[0].day)
        print("targetDay_FROM(월요일): ", str(targetDay_FROM), file=sys.stderr)
        year_FROM       = str(targetDay_FROM.year)
        month_FROM      = str(targetDay_FROM.month).zfill(2)
        day_FROM        = str(targetDay_FROM.day).zfill(2)
        print("year_FROM: ", str(year_FROM), file=sys.stderr)
        print("month_FROM: ", str(month_FROM), file=sys.stderr)
        print("day_FROM: ", str(day_FROM), file=sys.stderr)

        targetDay_TO  = datetime.date(weekly[4].year, weekly[4].month, weekly[4].day)
        print("targetDay_FROM(금요일): ", str(targetDay_TO), file=sys.stderr)
        year_TO       = str(targetDay_TO.year)
        month_TO      = str(targetDay_TO.month).zfill(2)
        day_TO        = str(targetDay_TO.day).zfill(2)
        print("year_TO: ", str(year_TO), file=sys.stderr)
        print("month_TO: ", str(month_TO), file=sys.stderr)
        print("day_TO: ", str(day_TO), file=sys.stderr)        

        requestParameter_FROM   = "TI_FROM_YMD=" + year_FROM + month_FROM + day_FROM
        requestParameter_TO   = "TI_TO_YMD=" + year_TO + month_TO + day_TO        
        requestParameter_GRADE  = "GRADE=" + Grade
        requestParameter_CLASS  = "CLASS_NM=" + Class
        print("requestParameter_FROM(시작날짜): ", str(requestParameter_FROM), file=sys.stderr)
        print("requestParameter_TO(끝날짜): ", str(requestParameter_TO), file=sys.stderr)
        print("requestParameter_GRADE(학년): ", str(requestParameter_GRADE), file=sys.stderr)
        print("requestParameter_CLASS(반): ", str(requestParameter_CLASS), file=sys.stderr)

        args = requestURL + AND + requestParameter_GRADE + AND + requestParameter_CLASS + AND + requestParameter_FROM + AND + requestParameter_TO                 
        print("args: ", file=sys.stderr)
        print(str(args), file=sys.stderr)

        errorRet ={}
        if IsCanRequest(args, errorRet) == False:
            dict['Timetable_Info_0'] = errorRet
            dict['Timetable_Info_1'] = errorRet
            dict['Timetable_Info_2'] = errorRet
            dict['Timetable_Info_3'] = errorRet
            dict['Timetable_Info_4'] = errorRet
            Error = {
                "version": "2.0",
                "data": dict
            }
            return jsonify(Error)

        req = requests.get(args)
        reqJson = req.json()
        print("OpenApi에서 받은 수업 시간표 데이터:", file=sys.stderr)
        print(str(reqJson), file=sys.stderr)
        if str(reqJson).find("INFO-200") != -1:   
            CantFind = {
                "version": "2.0",
                "data": dict
            }
            return jsonify(CantFind)   

        i = 0
        for i in range(0, 5):
            targetDay  = datetime.date(weekly[i].year, weekly[i].month, weekly[i].day)
            year       = str(targetDay.year)
            month      = str(targetDay.month).zfill(2)
            day        = str(targetDay.day).zfill(2)
            weekday    = targetDay.weekday()

            if weekday == today.weekday():
                dict['Timetable_Date_' + str(i)] = month + "월" + " " + day  + "일" + " " + "(" + weekly2[weekday] + ")" + " " + "*오늘*"
            else:
                dict['Timetable_Date_' + str(i)] = month + "월" + " " + day  + "일" + " " + "(" + weekly2[weekday] + ")"
            print("Timetable_Date_" + str(i) + ": " + str(dict['Timetable_Date_' + str(i)]))

        text = ""
        i = 0
        max = len(reqJson['misTimetable'][1]['row'])
        for j in range(len(reqJson['misTimetable'][1]['row'])): 
                dateStr = str(reqJson['misTimetable'][1]['row'][j]['ALL_TI_YMD'])
                dateStr = re.sub(r'[^0-9]', '', dateStr)
                yearValue = str(dateStr[:4])
                monthValue = str(dateStr[4:6]).lstrip("0")
                dayValue = str(dateStr[6:]).lstrip("0")
    
                if yearValue == str(weekly[i].year) and monthValue == str(weekly[i].month) and dayValue == str(weekly[i].day):
                    text += str(reqJson['misTimetable'][1]['row'][j]['ITRT_CNTNT']) + '\n'                 
                else:
                    print(text, file=sys.stderr)   
                    dict['Timetable_Info_' + str(i)] = text[: - 1]    
                    i = i + 1
                    text = ""
                    text += str(reqJson['misTimetable'][1]['row'][j]['ITRT_CNTNT']) + '\n'       
                
                if j == max - 1:
                    print(text, file=sys.stderr)   
                    dict['Timetable_Info_' + str(i)] = text[: - 1]

        for k in range(0, 5):
            print("dict['Timetable_Info_" + "[" + str(k) + "]: " , file=sys.stderr)
            print(str(dict['Timetable_Info_' + str(k)]), file=sys.stderr)
    else:
        Error = {
            "version": "2.0",
            "data": dict
        }
        jsonify(Error)               

    responseData = {
        "version": "2.0",
        "data": dict       
    }
    return jsonify(responseData) 
