#!/bin/sh
S3_BUCKET="lambda-deploys"
S3_PREFIX="aws-builders"
SUBFOLDER="builder"
STACK_NAME="lambda-deploys"


echo "Packaging your lambda function for AWS..."
docker pull ktruckenmiller/lambda-packager:python
CONTAINER=$(docker create -it ktruckenmiller/lambda-packager:python)
docker cp ./${SUBFOLDER}/ "${CONTAINER}:/build/"
docker start -i $CONTAINER
docker cp ${CONTAINER}:/deployment.zip ./${SUBFOLDER}
docker rm $CONTAINER

echo "Now we are getting the cloudformation ready..."
aws cloudformation package \
  --template-file serverless.yml \
  --s3-bucket ${S3_BUCKET} \
  --s3-prefix ${S3_PREFIX} \
  --output-template-file deploy.yml

echo "Deploying cloudformation..."
aws cloudformation deploy \
  --template-file deploy.yml \
  --stack-name ${STACK_NAME} \
  --capabilities CAPABILITY_IAM
