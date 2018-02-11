import logging
import subprocess
from xmlrpc.server import SimpleXMLRPCServer

import magic

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


def n_pages_pdf(pdf_file):
    logger.debug('Extraction PDF number of pages...')
    data = run_subprocess(['pdfinfo', '-'], pdf_file)
    data = str(data['stdout'], 'utf-8').split('\n')
    for line in data:
        if 'Pages' in line:
            _, _, number = line.partition(':')
            number = int(number.strip().rstrip())
            break
    return number


class RPCFunctions:
    def _tesseract(self, file_data, options=None):
        options = options or ['-l', 'por', '--psm', '3', '--oem', '0']
        command = ['tesseract', '-', '-'] + options
        return run_subprocess(command, file_data)['stdout']

    def pdf_as_images(self, file_data, limit_pages=None):
        images = []
        limit_pages = limit_pages or n_pages_pdf(file_data)
        options = {
            'input_options': ['-density', '400'],
            'output_options': [
                '-depth', '8',
                '-strip',
                '-alpha', 'off',
                '-colorspace', 'gray',
                '-type', 'grayscale',
                '-contrast-stretch', '0',
                '-fill', 'white',
                '-opaque', 'none',
                '-background', 'white',
                '-deskew', '40%',
                '-trim',
                '+repage',
                '-compose', 'over',
                '-bordercolor', 'white',
                '-border', '400',
            ],
            'output': 'tiff:-',
        }
        for i in range(0, limit_pages):
            options['input'] = '-[{}]'.format(i)
            images.append(self.convert(file_data, options))
        return images

    def _prepare_single_file(self, file_data, **kwargs):
        file_mime = magic.from_buffer(file_data, mime=True)
        if file_mime == 'application/pdf':
            return self.pdf_as_images(file_data, kwargs.get('limit_pages'))
        else:
            # should process any "convert" options here
            return [self.convert(file_data, kwargs)]

    def _prepare_images(self, raw_data, **kwargs):
        if isinstance(raw_data, list):
            images = [image for single_file in raw_data for image in self._prepare_single_file(single_file, **kwargs)]
        else:
            images = self._prepare_single_file(raw_data, **kwargs)
        return images

    def tesseract(self, raw_data, options={}):
        logger.debug('Extraction PDF information via tesseract...')
        images = self._prepare_images(raw_data, **options.get('convert', {}))
        full_text = b''
        for image in images:
            full_text += self._tesseract(image, options.get('tesseract', []))
        return full_text

    def convert(self, raw_data, options={}):
        input_options = options.get('input_options', [])
        _input = options.get('input', '-')
        output_options = options.get('output_options', [])
        output = options.get('output', '-')
        converted_image = run_subprocess(
            ['convert'] + input_options + [_input] + output_options + [output],
            raw_data
        )
        return converted_image['stdout']


if __name__ == '__main__':
    with SimpleXMLRPCServer(("0.0.0.0", 8000), use_builtin_types=True) as server:
        print("Listening on port 8000...")
        server.register_instance(RPCFunctions())
        server.serve_forever()
