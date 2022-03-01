from datetime import date
from dotenv import load_dotenv
import urllib3, json, os, calendar

load_dotenv()

hosts = ['codeforces.com', 'codechef.com', 'atcoder.jp']
BASE_URL = 'https://clist.by/api/v2/contest/?format_time=true&upcoming=true&order_by=-start&host='
API_KEY = os.getenv('API_KEY')

results = []
fResults = []
http = urllib3.PoolManager()


def checkUpcomingContest(contests):
  day = calendar.day_name[date.today().weekday()]
  # print(startDate[0:10], date)
  for contest in contests:
    startDate = contest['start']
    if startDate[6:9] == day[0:3] and startDate[0:2] == str(date.today())[-2:]:
      results.append(contest)

def formatMessage(data):
  msg = f"Upcoming Contest{'s' if len(fResults) > 1 else ''} Today \n\n"
  count = 1
  for fResult in fResults:
    fMsg = f"*{count}. {fResult['Contest Name']}* \nStart Time : {fResult['Start Time']} \nEnd Time : {fResult['End Time']} \n=> : {fResult['URL']} \n\n"
    msg = msg + fMsg
    count += 1
  if len(fResults) == 0:
    msg = 'No Contests Today!'
  return msg

def sendTelegramMessage(data):
  BASE_URL = 'https://api.telegram.org/bot5129277495:AAERHNBWUe_YiWU2j5gzP8sn9Jyj9COAJJc/sendMessage?chat_id=608641856&text='
  DATA = data
  FINAL_URL = BASE_URL+data
  http.request('GET', FINAL_URL+'&parse_mode=markdown')

def startBot():
  for host in hosts:
    URL = BASE_URL + host + API_KEY
    data = http.request('GET', URL).data.decode('utf8')
    data = json.loads(data)
    print(data)
    checkUpcomingContest(data['objects'])
  for result in results:
    fData = {
      "Contest Name" : result['event'],
      "Contest Site" : result['host'],
      "Start Time" : result['start'][-5:],
      "End Time" : result['end'][-5:],
      "URL" : result['href']
    }
    fResults.append(fData)
  finalMsg = formatMessage(fResults)
  sendTelegramMessage(finalMsg)

startBot()