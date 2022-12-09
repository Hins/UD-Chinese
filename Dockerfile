# syntax=docker/dockerfile:1

FROM python:3.7.8

ADD . /code

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt  || true
RUN python /code/setup.py install

COPY . .

CMD python /code/monitoring.py --mon no --input /input --result /result