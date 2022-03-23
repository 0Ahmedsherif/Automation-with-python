import requests
import smtplib
import os
import paramiko
import boto3
import time
import schedule

ec2_client = boto3.client('ec2', region_name='eu-west-3')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')


def send_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: WEBSITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)


def restart_server_and_container():
    print("Rebooting the server...")
    ec2_client.reboot_instances(
        InstanceIds=[
            'i-002da6349a7cb4617',
        ],
    )
    time.sleep(90)
    while True:
        statuses = ec2_client.describe_instance_status(InstanceIds=['i-002da6349a7cb4617'])['InstanceStatuses']
        nginx_state = statuses[0]['InstanceState']['Name']
        if nginx_state == 'running':
            restart_the_container()
            break


def restart_the_container():
    print("Restarting the application...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='15.188.194.6', username='ubuntu', key_filename='myKey2.pem')
    stdin, stdout, stderr = ssh.exec_command('docker start 6512317e772b')
    print(stdout.readlines())
    ssh.close()
    print('Application restarted')


def monitor_application():
    try:
        response = requests.get("http://15.188.194.6:8080/")
        if response.status_code == 200:
            print("Application is running successfully")
        else:
            print("Application Down. Fix it! ")
            msg = f'Application returned {response.status_code}. Fix the issue! Restart the application'
            send_notification(msg)
            restart_the_container()

    except Exception as err:
        print(f'Connection error happened: {err}')
        msg = 'Application not accessible'
        send_notification(msg)
        restart_server_and_container()


schedule.every(5).minutes.do(monitor_application)
while True:
    schedule.run_pending()