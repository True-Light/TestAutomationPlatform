FROM python:3.10

ENV ALLURE_RELEASE 2.21.0
ENV ALLURE_REPO https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline
ENV HTTP_PROXY_SERVER http://192.168.1.6:7890

COPY ./requirements.txt /tmp/requirements.txt

RUN apt-get -o Acquire::http::proxy="${HTTP_PROXY_SERVER}" update && \
    apt-get -o Acquire::http::proxy="${HTTP_PROXY_SERVER}" install -y --no-install-recommends \
      bzip2  \
      unzip  \
      xz-utils \
      binutils \
      fontconfig libfreetype6 \
      ca-certificates p11-kit && \
#    ln -s `which python3` /usr/bin/python && \
#    pip3 install --upgrade pip --proxy="${HTTP_PROXY_SERVER}" && \
    pip install --no-cache-dir -r /tmp/requirements.txt --proxy="${HTTP_PROXY_SERVER}" && \
    curl ${ALLURE_REPO}/${ALLURE_RELEASE}/allure-commandline-${ALLURE_RELEASE}.zip -L -o /tmp/allure-commandline.zip --proxy "${HTTP_PROXY_SERVER}" && \
        unzip -q /tmp/allure-commandline.zip -d / && \
        apt-get remove -y unzip && \
        rm -rf /tmp/* && \
        rm -rf /var/lib/apt/lists/* && \
        chmod -R +x /allure-$ALLURE_RELEASE/bin

ENV JAVA_HOME /usr/local/openjdk-20
ENV PATH $JAVA_HOME/bin:$PATH

# Default to UTF-8 file.encoding
ENV LANG C.UTF-8

# https://jdk.java.net/
# >
# > Java Development Kit builds, from Oracle
# >
ENV JAVA_VERSION 20

RUN set -eux; \
	\
	arch="$(dpkg --print-architecture)"; \
	case "$arch" in \
		'amd64') \
			downloadUrl='https://download.java.net/java/GA/jdk20/bdc68b4b9cbc4ebcb30745c85038d91d/36/GPL/openjdk-20_linux-x64_bin.tar.gz'; \
			downloadSha256='bb863b2d542976d1ae4b7b81af3e78b1e4247a64644350b552d298d8dc5980dc'; \
			;; \
		'arm64') \
			downloadUrl='https://download.java.net/java/GA/jdk20/bdc68b4b9cbc4ebcb30745c85038d91d/36/GPL/openjdk-20_linux-aarch64_bin.tar.gz'; \
			downloadSha256='b671dd1513e7bd4f3de6b1424a90a4998997a67593bf259936d55f5e83e31959'; \
			;; \
		*) echo >&2 "error: unsupported architecture: '$arch'"; exit 1 ;; \
	esac; \
	\
	wget -e "http_proxy=${HTTP_PROXY_SERVER}" --progress=dot:giga -O openjdk.tgz "$downloadUrl"; \
	echo "$downloadSha256 *openjdk.tgz" | sha256sum --strict --check -; \
	\
	mkdir -p "$JAVA_HOME"; \
	tar --extract \
		--file openjdk.tgz \
		--directory "$JAVA_HOME" \
		--strip-components 1 \
		--no-same-owner \
	; \
	rm openjdk.tgz*; \
	\
# update "cacerts" bundle to use Debian's CA certificates (and make sure it stays up-to-date with changes to Debian's store)
# see https://github.com/docker-library/openjdk/issues/327
#     http://rabexc.org/posts/certificates-not-working-java#comment-4099504075
#     https://salsa.debian.org/java-team/ca-certificates-java/blob/3e51a84e9104823319abeb31f880580e46f45a98/debian/jks-keystore.hook.in
#     https://git.alpinelinux.org/aports/tree/community/java-cacerts/APKBUILD?id=761af65f38b4570093461e6546dcf6b179d2b624#n29
	{ \
		echo '#!/usr/bin/env bash'; \
		echo 'set -Eeuo pipefail'; \
		echo 'trust extract --overwrite --format=java-cacerts --filter=ca-anchors --purpose=server-auth "$JAVA_HOME/lib/security/cacerts"'; \
	} > /etc/ca-certificates/update.d/docker-openjdk; \
	chmod +x /etc/ca-certificates/update.d/docker-openjdk; \
	/etc/ca-certificates/update.d/docker-openjdk; \
	\
# https://github.com/docker-library/openjdk/issues/331#issuecomment-498834472
	find "$JAVA_HOME/lib" -name '*.so' -exec dirname '{}' ';' | sort -u > /etc/ld.so.conf.d/docker-openjdk.conf; \
	ldconfig; \
	\
# https://github.com/docker-library/openjdk/issues/212#issuecomment-420979840
# https://openjdk.java.net/jeps/341
	java -Xshare:dump; \
	\
# basic smoke test
	fileEncoding="$(echo 'System.out.println(System.getProperty("file.encoding"))' | jshell -s -)"; [ "$fileEncoding" = 'UTF-8' ]; rm -rf ~/.java; \
	javac --version; \
	java --version

ENV ALLURE_HOME /allure-$ALLURE_RELEASE
ENV PATH $PATH:$ALLURE_HOME/bin

COPY ./scripts/worker-start.sh /worker-start.sh
RUN chmod +x /worker-start.sh
COPY ./scripts/beat-start.sh /beat-start.sh
RUN chmod +x /beat-start.sh

ENV PYTHONPATH /app

WORKDIR /app/celery_app

CMD ["/worker-start.sh"]
