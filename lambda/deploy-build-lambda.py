import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes
import sys
import os

def lambda_handler(event, context):
    print "[Info] Starting execution..."

    print "[Info] Getting a reference to the SNS topic..."
    sns = boto3.resource('sns')
    topic = sns.Topic(os.environ['SNS_TOPIC'])
    location = {
        "bucketName": os.environ['DEFAULT_BUILD_BUCKET'],
        "objectKey": os.environ['ZIP_FILE_NAME']
    }

    try:
        print "[Info] Getting a reference to the Code Pipeline job..."
        job = event.get("CodePipeline.job")
        print "[Info] Job: " + str(job)
        if job:
            codepipeline = boto3.client('codepipeline')
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]
        print "[Info] Building website from " + str(location)

        print "[Info] Getting a reference to S3..."
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        website_bucket = s3.Bucket(os.environ['PRODUCTION_BUCKET'])
        print "[Info] Getting a reference to the website bucket: " + str(website_bucket)
        build_bucket = s3.Bucket(location["bucketName"])
        print "[Info] build_bucket name: " + location["bucketName"]
        print "[Info] Getting a reference to the build bucket: " + str(build_bucket)

        print "[Info] Creating a zip object..."
        website_zip = StringIO.StringIO()
        print "[Info] Downloading zip file to the destination bucket: " + location["objectKey"]
        build_bucket.download_fileobj(location["objectKey"], website_zip)

        with zipfile.ZipFile(website_zip) as myzip:
            for nm in myzip.namelist():
                obj=myzip.open(nm)
                print "[Info] " + nm
                website_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                website_bucket.Object(nm).Acl().put(ACL='public-read')

        topic.publish(Subject="Deploy OK", Message="Julia Minegirl website deployed successfully")
        print "[Info] Job done!"
        print "[Info] Job: " + str(job)
        if codepipeline:
            codepipeline.put_job_success_result(jobId=job["id"])
    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print "[Error]" + str(e)
        topic.publish(Subject="Deploy FAILED", Message="The Julia Minegirl website was NOT deployed successfully: " + str(e))
        if codepipeline:
            codepipeline.put_job_failure_result(jobId=job["id"], failureDetails=str(e))

    return 'Hello from Lambda'
