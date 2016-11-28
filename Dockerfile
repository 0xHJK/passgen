FROM ubuntu:16.04
MAINTAINER HJK <HJKdev+docker@gmail.com>
RUN echo 'nameserver 114.114.114.114' >> /etc/resolv.conf
RUN apt-get update
RUN apt-get install -y python3 curl
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
COPY ./conf/pip.conf /root/.pip/pip.conf
RUN pip install flask
RUN apt-get purge -y --auto-remove curl
RUN apt-get clean
WORKDIR /root
