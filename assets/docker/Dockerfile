FROM postgres

MAINTAINER Mike Situ (github.com/shola)

USER postgres
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD changeme

ADD example.dump /tmp/example.dump
ADD load_sample_data.sh /docker-entrypoint-initdb.d/