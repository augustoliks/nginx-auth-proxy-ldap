FROM debian:buster-slim as cert-key
WORKDIR /app
RUN apt update -y && apt install openssl apache2-utils -y
RUN mkdir /dist
COPY cert-scripts .
RUN sh create-certificate.sh
RUN cp cert.crt /dist/ 
RUN cp cert.key /dist/

FROM nginx as production
# FROM nginx:1.18 as production
COPY --from=cert-key /dist/ /etc/ssl/certs/
# COPY cert-files/dhparam.pem /etc/ssl/certs/dhparam.pem
COPY conf.d/ /etc/nginx/conf.d/
COPY static/ /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf
COPY run.sh /run.sh
RUN rm -f /etc/nginx/conf.d/default.conf
CMD ["/run.sh"]
