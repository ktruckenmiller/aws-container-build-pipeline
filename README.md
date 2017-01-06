# AWS Build System
This repo contains lambdas that will do things to get event based builds
to occur. 

# Deploy this infrastructure
In deploying to AWS, we use cloudformation's new serverless along side of docker containers to package and deploy our lambdas.


# Using the builder
Once the infrastructure is deployed, use the jenkins jobs (by replacing the invoked lambda function) in order to connect your repository to the lambdas.

Once you've connected the repository, `git tag` with the version of the repository to create a build event in the infrastructure. 


