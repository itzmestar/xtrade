import hmac
import time
import requests
from requests import Request, Session, Response
from urllib.parse import urlencode
import logging
from pprint import pformat
from django.conf import settings

BASE_URL_SPOT = 'https://testnet.binance.vision'
if settings.PROD:
    BASE_URL_SPOT = 'https://api.binance.com'

LOG = logging.getLogger(__name__)


class Binance:
    """
        class representing the Binance data exchanges.
    """

    def __init__(self, key, secret, test=False):
        # LOG.info("Binance object initializing...")
        self._api_key = key
        self._api_secret = secret
        self._session = Session()
        self.test = test

    def _request(self, method, path, sign, **kwargs):
        request = Request(method, path, **kwargs)
        if sign:
            self._sign_request(request)
        response = self._session.send(request.prepare())
        #LOG.debug(response.status_code)
        return response

    def _sign_request(self, request):
        request.headers['X-MBX-APIKEY'] = self._api_key
        signature_payload = urlencode(request.params)
        if request.data:
            signature_payload += urlencode(request.data)
        signature = hmac.new(self._api_secret.encode(), signature_payload.encode(), 'sha256').hexdigest()
        request.params['signature'] = signature

    @staticmethod
    def _process_response(response, expected=list()):
        try:
            return response.json()
        except Exception as e:
            #LOG.exception(e)
            return expected

    @staticmethod
    def _get_timestamp():
        timestamp = int(time.time() * 1000) - 3000
        return timestamp

    def _get(self, url, sign=False, params=None):
        response = self._request('GET', url, sign=sign, params=params)
        return self._process_response(response)

    def _post(self, url, sign=False, params=None):
        response = self._request('POST', url, sign=sign, params=params, data={})
        return self._process_response(response)

    def _delete(self, url, sign=False, params=None):
        response = self._request('DELETE', url, sign=sign, params=params)
        return self._process_response(response, expected=dict())

    def get_account_information(self):
        """
        API to call: GET /sapi/v1/capital/config/getall (HMAC SHA256)
        :return:
        """
        path = '/api/v3/account'

        params = {
            'recvWindow': 60000,
            'timestamp': self._get_timestamp()
        }

        data = self._get(BASE_URL_SPOT + path, sign=True, params=params)
        LOG.debug(pformat(data))
        return data

    @staticmethod
    def get_trading_symbols():
        """
        returns lists of currently trading symbol as tuple
        """
        path = '/api/v3/exchangeInfo'

        try:
            response = requests.get(BASE_URL_SPOT + path)
            if response.status_code != 200:
                #print(response.status_code)
                return list()
            data = response.json()
            symbols = data.get('symbols', [])
            symbols_list = [x['symbol'] for x in symbols if x['status'] == 'TRADING']
            symbols_list = [(x, x) for x in symbols_list]
            return symbols_list
        except Exception as e:
            LOG.exception(e)
            return list()

    def get_current_open_orders(self):
        path = '/api/v3/openOrders'
        params = {
            'recvWindow': 60000,
            'timestamp': self._get_timestamp()
        }

        data = self._get(BASE_URL_SPOT + path, sign=True, params=params)
        LOG.debug(pformat(data))
        return data

    def place_buy_order(self, **params):
        """
        API call POST /api/v3/order (HMAC SHA256)
        """
        path = '/api/v3/order/test'
        if settings.PROD:
            path = '/api/v3/order'

        params.update({
            'side': 'BUY',
            'recvWindow': 60000,
            'timestamp': self._get_timestamp()
        })

        if params.get('type') == 'MARKET':
            del params['price']
        else:
            params.update({'timeInForce': 'GTC'})
        #LOG.debug(pformat(params))
        data = self._post(BASE_URL_SPOT + path, sign=True, params=params)
        LOG.debug(pformat(data))
        return data

    def place_sell_order(self, **params):
        """
        API call POST /api/v3/order (HMAC SHA256)
        """
        path = '/api/v3/order/test'
        if settings.PROD:
            path = '/api/v3/order'

        params.update({
            'side': 'SELL',
            'recvWindow': 60000,
            'timestamp': self._get_timestamp()
        })

        if params.get('type') == 'MARKET':
            del params['price']
        else:
            params.update({'timeInForce': 'GTC'})
        # LOG.debug(pformat(params))
        data = self._post(BASE_URL_SPOT + path, sign=True, params=params)
        LOG.debug(pformat(data))
        return data

    def place_cancel_order(self, symbol, order_id):
        """
        API to call: DELETE /api/v3/order (HMAC SHA256)
        """
        path = '/api/v3/order'
        if settings.PROD:
            path = '/api/v3/order'

        params = {
            'symbol': symbol,
            'orderId': order_id,
            'recvWindow': 60000,
            'timestamp': self._get_timestamp()
             }

        data = self._delete(BASE_URL_SPOT + path, sign=True, params=params)
        LOG.debug(pformat(data))
        return data

    # ==== websocket ListenKey ==== #
    def create_listen_key(self):
        """
        API to call POST /api/v3/userDataStream
        """
        path = '/api/v3/userDataStream'

        data = self._post(BASE_URL_SPOT + path, sign=True)
        LOG.debug(pformat(data))
        return data

    def close_listen_key(self):
        """
        API to call DELETE /api/v3/userDataStream
        """
        path = '/api/v3/userDataStream'

        data = self._delete(BASE_URL_SPOT + path, sign=True)
        LOG.debug(pformat(data))
        return data

