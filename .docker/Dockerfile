FROM prestashop/prestashop-git:7.4

# To run files with the same group as your primary user
RUN groupmod -g 1000 www-data \
  && usermod -u 1000 -g 1000 www-data

COPY .docker/wait-for-it.sh /tmp/
COPY .docker/docker_run_git.sh /tmp/

RUN mkdir -p /var/www/.npm
RUN chown -R www-data:www-data /var/www/.npm

# These two directories are docker mounted volumes
RUN chown -R www-data:www-data /var/www/html/vendor
RUN chown -R www-data:www-data /var/www/html/var

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt install -y nodejs

RUN apt -y install npm

CMD ["/tmp/docker_run_git.sh"]


## SSL
COPY ssl/generate-keys.sh /etc/apache2/ssl/
CMD ["/etc/apache2/ssl/generate-keys.sh"]

# COPY ssl/keys /etc/apache2/ssl

COPY ssl/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf
RUN ln -s /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-enabled/default-ssl.conf

RUN a2enmod ssl

EXPOSE 80
EXPOSE 443

# RUN service apache2 restart
