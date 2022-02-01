FROM centos:7

RUN sudo yum install -y pip3 python3

COPY . /opt/app
WORKDIR /opt/app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "-d", "120", "-o", "output.txt"]