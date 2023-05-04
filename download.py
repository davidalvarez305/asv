from posixpath import abspath
import datetime as dt
import paramiko
import os
from dotenv import load_dotenv
from website.asv.utils.upload_to_s3 import upload_to_s3

def main():
    load_dotenv()
    FILE_NAME = format(dt.date.today().replace(day=1) - dt.timedelta(days=1), '%B_%Y.csv')
    LOCAL_PATH = abspath('./website/uploads/' + FILE_NAME)

    # Download File From FTP
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(os.environ.get('FTP_HOST'), username=os.environ.get('FTP_USERNAME'), password=os.environ.get('FTP_PASSWORD'))
    
        sftp = ssh.open_sftp()

        sftp.get(remotepath=os.environ.get('FTP_PATH'), localpath=LOCAL_PATH)

    # Upload File to AWS S3 Bucket
    upload_to_s3(filename=FILE_NAME, localpath=LOCAL_PATH)

if __name__ == "__main__":
    main()