import hashlib
import hmac
import time
from base64 import b64encode
from typing import Any, Dict
from urllib.parse import urlparse

from hummingbot.connector.time_synchronizer import TimeSynchronizer
from hummingbot.core.web_assistant.auth import AuthBase
from hummingbot.core.web_assistant.connections.data_types import RESTRequest, WSRequest


class HitbtcAuth(AuthBase):
    def __init__(self, api_key: str, secret_key: str, time_provider: TimeSynchronizer):
        self.api_key = api_key
        self.secret_key = secret_key
        self.time_provider = time_provider

    async def rest_authenticate(self, request: RESTRequest) -> RESTRequest:
        """
        Adds the server time and the signature to the request, required for authenticated interactions. It also adds
        the required parameter in the request header.
        :param request: the request to be configured for authenticated interaction
        """

        headers = self.get_headers("GET", request.url, request.params)
        if request.headers is not None:
            headers.update(request.headers)
        request.headers = headers

        return request

    async def ws_authenticate(self, request: WSRequest) -> WSRequest:
        """
        This method is intended to configure a websocket request to be authenticated. Binance does not use this
        functionality
        """
        return request

    def get_headers(self,
                    method,
                    url,
                    params) -> Dict[str, Any]:
        """
        Generates authentication headers required by HitBTC
        :return: a dictionary of auth headers
        """
        url = urlparse(url)
        timestamp = str(int(time.time()))
        msg = method + timestamp + url.path
        if url.query != "":
            msg += "?" + url.query

        signature = hmac.new(self.secret_key.encode(), msg.encode(), hashlib.sha256).hexdigest()
        authstr = "HS256 " + b64encode(b':'.join((self.api_key.encode(), timestamp.encode(), signature.encode()))).decode().strip()
        headers = {
            "Authorization": authstr,
            "Content-Type": "application/x-www-form-urlencoded",
        }
        return headers
