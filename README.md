# tesseract4

[![Build Status](https://travis-ci.org/sbneto/tesseract4.svg?branch=master)](https://travis-ci.org/sbneto/tesseract4)

# Usage

Run the container with the following command:

```bash
docker run --rm -d -p "8000:8000" sbneto/tesseract4:python-por-rpc
```

And connect to the container running python XMLRPC server to run remote calls.

```python
from xmlrpc.client import ServerProxy

# Connect to the RPC server
proxy = ServerProxy("http://localhost:8000/", use_builtin_types=True)

# Read file data as bytes
with open('test.pdf', 'rb') as f:
    data = f.read()
    
# Perform the remote call
text = str(proxy.tesseract(data), 'utf-8')

# Check the results =]
print(text)
```
