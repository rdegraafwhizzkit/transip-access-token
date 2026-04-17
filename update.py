import requests
import os
import logging
from transip_access_token_python import TransIPAccessToken, TransIPAPI

logging.basicConfig(level=logging.INFO)

if '__main__' == __name__:
    token = TransIPAccessToken(
        os.environ['TRANSIP_USERNAME'],
        private_key=''.join(open(os.environ['TRANSIP_PRIVATE_KEY_FILE']).readlines()),
        global_key=True
    ).create_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    ip = requests.get(url='https://ip.me').text.strip()

    for domain in requests.get(
            url=f'https://{TransIPAPI.ENDPOINT}/{TransIPAPI.VERSION}/domains',
            headers=headers
    ).json()['domains']:
        domain_name = domain['name']
        for dns_entry in requests.get(
                url=f'https://{TransIPAPI.ENDPOINT}/{TransIPAPI.VERSION}/domains/{domain_name}/dns',
                headers=headers
        ).json()['dnsEntries']:
            if dns_entry['type'] != 'A':
                continue

            dns_entry_name = dns_entry['name']
            fqdn = f'{dns_entry_name}.{domain_name}' if '@' != dns_entry_name else domain_name

            if dns_entry['content'] == ip:
                logging.info(f'No update needed for {fqdn}')
                continue

            logging.info(f'Updating {fqdn}')
            response = requests.patch(
                url=f'https://{TransIPAPI.ENDPOINT}/{TransIPAPI.VERSION}/domains/{domain_name}/dns',
                headers=headers,
                json={
                    'dnsEntry': {
                        'name': dns_entry_name,
                        'expire': dns_entry['expire'],
                        'type': 'A',
                        'content': ip
                    }
                }
            )

            if not response.ok:
                logging.error(response.text)
