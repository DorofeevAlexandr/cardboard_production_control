FROM postgres:16-alpine
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN echo "Europe/Moscow" > /etc/timezone
COPY cardboard_database.sql /docker-entrypoint-initdb.d/cardboard_database.sql
