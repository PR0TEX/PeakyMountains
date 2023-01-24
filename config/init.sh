#!/bin/sh

echo """
UPDATE ps_configuration
SET value='localhost'
WHERE name = 'PS_SHOP_DOMAIN';

UPDATE ps_configuration
SET value='localhost'
WHERE name = 'PS_SHOP_DOMAIN_SSL';

UPDATE ps_configuration
SET value=1
WHERE name = 'PS_SSL_ENABLED';

UPDATE ps_configuration
SET value=1
WHERE name = 'PS_SSL_ENABLED_EVERYWHERE';

""" >postinstall.sql


mysql \
  -u"$DB_USER" \
  -p"$DB_PASSWD" \
  -h "$DB_SERVER" \
  "$DB_NAME" \
  <postinstall.sql

DUMP_FILE=/db-dump/dump.sql

if [ -f "$DUMP_FILE" ]; then
  mysql \
    -u"$DB_USER" \
    -p"$DB_PASSWD" \
    -h "$DB_SERVER" \
    "$DB_NAME" \
    <$DUMP_FILE
fi
