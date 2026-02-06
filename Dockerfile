FROM nginx:alpine

# Copiar HTML
COPY src/index.html /usr/share/nginx/html/

# Configurar Nginx
RUN echo 'server {' > /etc/nginx/conf.d/default.conf && \
    echo '    listen 80;' >> /etc/nginx/conf.d/default.conf && \
    echo '    server_name localhost;' >> /etc/nginx/conf.d/default.conf && \
    echo '    root /usr/share/nginx/html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    index index.html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    ' >> /etc/nginx/conf.d/default.conf && \
    echo '    # CORS Headers' >> /etc/nginx/conf.d/default.conf && \
    echo '    add_header X-Frame-Options "ALLOWALL" always;' >> /etc/nginx/conf.d/default.conf && \
    echo '    add_header Content-Security-Policy "frame-ancestors *" always;' >> /etc/nginx/conf.d/default.conf && \
    echo '    add_header Access-Control-Allow-Origin "*" always;' >> /etc/nginx/conf.d/default.conf && \
    echo '    ' >> /etc/nginx/conf.d/default.conf && \
    echo '    location / {' >> /etc/nginx/conf.d/default.conf && \
    echo '        try_files $uri $uri/ /index.html;' >> /etc/nginx/conf.d/default.conf && \
    echo '    }' >> /etc/nginx/conf.d/default.conf && \
    echo '}' >> /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
