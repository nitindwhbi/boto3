# This code fetches job runs info for glue job.
# Change the numbers & date as per requirement.

import boto3
import datetime

def get_active_job_runs(glue_client, job_name):
    active_jobs = []
    response = glue_client.get_job_runs(
        JobName=job_name,
        MaxResults=5
    )
    for job in response['JobRuns']:
        if job['JobRunState'] in ['SUCCEEDED','FAILED']:
            active_jobs.append(job)
    job_cntr = 5
    while (job_cntr <= 200):
        if 'NextToken' in response:
            response = glue_client.get_job_runs(
                JobName=job_name,
                MaxResults=5,
                NextToken=response['NextToken']
            )
            for job in response['JobRuns']:
                if job['JobRunState'] in ['SUCCEEDED','FAILED']:
                    active_jobs.append(job)
        job_cntr += 5
    return active_jobs

client = boto3.client('glue')
JobName='glue-job-name'

total_runs = get_active_job_runs(client,JobName)

job=[]
etime=[]
acap=[]
usage = []
startedOn = []

for i in total_runs:
    if (datetime.date(2021, 12, 1) <= i['StartedOn'].date() <= datetime.date(2021, 12, 31)):
        job.append(i['Id'])
        etime.append(i['ExecutionTime'])
        acap.append(i['AllocatedCapacity'])
        startedOn.append(i['StartedOn'])


print ("Total job runs - " + str(len(job)))

for num1, num2 in zip(etime, acap):
    usage.append(num1 * num2)

print ("Total Capacity Time - " + str(sum(usage)))
