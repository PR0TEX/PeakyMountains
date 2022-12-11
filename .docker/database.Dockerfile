FROM mysql:5

WORKDIR /docker-entrypoint-initdb.d

COPY db-dump/dump.sh /docker-entrypoint-initdb.d/dump.sh
COPY db-dump/dump.sql /docker-entrypoint-initdb.d/dump.sql

RUN chmod +x dump.sh

# RUN ./dump.sh