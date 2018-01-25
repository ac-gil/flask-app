FROM ubuntu:16.04
RUN apt-get update -y --fix-missing
RUN apt-get install -y curl
COPY ./ /test
WORKDIR /test