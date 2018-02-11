FROM sbneto/tesseract4:python-por

WORKDIR /app/tesseract

COPY tesseract/requirements.txt /app/tesseract/requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends poppler-utils imagemagick ghostscript \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
	&& apt-get autoremove -yqq \
	&& apt-get clean \
	&& rm -Rf /tmp/* /var/tmp/* /var/lib/apt/lists/*

# INSTALLING TESSERACT SERVICE
COPY etc /etc
RUN chmod 750 /etc/service/tesseract/run

COPY tesseract /app/tesseract

EXPOSE 8000
CMD ["/sbin/my_init"]
