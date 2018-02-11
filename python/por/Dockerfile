FROM sbneto/tesseract4:python

ENV TESSERACT_TRAINED_LANG=por
# DOWNLOADING TRAINED DATA
RUN mkdir -p $TESSDATA_PREFIX/tessdata \
    && wget -O $TESSDATA_PREFIX/tessdata/osd.traineddata "https://github.com/tesseract-ocr/tessdata/raw/3.04.00/osd.traineddata" \
    && wget -O $TESSDATA_PREFIX/tessdata/equ.traineddata "https://github.com/tesseract-ocr/tessdata/raw/3.04.00/equ.traineddata" \
    && wget -O $TESSDATA_PREFIX/tessdata/$TESSERACT_TRAINED_LANG.traineddata "https://github.com/tesseract-ocr/tessdata/raw/master/$TESSERACT_TRAINED_LANG.traineddata" \
    && wget -O $TESSDATA_PREFIX/tessdata/${TESSERACT_TRAINED_LANG}_lstm.traineddata "https://github.com/tesseract-ocr/tessdata_fast/raw/master/$TESSERACT_TRAINED_LANG.traineddata"
