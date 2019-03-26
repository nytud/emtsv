FROM mittelholcz/hfst-docker:v3.15.0


ENV PYTHONUNBUFFERED 1
ENV LANGUAGE en_US:en
ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
ENV PATH="$JAVA_HOME/bin:${PATH}"

RUN apk --no-cache add \
    alpine-sdk \
    openblas-dev \
    openjdk8 \
    py3-setuptools \
    python3-dev \
    supervisor \
    uwsgi \
    uwsgi-python3

WORKDIR /app
COPY . /app

RUN pip3 install Cython && pip3 install \
        -r emmorphpy/requirements.txt \
        -r purepospy/requirements.txt \
        -r emdeppy/requirements.txt \
        -r HunTag3/requirements.txt

RUN mkdir -p /etc/supervisor.d/ && \
    cp /app/docker/supervisor-emtsv.ini /etc/supervisor.d/

    # adduser -S uwsgi -G uwsgi -H -s /sbin/nologin
    # addgroup -S uwsgi && \

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# FROM ubuntu:18.04

# WORKDIR /app
# COPY . /app

#     # apt-get --no-install-recommends -y install \

# RUN apt-get update && \
#     apt-get dist-upgrade -y && \
#     apt-get -y install \
#         gcc \
#         openjdk-8-jdk \
#         hfst \
#         python3 \
#         python3-pip \
#         python3-setuptools \
#         python3-dev \
#         build-essential \
#         locales \
#         uwsgi \
#         uwsgi-plugin-python3 \
#         supervisor && \
#     sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
#     locale-gen && \
#     pip3 install Cython && \
#     pip3 install \
#         -r emmorphpy/requirements.txt \
#         -r purepospy/requirements.txt \
#         -r emdeppy/requirements.txt \
#         -r HunTag3/requirements.txt && \
#     cp /app/docker/supervisor-app.conf /etc/supervisor/conf.d/ && \
#     groupadd uwsgi && \
#     useradd -g uwsgi uwsgi && \
#     usermod -s /sbin/nologin uwsgi

# ENV PYTHONUNBUFFERED 1
# ENV LANG en_US.UTF-8
# ENV LANGUAGE en_US:en
# ENV LC_ALL en_US.UTF-8

# CMD ["supervisord", "-n"]
