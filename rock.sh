#!/bin/bash
# Author HJK 2016-11-21

REPO='hjk/passgen'
NAME='passgen'
DIR=$(pwd)/code
PORT_HOST=5000
PORT_DOCKER=5000

run()
{
    if [[ `docker ps -a | awk '{print $NF}' | grep "^${NAME}$"` ]]; then
        docker start ${NAME}
    else
        docker run -d --name ${NAME} -v ${DIR}:/root/code -p ${PORT_HOST}:${PORT_DOCKER} ${REPO} python3 ./code/main.py
    fi
}


if [[ `docker images | awk '{print $1}' | grep "^${REPO}$"` ]]; then
    run
else
    docker build -t ${REPO} .
    run
fi
