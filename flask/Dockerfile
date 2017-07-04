FROM ubuntu:16.04
MAINTAINER tristan.klose@bfarm.de

RUN apt-get update -y && apt-get install virtualenv python-pip python3-pip python3-dev -y

RUN cd  ~ && mkdir venvs && virtualenv --python=/usr/bin/python3 venvs/flaskproj
RUN mkdir /root/flaskproj
WORKDIR /root/flaskproj
ADD Git/ /root/flaskproj/
ADD run.sh /root/flaskproj/run.sh
RUN chmod 777 run.sh 
RUN ./run.sh

# Serverstart
ADD start.sh /root/flaskproj/start.sh
RUN chmod 777 start.sh 
CMD ["./start.sh"]