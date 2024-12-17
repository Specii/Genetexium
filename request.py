from requests import get, post, RequestException
from requests.auth import HTTPProxyAuth


class Request:
    def __init__(self):
        self.retry_attempts = 3

    def __request(self, url, method, proxy, ssl, timeout=10, json=None):
        if proxy is None:
            proxy = {}

        protocol = proxy.get('protocol')
        host = proxy.get('host')
        port = proxy.get('port')
        username = proxy.get('username')
        password = proxy.get('password')

        try:
            url_protocol = 'https' if ssl else 'http'
            auth = HTTPProxyAuth(username=username, password=password) if username and password else None
            proxy_configuration = {protocol: f'{url_protocol}://{host}:{port}'}

            for attempt in range(self.retry_attempts):
                try:
                    response = (
                        get(url, proxies=proxy_configuration, auth=auth, verify=ssl, timeout=timeout)
                        if 'get' in method
                        else post(url, proxies=proxy_configuration, auth=auth, verify=ssl, timeout=timeout, json=json)
                    )

                    if response.status_code == 200:
                        return response

                except RequestException as req_exc:
                    # print(f'Attempt {attempt + 1}: RequestException for URL {url}. Error: {req_exc}')

                    continue

            print(f'Request to {url} failed')
            return False
        except Exception as e:
            raise e

    def get(self, url, proxy=None, ssl=False, timeout=10):
        return self.__request(url=url, method='get', proxy=proxy, ssl=ssl, timeout=timeout)

    def post(self, url, proxy=None, ssl=False, json=None, timeout=10):
        return self.__request(url=url, method='post', proxy=proxy, ssl=ssl, json=json, timeout=timeout)
