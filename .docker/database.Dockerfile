FROM mysql:5

LABEL org.opencontainers.image.source https://github.com/PR0TEX/PeakyMountains

WORKDIR /docker-entrypoint-initdb.d

COPY db-dump/dump.sh /docker-entrypoint-initdb.d/dump.sh
COPY db-dump/dump.sql /docker-entrypoint-initdb.d/dump.sql

RUN chmod +x dump.sh

# RUN ./dump.sh