#!/bin/bash

# convenience functions for removing all running/exited containers
# add these to your ~/.bash_profile if desired:
#   alias rmrfDockerContainers="docker stop $(docker ps -a -q) && docker rm $(docker ps -a -q)"
#   alias rmrfDockerImages="docker rmi $(docker images)"

# curl example data
curl -L -O http://cl.ly/173L141n3402/download/example.dump

# build postgres image
docker build . -t mypostgres:latest

# run postgres in the background
docker run --name some-postgres mypostgres -d postgres

# login to postgres terminal (as "postgres" user)
docker exec -it some-postgres psql --dbname pgguide
