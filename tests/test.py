from os import path
from xmlrpc.client import ServerProxy

BASE_FOLDER = path.dirname(path.abspath(__file__))
proxy = ServerProxy('http://127.0.0.1:8000/', use_builtin_types=True)

small_image_convert = {
    'output_options': [
        '-colorspace', 'gray',
        '-type', 'grayscale',
        '-contrast-stretch', '0',
        '-fill', 'white',
        '-opaque', 'none',
        '-alpha', 'off',
        '-background', 'white',
        '-deskew', '40%',
        '-trim',
        '+repage',
        '-compose', 'over',
        '-bordercolor', 'white',
        '-border', '10',
        '-liquid-rescale', '200%',
    ],
}


def test_pdf_as_image():
    with open(path.join(BASE_FOLDER, 'test.pdf'), 'rb') as f:
        proxy.pdf_as_images(f.read())


def test_tesseract_multiple_images():
    with open(path.join(BASE_FOLDER, 'number.gif'), 'rb') as f:
        img = f.read()
    text = str(proxy.tesseract([img, img, img], {'convert': small_image_convert}), 'utf-8')
    assert text == '(12) 99738 5318\n\f(12) 99738 5318\n\f(12) 99738 5318\n\f'


def test_tesseract_simple_phone_number():
    with open(path.join(BASE_FOLDER, 'number.gif'), 'rb') as f:
        text = str(proxy.tesseract(f.read(), {'convert': small_image_convert}), 'utf-8')
    assert text == '(12) 99738 5318\n\f'


def test_convert_simple_phone_number():
    with open(path.join(BASE_FOLDER, 'number.gif'), 'rb') as f:
        proxy.convert(f.read(), small_image_convert)


def test_tesseract_pdf():
    with open(path.join(BASE_FOLDER, 'test.pdf'), 'rb') as f:
        text = str(proxy.tesseract(f.read()), 'utf-8')
    assert 'PRÁTICA NA ADVOCACIA PROCESSUAL CIVIL' in text
    assert 'CURSOS LUIZ FLÁVIO GOMES Prof Renato Montans' in text
    assert 'Modelos práticos' in text
    assert '1. Petição inicial rito ordinário' in text
    assert 'EXCELENTÍSSIMO SENHOR DOUTOR JUIZ DE DIREITO1 DA VARA CÍVEL2 DO FORO' in text
    assert 'DA COMARCA DE CAMPINAS3 NO ESTADO DE SÃO PAULO' in text
    assert 'Constituição da República, o correto seria EXCELENTÍSSIMO SENHOR DOUTOR JUIZ FEDERAL.' in text
    assert 'CONTIDAS NO PROBLEMA, SEM A CRIAÇÃO DE FATOS, SOB PENA DE ANULAÇÃO DA PROVA.' in text
    assert 'relevantes ao julgamento da lide.' in text
