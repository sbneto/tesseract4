from xmlrpc.client import ServerProxy

proxy = ServerProxy('http://localhost:8000/', use_builtin_types=True)

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


def test_convert_simple_phone_number():
    with open('number.gif', 'rb') as f:
        proxy.convert(f.read(), small_image_convert)


def test_tesseract_simple_phone_number():
    with open('number.gif', 'rb') as f:
        text = str(proxy.tesseract(f.read(), {'convert': small_image_convert}), 'utf-8')
        assert text.strip() == '(12) 99738 5318'
