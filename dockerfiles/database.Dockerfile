FROM mysql:5

LABEL org.opencontainers.image.source https://github.com/PR0TEX/PeakyMountains

COPY db-dump/dump.sql /docker-entrypoint-initdb.d/dump.sql