FROM python:3.10-slim
# set work directory
WORKDIR /app

#required  for python-ldap
RUN apt-get update && \
apt-get --yes install build-essential python3-dev libmemcached-dev libldap2-dev libsasl2-dev libzbar-dev  ldap-utils tox lcov valgrind && \
apt-get clean


#required for mysqlclient
RUN apt-get -y install python3-dev default-libmysqlclient-dev build-essential pkg-config
# set environment variables 1s


# insert requirement,txt to the apps directory and other file
COPY . .


#RUN  pip install --upgrade pip
RUN python -m pip install setuptools
RUN python -m pip install python-ldap
RUN python -m pip install mysqlclient
RUN pip3 install --no-cache-dir -r requirements.txt




EXPOSE 8000


#CMD ["python3", "manage.py", "runserver","localhost:8000" , "-e", "production"]

