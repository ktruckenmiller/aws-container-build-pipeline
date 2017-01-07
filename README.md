# AWS Builder Bros
This repo contains lambdas that will do things to get event based builds
to occur. On git push tag, we'll build and update your dockerfile using
codebuild.


Prerequisites:
  - credstash with a github key stored (github.token in this example)
  - docker installed
  - aws cli
  - .om file in your repository root


You'll need an .om yaml-syntax file in the root repo like this:

```
build:
  artifacts:
    docker-friend:
      dockerfile: Dockerfile.ruby
      dockerhub: ktruckenmiller/docker-friend
```

This means, I'm going to build an image and upload it to dockerhub using the
dockerfile specified.
