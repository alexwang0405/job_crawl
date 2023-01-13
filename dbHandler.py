import psycopg2
from dotenv import dotenv_values


config = dotenv_values('.env')


class DBHandler:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=config['HOST'], 
            port=config['PORT'], 
            database=config['DATABASE'], 
            user=config['USER'], 
            password=config['PASSWORD']
        )
        self.cursor = self.conn.cursor()
    
    def write(self, data: list):
        for row in data:
            if 'job_link' not in row:
                raise Exception('無職缺連結')
            elif 'job_name' not in row:
                raise Exception('無職缺名稱')
            elif 'job_addr' not in row:
                raise Exception('無職缺地址')
            elif 'company_name' not in row:
                raise Exception('無公司名稱')
            elif 'salary' not in row:
                raise Exception('無薪資')
            elif 'education' not in row:
                raise Exception('無學歷')
            elif 'work_experience' not in row:
                raise Exception('無經歷')

            if self.is_duplicated(row['job_name'], row['company_name'], row['web_id']):
                print('資料重複')
                continue

            sql = f"""
            insert into {config['TABLE_NAME']} (job_link, job_name, job_addr, company_name, salary, education, work_experience, web_id, update_time)
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            self.cursor.execute(sql, (
                row['job_link'], 
                row['job_name'], 
                row['job_addr'], 
                row['company_name'], 
                row['salary'], 
                row['education'], 
                row['work_experience'],
                row['web_id'],
                row['update_time'],
            ))
            self.conn.commit()
            print('success')
        return 'finish'

    def is_duplicated(self, job_name, company_name, web_id):
        sql = f"select * from {config['TABLE_NAME']} where job_name=%s and company_name=%s and web_id=%s"
        self.cursor.execute(sql, (job_name, company_name, web_id))
        return self.cursor.rowcount != 0

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    import datetime

    dbHandler = DBHandler()

    print(dbHandler.write([{
        'job_link': 'https://www.104.com.tw/job/6l6c7?jobsource=hotjob_chr', 
        'job_name': 'Integration manager [串接專案管理師]', 
        'job_addr': '台北市大安區復興南路一段', 
        'company_name': '藍窗科技有限公司', 
        'salary': '待遇面議',
        'education': '專科',
        'work_experience': '1年以上',
        'web_id': 1,
        'update_time': datetime.datetime.now()
    }]))

    dbHandler.close()
    
