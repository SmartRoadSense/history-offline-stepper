FROM python:3

WORKDIR /tmp

RUN pip install psycopg2-binary
RUN pip install numpy

RUN apt-get update && apt-get install -yq --no-install-recommends \
    apt-utils \
    curl \
    # Install git
    git \
    # Install apache
    apache2 \
    # Install php 7.2
    libapache2-mod-php7.2 \
    php7.2-cli \
    php7.2-json \
    php7.2-curl \
    php7.2-fpm \
    php7.2-gd \
    php7.2-ldap \
    php7.2-mbstring \
    php7.2-sqlite3 \
    php7.2-xml \
    php7.2-pgsql \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . /tmp/.

VOLUME /data

CMD ["bash"]