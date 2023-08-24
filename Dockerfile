FROM python:3.8-buster


ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/bin
ENV PATH="$JAVA_HOME/bin:${PATH}"
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${JAVA_HOME}/jre/lib/amd64/server/
ENV EMTSV_NUM_PROCESSES=2


# HFST, HUNSPELL
RUN apt-get update ; \
    apt-get install -y \
    hfst \
    libhunspell-dev \
    software-properties-common \
    openjdk-11-jdk-headless \
    wget \
    ; \
    apt-get autoclean ; \
    apt-get autoremove -y

WORKDIR /app

COPY requirements.txt /app/
COPY embert/requirements.txt /app/embert/

RUN python3 -m pip install --no-cache-dir uwsgi cython numpy && \
    python3 -m pip install --no-cache-dir -r requirements.txt \
    ;
# Workaround for embert requirements.txt
#     -r embert/requirements.txt \

COPY . /app

RUN adduser --no-create-home --system --shell /sbin/nologin --group uwsgi


ENTRYPOINT ["/app/docker/entrypoint.sh"]
