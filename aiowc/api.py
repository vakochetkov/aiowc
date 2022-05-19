import asyncio
import aiohttp
import json
from time import time
from urllib.parse import urlencode
from aiowc.params import SessionParams, RequestParams 
from aiowc.oauth import OAuth


class API(object):
    """ API class, it tries to be compatible with the synchronous version
        Consists parameters for APISession """
    def __init__(self, url, consumer_key, consumer_secret, **kwargs):
        self.VERSION = 1.1

        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.wp_api = kwargs.get("wp_api", True)
        self.version = kwargs.get("version", "wc/v3")
        self.is_ssl = self.__is_ssl()
        self.timeout = kwargs.get("timeout", 30)
        self.verify_ssl = kwargs.get("verify_ssl", True)
        self.user_agent = kwargs.get("user_agent", f"WooCommerce-Python-aiowc/{self.VERSION}")
        self.query_string_auth = kwargs.get("query_string_auth", False)

        self.session_params = SessionParams(
            self.url,
            self.consumer_key,
            self.consumer_secret,
            self.version,
            self.wp_api,
            self.is_ssl,
            self.timeout,
            self.verify_ssl,
            self.user_agent,
            self.query_string_auth
        )


    def __is_ssl(self):
        """ Check if url use HTTPS """
        return self.url.startswith("https")


    def get_params(self) -> SessionParams:
        return self.session_params


class APISession(object):
    """ Holds aiohttp session for its lifetime and wraps different types of request """
    def __init__(self, api: API):
        self.params = api.get_params()


    async def __aenter__(self):
        self.session = aiohttp.ClientSession(json_serialize=json.dumps)
        return self


    async def __aexit__(self, *err):
        await self.session.close()
        self.session = None


    def __get_url(self, endpoint):
        """ Get URL for requests """
        url = self.params.url
        api = "wc-api"

        if url.endswith("/") is False:
            url = f"{url}/"

        if self.params.wp_api:
            api = "wp-json"

        return f"{url}{api}/{self.params.version}/{endpoint}"


    def __build_headers(self, request: RequestParams) -> dict:
        headers = {
                "user-agent": f"{self.params.user_agent}",
                "accept": "application/json"
        }
        if request.use_data:
            headers["content-type"] = "application/json;charset=utf-8"
        return headers


    def __get_oauth_url(self, url, method, **kwargs):
        """ Generate oAuth1.0a URL """
        oauth = OAuth(
            url=url,
            consumer_key=self.params.consumer_key,
            consumer_secret=self.params.consumer_secret,
            version=self.params.version,
            method=method,
            oauth_timestamp=kwargs.get("oauth_timestamp", int(time()))
        )

        return oauth.get_oauth_url()


    async def __request(self, method, endpoint, data, params=None, **kwargs):
        if params is None:
            params = {}

        url = self.__get_url(endpoint)
        auth = None

        if self.params.is_ssl is True and self.params.query_string_auth is False:
            auth = aiohttp.BasicAuth(self.params.consumer_key, self.params.consumer_secret)
        elif self.params.is_ssl is True and self.params.query_string_auth is True:
            params.update({
                "consumer_key": self.params.consumer_key,
                "consumer_secret": self.params.consumer_secret
            })
        else:
            encoded_params = urlencode(params)
            url = f"{url}?{encoded_params}"
            url = self.__get_oauth_url(url, method, **kwargs)

        if data is not None:
            use_data = True
            data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        else:
            use_data = False

        request = RequestParams(
            method, endpoint, data, use_data, params
        )

        return await self.session.request(
            method=request.method,
            url=url,
            auth=auth,
            timeout=aiohttp.ClientTimeout(self.params.timeout),
            ssl=self.params.verify_ssl,
            headers=self.__build_headers(request),
            data=request.data,
            params=request.params,
            **kwargs
        ) 


    async def get(self, endpoint, **kwargs):
        """ GET requests """
        return await self.__request("GET", endpoint, None, **kwargs)


    async def post(self, endpoint, data, **kwargs):
        """ POST requests """
        return await self.__request("POST", endpoint, data, **kwargs)


    async def put(self, endpoint, data, **kwargs):
        """ PUT requests """
        return await self.__request("PUT", endpoint, data, **kwargs)


    async def delete(self, endpoint, **kwargs):
        """ DELETE requests """
        return await self.__request("DELETE", endpoint, None, **kwargs)


    async def options(self, endpoint, **kwargs):
        """ OPTIONS requests """
        return await self.__request("OPTIONS", endpoint, None, **kwargs)
