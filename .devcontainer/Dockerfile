FROM node:24

RUN apt update && apt install -y \
    locales \
    git\
    sudo \
    && apt clean -y \
    && rm -rf /var/lib/apt/lists/*
    

RUN sed -i -e 's/# \(ja_JP.UTF-8\)/\1/' /etc/locale.gen \
    && locale-gen \
    && update-locale
ENV LANG=ja_JP.UTF-8

ENV TZ=Asia/Tokyo

RUN usermod -aG sudo node
USER node

WORKDIR /workspace
