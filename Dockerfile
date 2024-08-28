# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY REQUIREMENTS REQUIREMENTS
RUN pip3 install -r REQUIREMENTS
ENV server_port='8080'
ENV client_host='127.0.0.1'
ENV client_port='3000'
ENV redis_host='127.0.0.1'
ENV redis_port='6379'
ENV cpe_path='/home/blackharry/Documents/NXO-Rennes/NXO-CPE-guesser/data/official-cpe-dictionary_v2.3.xml'
ENV cpe_source='https://nvd.nist.gov/feeds/xml/cpe/dictionary/official-cpe-dictionary_v2.3.xml.gz'
COPY bin bin
COPY etc /etc
COPY lib lib
COPY docker/entrypoint.sh entrypoint.sh

RUN mkdir /app/config
RUN chmod u+x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]