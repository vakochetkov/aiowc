import asyncio
import aiohttp
import json

from aiowc.params import SessionParams, RequestParams 


class API(object):
    """ API class, it tries to be compatible with the synchronous version
        Consists parameters for APISession """
    def __init__(self, url, consumer_key, consumer_secret, **kwargs):
        self.VERSION = 1.0

        self.url = url
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.wp_api = kwargs.get("wp_api", True)
        self.version = kwargs.get("version", "wc/v3")
        self.is_ssl = self.__is_ssl()
        self.timeout = kwargs.get("timeout", 30)
        self.verify_ssl = kwargs.get("verify_ssl", True)
        self.user_agent = kwargs.get("user_agent", f"WooCommerce-Python-aiowc/{self.VERSION}")

        self.session_params = SessionParams(
            self.url,
            self.consumer_key,
            self.consumer_secret,
            self.version,
            self.wp_api,
            self.timeout,
            self.verify_ssl,
            self.user_agent
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


    def __build_full_url(self, request: RequestParams) -> str:
        wp_api = "wp-json" if self.params.wp_api else "wc-api"
        return f"{self.params.url}/{wp_api}/{self.params.version}/{request.endpoint}"


    def __build_headers(self, request: RequestParams) -> dict:
        headers = {
                "user-agent": f"{self.params.user_agent}",
                "accept": "application/json"
        }
        if request.use_data:
            data = json.dumps(request.data, ensure_ascii=True).encode('utf-8')
            headers["content-type"] = "application/json;charset=utf-8"
        return headers

            
    async def __request(self, method, endpoint, data, params=None):
        if data is not None:
            use_data = True
        else:
            use_data = False

        request = RequestParams(
            method, endpoint, data, use_data, params
        )

        return await self.session.request(
            method=request.method,
            url=self.__build_full_url(request),
            auth=aiohttp.BasicAuth(self.params.consumer_key, self.params.consumer_secret),
            timeout=aiohttp.ClientTimeout(self.params.timeout),
            ssl=self.params.verify_ssl,
            headers=self.__build_headers(request),
            data=request.data,
            params=request.params
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
