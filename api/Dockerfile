FROM ubuntu:16.04

ADD . /app

WORKDIR /app

RUN apt-get update && apt-get install -y libssl-dev libffi-dev autoconf automake libtool python3 python3-pip software-properties-common
RUN add-apt-repository ppa:ethereum/ethereum
RUN apt-get update && apt-get install -y solc
RUN apt-get update && apt-get install -y apt-transport-https curl
RUN pip3 install web3
RUN pip3 install py-solc
RUN pip3 install eth-testrpc
RUN pip3 install flask
RUN ls -l
EXPOSE 1234

CMD python3 server.py 
