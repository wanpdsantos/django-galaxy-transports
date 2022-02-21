FROM nginx:1.21-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /vol/static
RUN chmod 755 /vol/static