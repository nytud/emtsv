FROM python:3.8-buster


ENV PYTHONUNBUFFERED 1
ENV JAVA_HOME=/usr/lib/jvm/adoptopenjdk-8-hotspot-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${JAVA_HOME}/jre/lib/amd64/server/


# HFST, HUNSPELL
RUN apt-get update ; \
    apt-get install -y \
    hfst \
    hunspell \
    hunspell-hu \
    libhunspell-dev \
    software-properties-common \
    wget \
    ; \
    apt-get autoclean ; \
    apt-get autoremove -y


# JAVA
RUN wget -qO - https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public | apt-key add - ; \
    add-apt-repository --yes https://adoptopenjdk.jfrog.io/adoptopenjdk/deb/ ; \
    apt-get update && apt-get install -y adoptopenjdk-8-hotspot
RUN update-java-alternatives -s adoptopenjdk-8-hotspot-amd64


WORKDIR /app

COPY requirements.txt /app/
COPY emmorphpy/requirements.txt /app/emmorphpy/
COPY hunspellpy/requirements.txt /app/hunspellpy/
COPY purepospy/requirements.txt /app/purepospy/
COPY emdeppy/requirements.txt /app/emdeppy/
COPY HunTag3/requirements.txt /app/HunTag3/
COPY emudpipe/requirements.txt /app/emudpipe/
COPY embert/requirements.txt /app/embert/

RUN pip3 install --no-cache-dir uwsgi Cython numpy && pip3 install --no-cache-dir \
    -r requirements.txt \
    -r HunTag3/requirements.txt \
    -r emmorphpy/requirements.txt \
    -r hunspellpy/requirements.txt \
    -r purepospy/requirements.txt \
    -r emdeppy/requirements.txt \
    -r emudpipe/requirements.txt \
    -r embert/requirements.txt \
    ;

COPY . /app

RUN adduser --no-create-home --system --shell /sbin/nologin --group uwsgi


ENTRYPOINT ["/app/docker/entrypoint.sh"]
