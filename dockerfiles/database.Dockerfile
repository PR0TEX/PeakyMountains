FROM mysql:5

LABEL org.opencontainers.image.source https://github.com/PR0TEX/PeakyMountains

COPY db-dump/dump.sql /docker-entrypoint-initdb.d/dump.sql
# COPY db-dump/dump.sh /docker-entrypoint-initdb.d/dump.sh

# RUN chmod +x /docker-entrypoint-initdb.d/dump.sh