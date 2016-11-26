FROM ubuntu:xenial
MAINTAINER "Daniel Malon"

EXPOSE 22
VOLUME [ "/home" ]
WORKDIR /home

ARG BASE_PACKAGES="openssh-server curl wget vim-nox-py2 net-tools iputils-ping iputils-tracepath ngrep less libssl-dev python-pip python-cffi netcat"
ARG EXTRA_PACKAGES=""

RUN apt-get update -yy && \
    apt-get install -y $BASE_PACKAGES $EXTRA_PACKAGES && \
    apt-get clean && rm -rf /var/cache/apt/* /var/lib/apt/lists/* && \
    rm -rf /usr/share/doc/* /var/log/* && \
    touch /var/log/lastlog && \
    rm -rf /etc/update-motd.d/* && \
    rm -rf /etc/ssh/ssh_host_*_key.pub && \
    wget -qO /dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64 && \
    chmod +x /dumb-init

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD sshd_config /etc/ssh/sshd_config

ADD src/authorized_keys_iam.py /opt/iam/bin/authorized_keys
ADD src/sync_users_iam.py /opt/iam/bin/sync_users
ADD src/iam.py /opt/iam/bin/iam.py
ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]
