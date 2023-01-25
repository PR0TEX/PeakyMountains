
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


