#!/bin/sh
# Author HJK 2016-11-21

QUIET=
VERBOSE=
CMD=
REPO='hjk/passgen'
NAME='passgen'
DIR=$(pwd)/code
PACKAGE=

usage()
{
    echo "Usage: `basename $0` COMMAND [-qv] [-r REPO] [-n NAME] [-d DIR] [PACKAGE]"
    echo "Commands: build run"
    exit 1
}

if [ $# -eq 0 ] || [[ $1 == 'build' ]]; then
    CMD='build'
elif [[ $1 == 'run' ]]; then
    CMD='run'
else
    usage
fi

echo "start ${CMD}"

shift 1

while getopts :qvr:n:d: OPTION
do
    case $OPTION in
        q)
            QUIET=y
            ;;
        v)
            VERBOSE=y
            ;;
        r)
            REPO=$OPTARG
            ;;
        n)
            NAME=$OPTARG
            ;;
        d)
            DIR=$OPTARG
            ;;
        \?)
            usage
            ;;
    esac
done

run()
{
    if [[ `docker ps -a | awk '{print $NF}' | grep "^${NAME}$"` ]]; then
        docker start -i ${NAME}
    else
        docker run -it --name ${NAME} -v ${DIR}:/root/code -p 5000:5000 ${REPO} python3 ./code/main.py
    fi
}

build()
{
    # echo "build func"
    if [[ `docker images | awk '{print $1}' | grep "^${REPO}$"` ]]; then
        run
    else
        # echo "building...."
        for pkg in $@
        do
            # echo "RUN apt -y install ${pkg}"
            echo "RUN apt-get -y install ${pkg} >> Dockerfile"
        done
        docker build -t ${REPO} .
        run
    fi
}

shift $(($OPTIND - 1))

if [[ ${CMD} == 'build' ]]; then
    build $@
elif [[ ${CMD} == 'run' ]]; then
    run
fi

