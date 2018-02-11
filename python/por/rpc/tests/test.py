from os import path
from xmlrpc.client import ServerProxy

BASE_FOLDER = path.dirname(path.abspath(__file__))
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
    assert text == '' \
                   '| P( "í PRÁTICA NA ADVOCACIA PROCESSUAL CIVIL\n\n' \
                   '9 Prof. Darlan Barroso\n' \
                   'CURSOS LUIZ FLÁVIO GOMES Prof Renato Montans\n\n \n\n' \
                   'Modelos práticos\n\n' \
                   '1. Petição inicial rito ordinário\n\n' \
                   'MODELO DE PETIÇÃO INICIAL — RITO ORDINÁRIO\n\n' \
                   'EXCELENTÍSSIMO SENHOR DOUTOR JUIZ DE DIREITO1 DA VARA CÍVEL2 DO FORO\n' \
                   'DA COMARCA DE CAMPINAS3 NO ESTADO DE SÃO PAULO\n\n' \
                   '(espaço — aproximadamente 10 cm4)\n\n' \
                   'NOME DO AUTORS, (nacionalidade), (estado civil), (profissão), portador do\n' \
                   'documento de identidade RG. (número) e inscrito no CPF sob o (número), domiciliado nesta\n' \
                   'Comarca de Campinas, onde reside na rua (endereço completo), vem, por seu procurador\n' \
                   '(instrumento de mandato incluso — doc. n.º 1), propor a presente AÇÃO PELO\n' \
                   'PROCEDIMENTO ORDINÁRIO com PEDIDO DE ANTECIPAÇÃO DOS EFEITOS DA\n' \
                   'TUTELA, em face de NOME DA PARTE RÉ, sociedade inscrita no CNPF sob o n.º (número),\n' \
                   'com sede na Comarca de São Bernardo do Campo, rua (endereço completo), pelos motivos de\n\n' \
                   'fato e de direito a seguir expostos.\n' \
                   'I — DOS FATOS6\n\n' \
                   'O Autor, em abril de 2003, adquiriu da Ré veículo novo (descrição do bem) de sua\n\n' \
                   'própria fabricação.\n\n' \
                   'Ocorre que, quando da realização de uma viagem para a cidade vizinha, em\n' \
                   '(data), enquanto trafegava pela rodovia , o Autor foi obrigado a frear o veículo para não\n\n' \
                   'bater em um caminhão que estava na sua frente (Boletim de Ocorrência incluso, doc. n.º 2).\n\n \n\n' \
                   '1 Para magistrado da Justiça Estadual. Caso a competência fosse da Justiça Federal, conforme estabelece 0 art. 109 da\n' \
                   'Constituição da República, o correto seria EXCELENTÍSSIMO SENHOR DOUTOR JUIZ FEDERAL.\n\n' \
                   '2 Indicação da competência funciona].\n\n' \
                   '3 Indicação da competência territorial. Em se tratando de Justiça Federal o termo comarca é substituído por SUBSEÇÃO\n' \
                   'JUDICIÁRIA OU SEÇÃO JUDICIÁRIA.\n\n' \
                   'No modelo em questão a competência encontra fundamento no art. 101, I do Código de Defesa do Consumidor.\n\n' \
                   '4 Tal espaço se presta para, caso seja necessário, O juiz escrever sua decisão interlocutória ou despacho.\n\n' \
                   '5 EM CASO DE EXAMES E CONCURSOS O CANDIDATO DEVERÁ UTILIZAR-SE DOS NOMES E INFORMAÇOES\n' \
                   'CONTIDAS NO PROBLEMA, SEM A CRIAÇÃO DE FATOS, SOB PENA DE ANULAÇÃO DA PROVA.\n\n' \
                   '6 A narração que se apresenta nesta petição é meramente genérica, podendo, no caso concreto, haver especificação dos fatos\n' \
                   'relevantes ao julgamento da lide.\n\x0c'
