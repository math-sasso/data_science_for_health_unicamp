FROM ubuntu:18.04

LABEL maintainer="msasso@cpqd.com.br"

# Stamps the commit SHA into the labels and ENV vars
ARG BRANCH="master"
ARG COMMIT=""
LABEL branch=${BRANCH}
LABEL commit=${COMMIT}
ENV COMMIT=${COMMIT}
ENV BRANCH=${BRANCH}

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    build-essential \
    vim \
    chromium-browser \
    curl \
    libssl-dev \
    git \
    mercurial \
    pepperflashplugin-nonfree \
    openjdk-7-jre-headless\
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
 && rm -rf /var/lib/apt/lists/*

 # Install Miniconda and Python 3.8
ENV CONDA_AUTO_UPDATE_CONDA=false
ENV PATH=/home/user/miniconda/bin:$PATH
RUN curl -sLo ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-py38_4.8.2-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh \
 && conda install -y python==3.8.1 \
 && conda clean -ya

#installing requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ENV DATA_DIR = "/app/data/"

COPY ./src /app/word_hints_builder/src

WORKDIR /app/

EXPOSE 8080

# Entrypoint
ENTRYPOINT ["/bin/bash"]
CMD []