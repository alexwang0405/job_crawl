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

            if self.is_duplicated(row['job_name'], row['company_name']):
                print('資料重複')
                continue

            sql = f"""
            insert into {config['TABLE_NAME']} (job_link, job_name, job_addr, company_name, salary, education, work_experience)
            values (%s, %s, %s, %s, %s, %s, %s)
            """

            self.cursor.execute(sql, (
                row['job_link'], 
                row['job_name'], 
                row['job_addr'], 
                row['company_name'], 
                row['salary'], 
                row['education'], 
                row['work_experience']
            ))
            self.conn.commit()
            print('success')
        return 'finish'

    def is_duplicated(self, job_name, company_name):
        sql = f"select * from {config['TABLE_NAME']} where job_name=%s and company_name=%s"
        self.cursor.execute(sql, (job_name, company_name))
        return self.cursor.rowcount != 0

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':

    dbHandler = DBHandler()

    print(dbHandler.write([{
        'job_link': '//www.104.com.tw/job/7fywv?jobsource=jolist_d_relevance', 
        'job_name': '後端工程師(Python)', 
        'job_addr': '台北市松山區民權路3段178號15樓 | 詩嫚特集團_斯曼特企業股份有限公司', 
        'company_name': '詩嫚特集團_斯曼特企業股份有限公司', 
        'salary': '待遇面議',
        'education': '大學',
        'work_experience': ''
    }]))

    dbHandler.close()
    
