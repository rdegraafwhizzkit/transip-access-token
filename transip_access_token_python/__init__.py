from base64 import b64encode
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA512
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from time import time
import json
import requests


class TransIPAPI:
    ENDPOINT = 'api.transip.nl'
    VERSION = 'v6'


class TransIPAccessToken(TransIPAPI):
    class TransIPException(Exception):
        pass

    def __init__(
            self,
            login: str, private_key: str, read_only: bool = False, expiration_time: str = '30 minutes',
            global_key: bool = False, label: str = ''
    ):
        self._login = login
        self._read_only = read_only
        self._expiration_time = expiration_time
        self._global_key = global_key
        self._label = label
        self._private_key = private_key

    def create_token(self) -> str:
        request_body = self._get_request_body()
        return self._perform_request(
            request_body,
            self._create_signature(request_body)
        )

    def _get_request_body(self) -> dict:
        return {
            'login': self._login,
            'nonce': hex(int(time() * 1000000))[2:],
            'read_only': self._read_only,
            'expiration_time': self._expiration_time,
            'label': self._label,
            'global_key': self._global_key
        }

    def _create_signature(self, request_body: str | dict) -> str:
        request_body = json.dumps(request_body) if isinstance(request_body, dict) else request_body

        return b64encode(load_pem_private_key(
            self._private_key.encode('utf-8'),
            None
        ).sign(
            request_body.encode('utf-8'),
            padding=PKCS1v15(),
            algorithm=SHA512()
        )
        ).decode('utf-8')

    def _perform_request(self, request_body: dict, signature: str) -> str:
        result = requests.post(
            url=f'https://{self.ENDPOINT}/{self.VERSION}/auth',
            json=request_body,
            headers={
                'Content-Type': 'application/json',
                'Signature': signature
            }
        )
        if not result.ok:
            raise TransIPAccessToken.TransIPException(result.text)

        return result.json()['token']
