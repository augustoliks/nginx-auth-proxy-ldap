envsubst '$NGINX_SERVER_NAME' < /etc/nginx/conf.d/server-name.conf.template > /etc/nginx/conf.d/server-name.conf
envsubst '$NGINX_AUTH_COOKIE_NAME,$NGINX_AUTH_PROXY_LDAP_STARTTLS,$NGINX_SERVER_NAME,$NGINX_AUTH_PROXY_LDAP_SEARCH_FILTER,$NGINX_AUTH_PROXY_LDAP_REALM,$NGINX_AUTH_PROXY_LDAP_DISABLE_REFERRALS,$NGINX_AUTH_PROXY_LDAP_URL,$NGINX_AUTH_PROXY_LDAP_BASE_DN,$NGINX_AUTH_PROXY_LDAP_BIND_DN,$NGINX_AUTH_PROXY_LDAP_BIND_PASSWORD' < /etc/nginx/conf.d/auth-proxy.conf.template > /etc/nginx/conf.d/auth-proxy.conf


if $DEBUG == "1"; then
    while true; do
        sleep 1
        echo "debug ..."
    done
fi

nginx -g 'daemon off;'
