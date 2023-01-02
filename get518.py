import requests
import re
from dbHandler import DBHandler


url = 'https://www.518.com.tw/job-index.html?ad=python&al=2'

response = requests.get(url)
# print(response.text)
response_text = response.text.replace('\n', '')
job_list = re.findall(r'<ul class="all_job_hover" .*?</ul>', response_text)

all_job = []

if len(job_list) == 0:
    raise Exception('今日無更新')
else:
    for row in job_list:
        link = re.findall(r'<a .*? href="(https://www\.518\.com\.tw/job-.*?\.html)">', row)[0]
        name = re.findall(r'<h2 .*?>(.*?)</h2>', row)[0]
        addr = re.findall(r'<li class="area">(.*?)</li>', row)[0]
        com_name = re.findall(r'<li class="company">.*?>(.*?)</a></li>', row)[0]
        salary = re.findall(r'<p class="jobdesc">(.*?)</p>', row)[0]
        education = re.findall(r'<li class="edu">(.*?)</li>', row)[0]
        education = education.split(' / ')[1]
        work_experience = re.findall(r'<li class="exp">(.*?)</li>', row)[0]

        # print(link)
        # print(name)
        # print(addr)
        # print(com_name)
        # print(salary)
        # print(education)
        # print(work_experience)
        # print('='*15)

        all_job.append({
            'job_link': link,
            'job_name': name,
            'job_addr': addr,
            'company_name': com_name,
            'salary': salary,
            'education': education,
            'work_experience': work_experience,
            'web_id': 3,
        })
        

dbHandler = DBHandler()
dbHandler.write(all_job)
dbHandler.close()
