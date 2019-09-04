import pickle
import requests
import json
import os

from cryptography.fernet import Fernet
from shutil import copyfileobj
from bs4 import BeautifulSoup
from datetime import datetime
# Simple dict with user name : user id
from iZettleUsers import *

def savePDF(session,user,uId,report_date):
    url = "https://my.izettle.com/reports.pdf?user=" + uId +"&aggregation=day&date=" + report_date +"&type=pdf"
    r = session.get(url, verify=False,stream=True)
    r.raw.decode_content = True
    fileLocation = "/" + user + "/" + report_date.split('-')[0]
    current_directory = "G:\Delade enheter\Ekonomi\iZettle Rapporter"
    final_directory = current_directory + fileLocation
    if not os.path.exists(final_directory):
       os.makedirs(final_directory)

    fileName = user + "_" + report_date
    with open(final_directory+"/"+fileName+".pdf", 'wb') as f:
            copyfileobj(r.raw, f)
            print('Created: ' + fileName+".pdf")


def getUserReportList(session,uId):
    r2 = session.get('https://my.izettle.com/reports/summary?user=' + uId).json()
    results = r2["daily"]
    reports = set()
    for month in results:
        results_month = results[month]
        i = 0
        for _ in results_month:
            report_date_string = results_month[i]['aggregateStart'].split('T')[0] #prints the raw html you can now parse and scrape
            
            i = i + 1
            reports.add(report_date_string)
    return reports

def saveUserDateMap(UserDateMap):
    with open("dates.pickle","wb") as handle:
        pickle.dump(UserDateMap, handle)

def loadUserDateMap():
    file =  open('dates.pickle', 'rb') 
    return pickle.load(file)

def main():
    # Has to be included to show that 'we are not a bot', which well we are
    headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
            }
    url = 'https://login.izettle.com/login?username=ekonomi.ztyret%40ztek.se'
    file =  open('key', 'rb') 
    key = pickle.load(file)
    file =  open('pass', 'rb') 
    token = pickle.load(file)
    f = Fernet(key)
    login_data = {
        'username': 'ekonomi.ztyret@ztek.se',
        'password': f.decrypt(token).decode("utf-8"),
        'button':''
    }
    # All the reports sorted per user
    UserDateMap = loadUserDateMap()
    with requests.Session() as s:
        r = s.get(url, headers=headers)
        # When we need to log in we need to get the new form id, which is unique
        # for each session for iZettle '_csrf' is this id
        soup = BeautifulSoup(r.content,'html5lib')
        login_data['_csrf'] = soup.find('input', attrs={'name':'_csrf'})['value']
        s.post(url,data=login_data,headers=headers)
        for user in users:
            uId = users[user]
            reports = getUserReportList(s,uId)
            old_reports = UserDateMap[user]
            
            new_reports = reports.difference(old_reports)
            for report_to_add in new_reports:
                savePDF(s,user,uId,report_to_add)
                UserDateMap[user].add(report_to_add)
        saveUserDateMap(UserDateMap)
    print('Done')

if __name__ == '__main__':
    main()
            

