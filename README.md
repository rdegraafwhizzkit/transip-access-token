# Transip Access Token Python

## TODO
* A lot to make it more package style
* Add documentation in code

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
For development, you may add
```
pip install flake8
```
## Usage
Save private key in a file called pk.pem, then run:
```
TRANSIP_USERNAME=change-me \
  TRANSIP_PRIVATE_KEY_FILE=pk.pem \
  python main.py
```
which should result in
```
{
  "ping": "pong",
  "_links": [
    {
      "rel": "self",
      "link": "https://api.transip.nl/v6/api-test?page=1&pageSize=0"
    }
  ]
}
```