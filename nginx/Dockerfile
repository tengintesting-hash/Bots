FROM nginx:1.27-alpine

COPY conf.d/default-http.conf /etc/nginx/templates/default-http.conf.template
COPY conf.d/default-https.conf /etc/nginx/templates/default-https.conf.template
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
