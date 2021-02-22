from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import boto3
import os
import time
from base64 import b64decode
import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
ENCRYPTEDWebhookHandler = os.environ['WebhookHandler']
handler = WebhookHandler(boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTEDWebhookHandler))['Plaintext'].decode('utf-8'))
ENCRYPTEDLineBotApi = os.environ['LineBotApi']
line_bot_api = LineBotApi(boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTEDLineBotApi))['Plaintext'].decode('utf-8'))
def validIP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True
from botocore.exceptions import ClientError
security_group_id="sg-xxxxxxxxxxxxxxx"

def lambda_handler(event, context):
    try: 
        msg = json.loads(event['body'])
        tt = msg['events'][0]['message']['text']
        a = tt.split(',', 2)
        if a[0] == "add":
            try:
                res = validIP(a[1])
                if res == True:
                    ec2 = boto3.client('ec2')
                    ec2.authorize_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[{'IpProtocol': 'tcp','FromPort': 60000,'ToPort': 60000,'IpRanges': [{'CidrIp': a[1] + "/32"}]}])
                    line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="All Ready add your soure ip : " + a[1]))
                else:
                    line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Your Ip address not valid !!!"))
            except:
                line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Your Ip address not valid !!!"))
                pass
        elif a[0] == "del":
            try:
                res = validIP(a[1])
                if res == True:
                    ec2 = boto3.client('ec2')
                    ec2.revoke_security_group_ingress(
                    GroupId=security_group_id,
                    IpPermissions=[{'IpProtocol': 'tcp','FromPort': 60000,'ToPort': 60000,'IpRanges': [{'CidrIp': a[1] + "/32"}]}])
                    line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="All Ready delete your soure ip : " + a[1]))
                else:
                    line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Your Ip address not valid !!!"))
            except:
                line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Your Ip address not valid !!!"))
                pass
        elif a[0] == "help":
            try:
                if True:
                    res ='1. add ingress\n   - add,1.1.1.1\n2. delete ingress\n   - del,1.1.1.1\n3. list ingress\n   - list\n4. help\n   - help'
                    line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text=res))
            except:
                line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Your Ip address not valid !!!"))
                pass
        elif a[0] == "list":
            try:
                if True:
                    ec2 = boto3.client('ec2')
                    res = ec2.describe_security_groups(
                    GroupIds=[security_group_id])
                    resjson = res['SecurityGroups'][0]
                    tempipRange = ''
                    for a in resjson['IpPermissions']:
                        try:
                            if a['FromPort'] == 60000:
                                for b in a['IpRanges']:
                                    #print('----------------')
                                    #print (b['CidrIp'])
                                    tempipRange = tempipRange + b['CidrIp'] + "\n"
                                    #print('----------------')
                        except:
                            pass
                    line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text='your ip list is \n'+tempipRange))
                else:
                    line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Your Ip address not valid !!!"))
            except:
                line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Your Ip address not valid !!!"))
                pass
        elif a[0] == "db2":
            try:
                if a[1] == "re":
                    client = boto3.client('ssm')
                    res = client.send_command(InstanceIds=['i-xxxxxxxxx'],DocumentName="AWS-RunShellScript",Parameters={'commands': ['restartdb2.sh']})
                    resid = res['Command']['CommandId']
                    time.sleep(5)
                    rescc = client.get_command_invocation(CommandId=resid,InstanceId='i-xxxxxxxxx')
                    statuscc = rescc['StatusDetails']
                    line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="RunShellScript status: " + statuscc))
                else:
                    line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Nothing to Doing just echo your message: "+tt))
            except:
                line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Nothing to Doing just echo your message something error: "+tt))
                pass
        else:
            line_bot_api.reply_message(msg['events'][0]['replyToken'],TextSendMessage(text="Nothing to Doing just echo your message: "+tt))
        response = {"statusCode": 200,"body": json.dumps({"message": 'ok'})}
        return response
    except:
        pass
