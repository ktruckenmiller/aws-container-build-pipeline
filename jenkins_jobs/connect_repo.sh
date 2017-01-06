#!/bin/sh

set -x

cat << EOF > payload.json
	{
    	"repo_name": "$repo_name"
    }
EOF
## put awscli or boto code here that imports the name of the lambda and uses it as a variable
docker pull ktruckenmiller/awscli
container_id=$(docker create -ti ktruckenmiller/awscli lambda invoke \
 	--region us-west-2 \
 	--function-name arn:aws:lambda:us-west-2:601394826940:function:github-connector-RepoConnector-WI3603YJ91EK \
 	--payload file:///aws/payload.json \
 	result.txt)
docker cp payload.json $container_id:/aws/payload.json



docker start -i $container_id


docker wait $container_id
docker logs $container_id
docker cp $container_id:/aws/result.txt result.txt


docker rm $container_id
