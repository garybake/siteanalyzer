GB WebPage Classifier
=====================
App to determine what a web page is about by classifying the image

Uses serverless aws architecture

Architecture
============
![Architecture](/docs/SiteAnalyzer.png)

Endpoints
=========
## Get list of all registered sites 
curl https://gbimmageclassifier.<yourdomain>/url/list 

## Get list of images for specific site
curl https://gbimmageclassifier.<yourdomain>/image/list?pageid=7213c7e3.www.garybake.com

## Request analysis of web page
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"url":"http://garybake.com"}' \
  https://gbimmageclassifier.<yourdomain>/url/analyze

AWS
===
Cloudformation
Route53
API gateway
Lambda
S3
DynamoDB
SQS
Cloudwatch 

Python
======
Boto3
BeautifulSoup
Requests

ENV
===
Needs the following environment variables set

export AWS_ACCOUNT_ID=***
export AWS_ACCESS_KEY_ID=***
export AWS_SECRET_ACCESS_KEY=***
export AWS_DEFAULT_REGION=***

export GBIMAGECLASSIFIER_BUCKET=***
export GBIMAGECLASSIFIER_TABLE=WebPage
export GBIMAGECLASSIFIER_CRAWLERQUEUE=CrawlerQueue
export GBIMAGECLASSIFIER_ANALYSISQUEUE=AnalysisQueue
export GBIMAGECLASSIFIER_DOMAIN=***
export GBIMAGECLASSIFIER_REGION=$AWS_DEFAULT_REGION

TODO
====

Front end UI
Add ui-service to deploy.sh
Refactor project layout
Move boto objects out of functions
AWS_DEFAULT_REGION is a reserved parameter (ui-service)
