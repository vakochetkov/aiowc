import asyncio
import aiohttp
from dataclasses import dataclass


@dataclass
class SessionParams():
    url: str = None
    consumer_key: str = None
    consumer_secret: str = None
    version: str  = "wc/v3"
    wp_api: bool  = True 
    timeout: int  = 30 # in seconds
    verify_ssl: bool = True
    user_agent: str = None


@dataclass
class RequestParams():
    method: str = None
    endpoint: str = None
    data: aiohttp.FormData = None
    use_data: bool = False
    params: dict = None
                