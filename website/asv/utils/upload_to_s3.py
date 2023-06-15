import os
import boto3

def upload_to_s3(filename, localpath):
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(os.environ.get('AWS_BUCKET'))
        bucket.upload_file(localpath, "asv/" + filename)

        os.remove(localpath)
    except BaseException as err:
        print("Error uploading to S3: ", err)
        raise Exception(err)