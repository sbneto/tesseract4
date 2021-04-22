FROM python:3.9-slim-buster

# https://github.com/DanBloomberg/leptonica/releases
# https://github.com/tesseract-ocr/tesseract/commits/master
ENV LEPTONICA_VERSION="1.80.0" \
    TESSERACT_SHA="66a963b50a8a89cd7d65f6185d6a21ffb749b246" \
    LIBMAGIC_VERSION="5.39" \
    PATH="/usr/local/bin:/usr/local/lib:$PATH"

COPY tesseract /app/tesseract
RUN set -ex \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update \
    && buildDeps=" \
        automake \
        g++ \
        git \
        libtool \
        make \
        pkg-config \
        autoconf \
        autoconf-archive \
        pkg-config \
        libpng-dev \
        libjpeg62-turbo-dev \
        libtiff5-dev \
        libwebp-dev \
        libopenjp2-7-dev \
        libgif-dev \
        zlib1g-dev \
    " \
    && apt-get install -y --no-install-recommends \
        $buildDeps \
        ca-certificates \
        libpng16-16 \
        libjpeg62-turbo \
        libtiff5 \
        libwebp6 \
        libopenjp2-7 \
        libgif7 \
        zlib1g \
        wget \
        git \
        unzip \
        # EXTRA TOOLS
        poppler-utils \
        ghostscript \
        imagemagick \
    && cd /tmp \
    # DOWNLOADING LIBMAGIC
    # do not use another image compilation as these might differ
    && wget -O /tmp/libmagic.tar.gz https://deb.debian.org/debian/pool/main/f/file/file_$LIBMAGIC_VERSION.orig.tar.gz \
    && mkdir -p /usr/src/libmagic \
    && tar -xzC /usr/src/libmagic -f /tmp/libmagic.tar.gz \
    && rm /tmp/libmagic.tar.gz \
    && cd /usr/src/libmagic/file-$LIBMAGIC_VERSION \
    # COMPILING LIBMAGIC
    && ./configure --host=x86_64-pc-linux-gnu \
    && make \
    && make install \
    && ldconfig \
    && cd /tmp \
    && rm -rf /usr/src/libmagic \
    # DOWNLOADING LEPTONICA
    && wget -O /tmp/leptonica.tar.gz "https://github.com/DanBloomberg/leptonica/releases/download/$LEPTONICA_VERSION/leptonica-$LEPTONICA_VERSION.tar.gz" \
    && mkdir -p /usr/src/leptonica \
    && tar -xzC /usr/src/leptonica -f /tmp/leptonica.tar.gz \
    && rm /tmp/leptonica.tar.gz \
    # COMPILING LEPTONICA
    # http://www.leptonica.org/source/README.html
    && cd /usr/src/leptonica/leptonica-$LEPTONICA_VERSION \
    && ./configure \
    && make \
    && make install \
    && cd /tmp \
    && rm -rf /usr/src/leptonica \
    # DOWNLOADING TESSERACT
    && wget -O /tmp/tesseract.zip "https://github.com/tesseract-ocr/tesseract/archive/${TESSERACT_SHA}.zip" \
    && mkdir -p /usr/src/tesseract \
    && unzip /tmp/tesseract.zip -d /usr/src/tesseract \
    && rm /tmp/tesseract.zip \
    # COMPILING TESSERACT
    # https://tesseract-ocr.github.io/tessdoc/Compiling-%E2%80%93-GitInstallation.html
    && cd /usr/src/tesseract/tesseract-${TESSERACT_SHA} \
    && ./autogen.sh \
    && ./configure LDFLAGS="-L/usr/local/lib" CFLAGS="-O2 -I/usr/local/include" \
    &&  make \
    && make install \
    && ldconfig \
    && cd /tmp \
    && rm -rf /usr/src/tesseract \
    # INSTALL PYTHON SERVERLIBLEPT_HEADERSDIR
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade -r /app/tesseract/requirements.txt \
    # CLEANUP
    && apt-get purge -yqq $buildDeps \
    && apt-get autoremove -yqq \
    && apt-get clean \
    && rm -Rf /tmp/* /var/tmp/* /var/lib/apt/lists/*

EXPOSE 8000

WORKDIR /app/tesseract

CMD ["python3", "/app/tesseract/app.py"]