from flask import Flask, request, jsonify
from SchoolMealServiceInfo import SchoolMealServiceInfo
from SchoolScheduleInfo import SchoolScheduleInfo
from SchoolTimetableInfo import SchoolTimetableInfo
#from SchoolInfo import SchoolInfo
from SchoolExamInfo import SchoolExamInfo
#from HomeInfo import HomeInfo
#from SchoolMealServiceMenu import SchoolMealServiceMenu
#from SchoolTimetableMenu import SchoolTimetableMenu
from SchoolOnlineClass import SchoolOnlineClass
from DefaultInfo import *
import sys

app = Flask(__name__)

@app.route("/DeBug_Open")
def DeBug_Open():
    return "Server is Open"

@app.route("/SchoolMealServiceInfo", methods=['POST'])
def CallSchoolMealServiceInfo():
     return SchoolMealServiceInfo()

@app.route("/SchoolScheduleInfo", methods=['POST'])
def CallSchoolScheduleInfo(): 
     return SchoolScheduleInfo()

@app.route("/SchoolTimetableInfo", methods=['POST'])
def CallSchoolTimetableInfo(): 
     return SchoolTimetableInfo()

@app.route("/SchoolExamInfo", methods=['POST'])
def CallSchoolExamInfo():
     return SchoolExamInfo()

@app.route("/SchoolOnlineClass", methods=['POST'])
def CallSchoolOnlineClass():
     return SchoolOnlineClass()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=OPEN_PORT)

    