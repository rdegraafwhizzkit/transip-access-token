import os
import json
import requests
import logging
from transip_access_token_python import TransIPAPI, TransIPAccessToken

logging.basicConfig(level=logging.INFO)

if '__main__' == __name__:
    token = TransIPAccessToken(
        os.environ.get('TRANSIP_USERNAME'),
        private_key=''.join(open(os.environ.get('TRANSIP_PRIVATE_KEY_FILE')).readlines()),
        global_key=True
    ).create_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    print(json.dumps(requests.get(
        url=f'https://{TransIPAPI.ENDPOINT}/{TransIPAPI.VERSION}/api-test',
        headers=headers
    ).json(), indent=2))
