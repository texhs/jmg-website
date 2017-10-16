import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:sa-east-1:537848568785:DeployJuliaMinegirlWebsiteTopic')

    location = {
        "bucketName": 'build.juliaminegirl',
        "objectKey": 'build-juliaminegirl-website.zip'
    }

    try:
        job = event.get("CodePipeline.job")
        if job:
            for artifact in job["data"]["inputArtifacts"]:
                if artifact["name"] == "MyAppBuild":
                    location = artifact["location"]["s3Location"]

        print "Building website from " + str(location)
        s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
        website_bucket = s3.Bucket('www.juliaminegirl.com.br')
        build_bucket = s3.Bucket(location["bucketName"])

        website_zip = StringIO.StringIO()
        build_bucket.download_fileobj(location["objectKey"], website_zip)

        with zipfile.ZipFile(website_zip) as myzip:
            for nm in myzip.namelist():
                obj=myzip.open(nm)
                print nm
                website_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                website_bucket.Object(nm).Acl().put(ACL='public-read')

        topic.publish(Subject="Julia Minegirl website deployed", Message="Julia Minegirl website deployed successfully")
        print "Job done!"
        if job:
            codepipeline = boto3.client('codepipeline')
            codepipeline.put_job_success_result(jobId=job["id"])
    except:
        topic.publish(Subject="Julia Minegirl website deploy FAILED", Message="The Julia Minegirl website was NOT deployed successfully")
    return 'Hello from Lambda'
