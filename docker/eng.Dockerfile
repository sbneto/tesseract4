FROM sbneto/tesseract4

ENV TESSERACT_TRAINED_LANG=eng
# DOWNLOADING TRAINED DATA
# https://tesseract-ocr.github.io/tessdoc/Data-Files.html
RUN mkdir -p /usr/local/share/tessdata \
    && wget -O /usr/local/share/tessdata/osd.traineddata \
        "https://github.com/tesseract-ocr/tessdata/raw/3.04.00/osd.traineddata" \
    && wget -O /usr/local/share/tessdata/equ.traineddata \
        "https://github.com/tesseract-ocr/tessdata/raw/3.04.00/equ.traineddata" \
    && wget -O /usr/local/share/tessdata/$TESSERACT_TRAINED_LANG.traineddata \
        "https://github.com/tesseract-ocr/tessdata/raw/master/$TESSERACT_TRAINED_LANG.traineddata"
