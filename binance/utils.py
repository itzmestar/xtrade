import hmac
import time
import requests
from requests import Request, Session, Response
from urllib.parse import urlencode


class Binance:
    """
        class representing the Binance data exchanges.
    """

    def __init__(self, key, secret, test=False):
        # LOG.info("Binance object initializing...")
        self._api_key = key
        self._api_secret = secret
        self._session = Session()
        self._base_url_futures_coin = 'https://dapi.binance.com/'
        self._base_url_spot = 'https://api.binance.com/'
        self._base_url_futures_usdt = 'https://fapi.binance.com/'
        self.test = test
        if test:
            self._base_url_spot = 'https://testnet.binance.vision/'

    def _get(self, url, sign=False, params=None):
        return self._request('GET', url, sign=sign, params=params)

    def _request(self, method, path, sign, **kwargs):
        request = Request(method, path, **kwargs)
        if sign:
            self._sign_request(request)
        response = self._session.send(request.prepare())
        #LOG.debug(response.status_code)
        return self._process_response(response)

    def _sign_request(self, request):
        request.headers['X-MBX-APIKEY'] = self._api_key
        signature_payload = urlencode(request.params)
        if request.data:
            signature_payload += urlencode(request.data)
        signature = hmac.new(self._api_secret.encode(), signature_payload.encode(), 'sha256').hexdigest()
        request.params['signature'] = signature

    @staticmethod
    def _process_response(response):
        try:
            if response.status_code != 200:
                #LOG.error(response.content)
                return list()
            return response.json()
        except Exception as e:
            #LOG.exception(e)
            return list()

    @staticmethod
    def _get_timestamp():
        timestamp = int(time.time() * 1000) - 3000
        return timestamp

    def get_account_balance_spot(self):
        """
        API to call: GET /sapi/v1/capital/config/getall (HMAC SHA256)
        :return:
        """
        #LOG.info("Started")
        path = 'sapi/v1/capital/config/getall'

        params = {
            'recvWindow': 60000,
            'timestamp': self._get_timestamp()
        }

        data = self._get(self._base_url_spot + path, sign=True, params=params)
        #LOG.debug(data)
        return data

    def get_trading_symbols(self):
        """
        returns lists of currently trading symbol
        """
        path = '/api/v3/exchangeInfo'

        try:
            response = requests.get(self._base_url_spot + path)
            if response.status_code != 200:
                # LOG.error(response.content)
                return list()
            data = response.json()
            symbols = data.get('symbols', [])
            symbols_list = [x['symbol'] for x in symbols if x['status'] == 'TRADING']
            return symbols_list
        except:
            return list()
