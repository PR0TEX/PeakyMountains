FROM prestashop/prestashop:1.7.8.7

LABEL org.opencontainers.image.source https://github.com/PR0TEX/PeakyMountains

RUN rm -rf /var/www/html/install

RUN apt-get update \
 && apt-get install memcached libmemcached-dev zlib1g-dev -y

RUN pecl install memcached

RUN echo extension=memcached.so >> /usr/local/etc/php/php.ini

RUN /etc/init.d/apache2 restart

## SSL
COPY ssl/domains.ext /etc/apache2/ssl/
COPY ssl/generate-keys.sh /etc/apache2/ssl/
WORKDIR /etc/apache2/ssl

RUN ./generate-keys.sh

RUN ls -lah

COPY ssl/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
RUN ln -s /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-enabled/default-ssl.conf

RUN a2enmod ssl

EXPOSE 80
EXPOSE 443

COPY config /tmp/init-scripts

WORKDIR /var/www/html

COPY app .

CMD ["/bin/sh", "entrypoint.sh"]