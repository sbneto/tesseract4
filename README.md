# tesseract4


# Usage

Run the container with the following command:

```bash
docker run --rm -p "8000:8000" sbneto/tesseract4:python-por-rpc
```

And connect to the container running python XMLRPC server to run remote calls.

```python
from xmlrpc.client import ServerProxy, Binary

proxy = ServerProxy("http://localhost:8000/", use_builtin_types=True)

pdf_file = Binary(open("MY_PDF_FILE.pdf", "rb").read())
text = str(proxy.tesseract(pdf_file), 'utf-8')
print(text)
```
