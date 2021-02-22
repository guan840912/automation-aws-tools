import json
import requests
import logging
import boto3
import os
from base64 import b64decode


LINENOTIFYTOKENEN = os.environ['LINE_NOTIFY_TOKEN']
LINENOTIFYTOKEN = boto3.client('kms').decrypt(CiphertextBlob=b64decode(LINENOTIFYTOKENEN))['Plaintext'].decode('utf-8')


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=payload)
    return r.status_code
    
def meg_to_line(user_name, user_email, project_name, commits_message ):
    res = "\n"+"User Name: " + user_name +"\n" + "User Email: " + user_email +"\n"+ "Project Name: "+project_name + "\n"+"Messages: "+ commits_message
    return res

def meg_to_line_pipeline(project_name, user_name, branch_name ,commit_id,  commits_message , pipeline_status):
    res = "\n"+ "Project Name: "+project_name + "\n"+"User Name: " + user_name +"\n" + "Branch Name: " + branch_name  +"\n" + "Commit Id: " + commit_id + "\n"+"Messages: "+ commits_message + "\n"+"Pipeline Status: "+ pipeline_status
    return res

def lambda_handler(event, context):
    msg = json.loads(event['body'])
    tt = msg['object_kind']
    try:
        if tt == "push":
            rr = meg_to_line(msg['user_name'],msg['commits'][0]['author']['email'] , msg['project']['name'],msg['commits'][0]['message'] )
            lineNotifyMessage(LINENOTIFYTOKEN, str(rr))
        elif tt == "pipeline":
            rr = meg_to_line_pipeline(msg['project']['name'],msg['user']['name'],msg['object_attributes']['ref'],msg['commit']['id'],msg['commit']['message'],msg['object_attributes']['status'])
            lineNotifyMessage(LINENOTIFYTOKEN, str(rr))
        elif tt == "github":
            rr = "\n Project Name: cdk-terraform-source-code \n message: " + msg['newversion']
            lineNotifyMessage(LINENOTIFYTOKEN, str(rr))
    except:
        pass