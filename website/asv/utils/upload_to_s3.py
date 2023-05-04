import os
import boto3

def upload_to_s3(filename, localpath):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(os.environ.get('AWS_BUCKET'))
    bucket.upload_file(localpath, "asv/" + filename)

    os.remove(localpath)