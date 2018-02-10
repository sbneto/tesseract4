FROM sbneto/tesseract4:python-por

RUN apt-get update \
    && apt-get install -y imagemagick ghostscript \
	&& apt-get autoremove -yqq \
	&& apt-get clean \
	&& rm -Rf /tmp/* /var/tmp/* /var/lib/apt/lists/*

# INSTALLING TESSERACT SERVICE
COPY etc /etc
RUN chmod 750 /etc/service/tesseract/run

COPY tesseract /app/tesseract

EXPOSE 8000
CMD ["/sbin/my_init"]
