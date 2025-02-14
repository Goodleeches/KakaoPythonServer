import requests
from flask import jsonify
from requests.models import Response
# open Port
OPEN_PORT                       = 9900
#"7010093"	  #7091427
# 시도교육청코드
EDUCATION_OFFICE_CODE           =   "ATPT_OFCDC_SC_CODE=" + "B10" 	     
# 표준학교코드
SCHOOL_CODE                     =   "SD_SCHUL_CODE=" + "7091427" 
# keyIdentifier
GET_TYPE                        =   "Type=" + "json"
KEY_IDF                         =   "?KEY="
AND                             =   "&"
# Neis Authorization Key
AUTHORIZATION_KEY_NEIS          =   "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# URL
URL_MIS_SCHOOL_TIMETABLE_INFO   =   "https://open.neis.go.kr/hub/misTimetable"
URL_SCHOOL_MEAL_SERVICE_INFO    =   "https://open.neis.go.kr/hub/mealServiceDietInfo"
URL_SCHOOL_SCHEDULE_INFO        =   "https://open.neis.go.kr/hub/SchoolSchedule"
URL_HIS_SCHOOL_TIMETABLE_INFO   =   "https://open.neis.go.kr/hub/hisTimetable"
URL_SCHOOL_INFO                 =   "https://open.neis.go.kr/hub/schoolInfo"

#print("", file=sys.stderr)
# http://125.129.247.69:9900/ 

#Database
DB_HOST                         =   'localhost'
DB_USER                         =   'root'
DB_PASSWORD                     =   'root'
DB_NAME                         =   'kakaodb'
DB_CHARSET                      =   'utf8'

#ExcelDataPath
PATH = "C:/Users/me/Desktop/KakaoPythonServer/excelData/"


def IsCanRequest(url, dict):
    
    try: 
        requests.get(url)   
    except requests.exceptions.Timeout as errd:
        print("Timeout Error : ", errd)
        error ="Timeout Error : " + str(errd)
        if str(url).find("open.neis.go.kr") != -1:
            error += "\n" + "[나이스 OpenAPI 시스템 점검]\n\n보다 안정적인 서비스 이용을 위해 점검 중입니다. 서비스 이용에 불편을 드려 죄송합니다.\n" + "https://open.neis.go.kr"
        
        dict = {"version": "2.0", "template": { "outputs": [{"simpleText" : { "text": error}}]}}
        return False           
        
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting : ", errc)
        error ="Error Connecting : " + str(errc)
        if str(url).find("open.neis.go.kr") != -1:
            error += "\n" + "[나이스 OpenAPI 시스템 점검]\n\n보다 안정적인 서비스 이용을 위해 점검 중입니다. 서비스 이용에 불편을 드려 죄송합니다.\n" + "https://open.neis.go.kr"
 
        dict = {"version": "2.0", "template": { "outputs": [{"simpleText" : { "text": error}}]}}
        return False           
        
    except requests.exceptions.HTTPError as errb:
        print("Http Error : ", errb)
        error ="Http Error : " + str(errb)
        if str(url).find("open.neis.go.kr") != -1:
            error += "\n" + "[나이스 OpenAPI 시스템 점검]\n\n보다 안정적인 서비스 이용을 위해 점검 중입니다. 서비스 이용에 불편을 드려 죄송합니다.\n" + "https://open.neis.go.kr"
         
        dict = {"version": "2.0", "template": { "outputs": [{"simpleText" : { "text": error}}]}}
        return False  

    # Any Error except upper exception
    except requests.exceptions.RequestException as erra:
        print("AnyException : ", erra)   
        error ="AnyException : " + str(erra)
        if str(url).find("open.neis.go.kr") != -1:
            error += "\n" + "[나이스 OpenAPI 시스템 점검]\n\n보다 안정적인 서비스 이용을 위해 점검 중입니다. 서비스 이용에 불편을 드려 죄송합니다.\n" + "https://open.neis.go.kr"
         
        dict = {"version": "2.0", "template": { "outputs": [{"simpleText" : { "text": error}}]}}
        return False

    return True
    
