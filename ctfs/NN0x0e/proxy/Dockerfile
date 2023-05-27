FROM nginx

ADD default.conf /etc/nginx/conf.d/default.conf
ADD index.html /usr/share/nginx/html/index.html
CMD ["/usr/sbin/nginx", "-g", "daemon off;"]