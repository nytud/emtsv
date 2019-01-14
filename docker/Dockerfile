FROM ubuntu:18.04

WORKDIR /app

ENV PYTHONUNBUFFERED 1

# Update
RUN DEBIAN_FRONTEND=noninteractive apt-get update
# RUN DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade

# Install needed packages
RUN DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends -y install openjdk-8-jdk hfst python3 python3-pip python3-setuptools python3-dev build-essential git curl wget locales uwsgi uwsgi-plugin-python3 supervisor

# Install git-lfs repo
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash

# Install git-lfs
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install git-lfs

# Install locales. Any UTF-8 locale will do.
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Add non-privileged user
RUN groupadd uwsgi && useradd -g uwsgi uwsgi
RUN chown -R uwsgi:uwsgi /app

# Use git lfs for clone to make the process foolproof
RUN su - uwsgi -c 'git lfs clone --recurse-submodules https://github.com/dlt-rilmta/emtsv /app'

# We do not need shell for uwsgi anymore
RUN usermod -s /sbin/nologin uwsgi

RUN pip3 install Cython
RUN pip3 install -r emmorphpy/requirements.txt
RUN pip3 install -r purepospy/requirements.txt
RUN pip3 install -r emdeppy/requirements.txt
RUN pip3 install -r HunTag3/requirements.txt

RUN make -C emtokenpy/ all

# Add config files
RUN cp /app/docker/supervisor-app.conf /etc/supervisor/conf.d/

# CMD ["./test.sh"]

CMD ["supervisord", "-n"]
