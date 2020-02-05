# FROM mittelholcz/hfst:hfst-v3.15.0
FROM python:3.8-buster


ENV PYTHONUNBUFFERED 1
# ENV LANGUAGE en_US:en

# RUN apk --no-cache add \
#     build-base \
#     gfortran \
#     linux-headers \
#     musl-dev \
#     openblas-dev \
#     openjdk8 \
#     py3-setuptools \
#     python3-dev \
#     hunspell-dev \
#     ;

RUN apt-get update ; \
    apt-get install -y \
    hfst \
    hunspell \
    hunspell-hu \
    libhunspell-dev \
    openjdk-11-jdk \
    ; \
    apt-get autoclean ; \
    apt-get autoremove -y

# RUN ln -s /usr/lib/libhunspell-1.6.so /usr/lib/libhunspell.so  # TODO: Hack for Hunspell
# ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk
# ENV PATH="$JAVA_HOME/bin:${PATH}"
# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jvm/java-1.8-openjdk/jre/lib/amd64/server/
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

# WORKDIR /app

# COPY requirements.txt /app/
# COPY emmorphpy/requirements.txt /app/emmorphpy/
# COPY hunspellpy/requirements.txt /app/hunspellpy/
# COPY purepospy/requirements.txt /app/purepospy/
# COPY emdeppy/requirements.txt /app/emdeppy/
# COPY HunTag3/requirements.txt /app/HunTag3/
# COPY emudpipe/requirements.txt /app/emudpipe/
# COPY embert/requirements.txt /app/embert/

# RUN pip3 install --no-cache-dir uwsgi Cython && pip3 install --no-cache-dir \
#     -r requirements.txt \
#     -r HunTag3/requirements.txt \
#     -r emmorphpy/requirements.txt \
#     -r hunspellpy/requirements.txt \
#     -r purepospy/requirements.txt \
#     -r emdeppy/requirements.txt \
#     -r emudpipe/requirements.txt \
#     -r embert/requirements.txt \
#     ;

# COPY . /app

# RUN addgroup uwsgi ; adduser -H -S -s /sbin/nologin -G uwsgi uwsgi

# ENTRYPOINT ["/app/docker/entrypoint.sh"]
