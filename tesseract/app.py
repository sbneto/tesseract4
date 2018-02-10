import logging
import subprocess
from xmlrpc.server import SimpleXMLRPCServer

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
        'stdout': str(process.stdout, 'utf-8'),
        'stderr': str(process.stderr, 'utf-8'),
    }
    return result


def tesseract(pdf_file, limit_pages):
    try:
        logger.debug('Extraction PDF information via tesseract...')
        full_text = ''
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
            text = run_subprocess(['tesseract', '-', '-', '-l=por', '--psm=1'], tiff_image, raw=True)
            full_text += str(text, 'utf-8')
        return full_text
    except RuntimeError:
        raise RuntimeError('Problem executing tesseract...')


if __name__ == '__main__':
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(tesseract)
    server.serve_forever()
