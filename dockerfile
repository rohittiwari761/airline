FROM python:3
WORKDIR /usr/src/app
ADD requirments.txt /usr/src/app
RUN pip install -r requirments.txt
ADD . /usr/src/app
