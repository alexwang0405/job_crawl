import requests
from dbHandler import DBHandler
import datetime

url = 'https://www.104.com.tw/jobs/search/list?ro=0&isnew=0&kwop=7&keyword=python&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=15&asc=0&page={}&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'

header = {
    'Referer': 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword=python&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=15&asc=0&page=1&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

page = 1
all_job = []

while True:
    try:
        response = requests.get(url.format(page), headers=header).json()
    except requests.JSONDecodeError as e:
        print(e)
        break
    except:
        print('異常錯誤')
        break
    else:
        data_list = response['data']['list']
        if not data_list:
            break
        else:
            for row in data_list:
                
                link = row['link']['job']
                if link[0] == '/':
                    link = f"https:{row['link']['job']}"

                all_job.append({
                    'job_link': link,
                    'job_name': row['jobName'],
                    'job_addr': f"{row['jobAddrNoDesc']}{row['jobAddress']}",
                    'company_name': row['custName'],
                    'salary': row['salaryDesc'],
                    'education': row['optionEdu'],
                    'work_experience': row['periodDesc'],
                    'web_id': 1,
                    'update_time': datetime.datetime.now(),
                })
    page += 1
    

dbHandler = DBHandler()
dbHandler.write(all_job)
dbHandler.close()
