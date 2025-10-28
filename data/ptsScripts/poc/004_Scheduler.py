'''
Created on 10-Mar-2025
This Module shows you important features of pytask scripting
@author: kayma
'''
import kTools; tls = kTools.KTools()
import time

def hello():
    tls.info("Hello scheduler - start!")
    time.sleep(9)    
    tls.info("Hello scheduler - end!")

PTS.sch.every(3).seconds.do(hello).tag("first-task")
#PTS.sch.every(10).minutes.do(job)
#PTS.sch.every().hour.do(job)
#PTS.sch.every().day.at("10:30").do(job)
#PTS.sch.every().monday.do(job)
#PTS.sch.every().wednesday.at("13:15").do(job)
#PTS.sch.every().day.at("12:42", "Europe/Amsterdam").do(job)
#PTS.sch.every().minute.at(":17").do(job)
#https://schedule.readthedocs.io/en/stable/examples.html

#To list jobs
#PTS.sch.jobs
#To cancel the job from listed jobs
#PTS.sch.cancel_job(PTS.sch.jobs[0])
#To stop all jobs
#PTS.sch.clear()
#To stop selected tagged jobs
#PTS.sch.clear("first-task")