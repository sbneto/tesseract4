import logging
import subprocess
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import Binary

logger = logging.getLogger(__name__)


def run_subprocess(command, input_data, **kwargs):
    process = subprocess.run(
        command,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **kwargs
    )
    result = {
        'returncode': process.returncode,
        'stdout': process.stdout,
        'stderr': process.stderr,
    }
    return result


def n_pages(pdf_file):
    try:
        logger.debug('Extraction PDF number of pages...')
        data = run_subprocess(['pdfinfo', '-'], pdf_file)
        data = str(data['stdout'], 'utf-8').split('\n')
        for line in data:
            if 'Pages' in line:
                _, _, number = line.partition(':')
                number = int(number.strip().rstrip())
                break
        return number
    except RuntimeError:
        raise RuntimeError('Error extracting PDF number of pages...')


def tesseract(pdf_file, limit_pages=None):
    try:
        logger.debug('Extraction PDF information via tesseract...')
        limit_pages = limit_pages or n_pages(pdf_file.data)
        full_text = b''
        for i in range(0, limit_pages):
            logger.debug('Processing page {} of {}...'.format(i, limit_pages))
            page_arg = '-[{}]'.format(i)
            tiff_image = run_subprocess(
                [
                    'convert', '-density', '300', page_arg, '-depth', '8',
                    '-strip', '-background', 'white', '-alpha', 'off', '-'
                ],
                pdf_file.data,
            )
            text = run_subprocess(['tesseract', '-', '-', '-l', 'por', '--psm', '1', '--oem', '2'], tiff_image['stdout'])
            full_text += text['stdout']
        return Binary(full_text)
    except RuntimeError:
        raise RuntimeError('Problem executing tesseract...')


if __name__ == '__main__':
    server = SimpleXMLRPCServer(("0.0.0.0", 8000))
    print("Listening on port 8000...")
    server.register_function(tesseract)
    server.serve_forever()
