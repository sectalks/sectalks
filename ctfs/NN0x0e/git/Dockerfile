FROM php:7.4-apache

RUN apt-get update && apt-get install -y git

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

COPY 000-default.conf /etc/apache2/sites-available/000-default.conf
RUN sed -i "s/Listen 80/Listen 8080/g" /etc/apache2/ports.conf

COPY ssl.crt /etc/apache2/ssl/ssl.crt
COPY ssl.key /etc/apache2/ssl/ssl.key
RUN mkdir -p /var/run/apache2/

RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf

COPY app/* /var/www/html/
WORKDIR /var/www/html
RUN composer update
RUN chown -R www-data:www-data /var/www/html
RUN a2enmod rewrite
RUN a2enmod ssl

ENTRYPOINT apache2-foreground

EXPOSE 8080
