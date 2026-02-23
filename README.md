# Transip Access Token Python

## TODO
* A lot to make it more package style

## Setup
```
deactivate > /dev/null 2>&1 | :
rm -rf .venv

python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install pip-tools
pip-compile requirements.in 
pip install -r requirements.txt 
```

## Usage
Save private key in a file called pk.pem, then run:
```
import requests
from transip_access_token import TransIPAPI, TransIPAccessToken

if '__main__' == __name__:
    token = TransIPAccessToken(
        '<your username>',
        private_key=''.join(open('pk.pem').readlines()),
        global_key=True
    ).create_token()

    print(requests.get(
        url=f'https://{TransIPAPI.ENDPOINT}/{TransIPAPI.VERSION}/invoices',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
    ).text)
```