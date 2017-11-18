import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import httplib
import os
import time
from datetime import datetime, timedelta

def storeYoutubeInfoAtDatabase(result):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_YOUTUBE_INFO_TABLE_NAME'])
    table.put_item(
        Item={
            'id' : 1,
            'result' : result,
            'datetime': str(datetime.now())
        }
    )

def retrieveYoutubeInfoFromDatabase():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ['DB_YOUTUBE_INFO_TABLE_NAME'])
    record = table.query(
        KeyConditionExpression=Key('id').eq(1)
    )
    if record and record['Items']:
        return record['Items'][0]

def lambda_handler(event, context):

    record = retrieveYoutubeInfoFromDatabase()
    if record:
        print "Agora: " + str(datetime.now())
        print "Data hora do registro no BD: " + str(record['datetime'])
        age = datetime.now() - datetime.strptime(record['datetime'][:19], '%Y-%m-%d %H:%M:%S')

        print "Age: " + str(age)
        if (age <= timedelta(minutes = 1)):
            print "[INFO] The age is smaller than 1 minute. Let's reuse the cached information."
            return record['result']

    print "[INFO] The age is greater than 1 minute. Let's query Youtube."

    # Obtain environment variables
    URL = os.environ['YOUTUBE_API_URL']
    CHANNEL_ID = os.environ['CHANNEL_ID']
    NUMBER_OF_VIDEOS = os.environ['NUMBER_OF_VIDEOS']
    GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
    YOUTUBE_WATCH_URL = os.environ['YOUTUBE_WATCH_URL']
    URI = "/youtube/v3/search?part=snippet&channelId=" + CHANNEL_ID + "&maxResults=" + NUMBER_OF_VIDEOS + "&order=date&type=video&key=" + GOOGLE_API_KEY

    # Establish a https connection, get the response and store the JSON
    c = httplib.HTTPSConnection(URL)
    c.request("GET", URI)
    response = c.getresponse()
    text = response.read()
    data = json.loads(text)

    # Iterate over the JSON objects and create a customized result to return
    result = []
    index = 0
    for item in data['items']:
        snippet = item['snippet']
        index = index + 1
        video = {}
        video['index'] = str(index)
        video['title'] = snippet['title']
        video['url'] = YOUTUBE_WATCH_URL + item['id']['videoId']
        video['thumbnail'] = snippet['thumbnails']['high']['url']
        print str(snippet['thumbnails'])
        result.append(video)

    storeYoutubeInfoAtDatabase(result)
    print "[RESULT] " + str(result)
    return result
