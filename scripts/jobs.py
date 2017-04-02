import schedule
import time
import requests
import logging

logging.basicConfig(level=logging.INFO)


spider_url  = "http://10.0.0.245:6800/schedule.json"

def check_github_job():
    logging.info("check start")
    payloads    = {
        'project': 'default',
        'spider': 'fetch-project',
    }
    requests.post(spider_url, data=payloads)
    logging.info("check finished")



schedule.every(4).hours.do(check_github_job)

while True:
    schedule.run_pending()
    time.sleep(1)
