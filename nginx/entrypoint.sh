#!/bin/sh
set -e

TEMPLATE_DIR=/etc/nginx/templates
CONF_DIR=/etc/nginx/conf.d

if [ -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]; then
  TEMPLATE="${TEMPLATE_DIR}/default-https.conf.template"
else
  TEMPLATE="${TEMPLATE_DIR}/default-http.conf.template"
fi

envsubst '$DOMAIN' < "$TEMPLATE" > "${CONF_DIR}/default.conf"

exec nginx -g 'daemon off;'
