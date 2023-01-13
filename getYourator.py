import requests
from dbHandler import DBHandler
import datetime

DOMAIN = 'https://www.yourator.co'
url = 'https://www.yourator.co/api/v2/jobs?term[]=python&sort=recent_updated&page={}'

page = 1
all_job = []

while True:
    try:
        response = requests.get(url.format(page)).json()
    except requests.JSONDecodeError as e:
        print(e)
        break
    except:
        print('異常錯誤')
        break
    else:
        data_list = response['jobs']
        if not data_list:
            break
        else:
            for row in data_list:
                all_job.append({
                    'job_link': f"{DOMAIN}{row['path']}",
                    'job_name': row['name'],
                    'job_addr': row['city'],
                    'company_name': row['company']['brand'],
                    'salary': row['salary'],
                    'education': '請至連結頁面查詢',
                    'work_experience': '請至連結頁面查詢',
                    'web_id': 2,
                    'update_time': datetime.datetime.now()
                })
    page += 1
    

dbHandler = DBHandler()
dbHandler.write(all_job)
dbHandler.close()
