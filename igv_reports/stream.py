import gzip
import io
import requests
from os.path import exists

def getstream(file):
    # TODO -- gcs

    if file.startswith('http://') or file.startswith('https://'):
        response = requests.get(file)
        status_code = response.status_code  # TODO Do something with this

        if file.endswith('.gz'):
            content = response.content
            text = gzip.decompress(content).decode('utf-8')
        else:
            text = response.text
        f = io.StringIO(text)
        return f

    elif file.endswith('.gz'):
        f = gzip.open(file, mode='rt')

    else:
        f = open(file, encoding='UTF-8')

    return f


# Check if the http or https URL resource exists.
# Used to probe for index files

def resource_exists(url):

    try:
        response = requests.get(url)
        status_code = response.status_code
        return status_code >= 200 and status_code < 400
    except:
        return False

