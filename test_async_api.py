""" API Tests
    Same as sync woocommerce version except using pytest instead of unittest
"""
import json
import pytest

import aiohttp
import asyncio
from aioresponses import aioresponses
from aiowc import API as aioapi
from aiowc import APISession, oauth


class MockResponse:
    def __init__(self, text, status):
        self._text = text
        self.status = status

    async def text(self):
        return self._text

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


@pytest.fixture()
def make_api():
    return aioapi(
        url="https://woo.test",
        consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    )


@pytest.fixture()
def make_api_non_ssl():
    return aioapi(
        url="http://woo.test",
        consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    )


def test_version(make_api):
    """ Test default version """
    assert make_api.version == "wc/v3"


def test_non_ssl(make_api_non_ssl):
    """ Test non-ssl """
    assert make_api_non_ssl.is_ssl == False


def test_with_ssl(make_api):
    """ Test ssl """
    assert make_api.is_ssl == True


def test_with_timeout():
    """ Test timeout """
    api = aioapi(
        url="https://woo.test",
        consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        timeout=10,
    )
    assert api.timeout == 10

    async def make_session():
        async with APISession(api) as session:
            res = await session.get("products")
            return res

    loop = asyncio.get_event_loop()
    with aioresponses() as m:     
        m.get(api.url + "/wp-json/wc/v3" + "/products", status=200, payload=dict(content="OK"))
        resp = loop.run_until_complete(make_session())
        assert resp.status == 200


def test_get(make_api):
    """ Test GET requests """
    api = make_api

    async def make_session():
        async with APISession(api) as session:
            res = await session.get("products")
            return res

    loop = asyncio.get_event_loop()
    with aioresponses() as m:     
        m.get(api.url + "/wp-json/wc/v3" + "/products", status=200, payload=dict(content="OK"))
        resp = loop.run_until_complete(make_session())
        assert resp.status == 200


def test_get_with_parameters(make_api):
    """ Test GET requests w/ url params """
    api = make_api
    
    async def make_session():
        async with APISession(api) as session:
            res = await session.get("products", params={
                              "per_page": 10, "page": 1, "offset": 0})
            return res

    loop = asyncio.get_event_loop()
    with aioresponses() as m:     
        m.get(api.url + "/wp-json/wc/v3" + "/products" + "?offset=0&page=1&per_page=10",
            status=200, payload=dict(content="OK"))
        resp = loop.run_until_complete(make_session())
        assert resp.status == 200


def test_get_with_requests_kwargs(make_api):
    """ Test GET requests w/ optional requests-module kwargs """
    api = make_api

    async def make_session():
        async with APISession(api) as session:
            res = await session.get("products", allow_redirects=True)
            return res

    loop = asyncio.get_event_loop()

    with aioresponses() as m:     
        m.get(api.url + "/wp-json/wc/v3" + "/products", status=200, payload=dict(content="OK"))
        resp = loop.run_until_complete(make_session())
        assert resp.status == 200


def test_post(make_api):
    """ Test POST requests """
    api = make_api

    async def make_session():
        async with APISession(api) as session:
            res = await session.post("products", {})
            return res

    loop = asyncio.get_event_loop()
    with aioresponses() as m:     
        m.post(api.url + "/wp-json/wc/v3" + "/products", status=201, payload=dict(content="OK"))
        resp = loop.run_until_complete(make_session())
        assert resp.status == 201


def test_put(make_api):
    """ Test PUT requests """
    api = make_api

    async def make_session():
        async with APISession(api) as session:
            res = await session.put("products", {})
            return res

    loop = asyncio.get_event_loop()
    with aioresponses() as m:     
        m.put(api.url + "/wp-json/wc/v3" + "/products", status=200, payload=dict(content="OK"))
        resp = loop.run_until_complete(make_session())
        assert resp.status == 200


def test_delete(make_api):
    """ Test DELETE requests """
    api = make_api

    async def make_session():
        async with APISession(api) as session:
            res = await session.delete("products")
            return res

    loop = asyncio.get_event_loop()
    with aioresponses() as m:     
        m.delete(api.url + "/wp-json/wc/v3" + "/products", status=200, payload=dict(content="OK"))
        resp = loop.run_until_complete(make_session())
        assert resp.status == 200


def test_oauth_sorted_params():
    """ Test order of parameters for OAuth signature """
    def check_sorted(keys, expected):
        params = oauth.OrderedDict()
        for key in keys:
            params[key] = ''

        ordered = list(oauth.OAuth.sorted_params(params).keys())
        assert ordered == expected

    check_sorted(['a', 'b'], ['a', 'b'])
    check_sorted(['b', 'a'], ['a', 'b'])
    check_sorted(['a', 'b[a]', 'b[b]', 'b[c]', 'c'],
                 ['a', 'b[a]', 'b[b]', 'b[c]', 'c'])
    check_sorted(['a', 'b[c]', 'b[a]', 'b[b]', 'c'],
                 ['a', 'b[c]', 'b[a]', 'b[b]', 'c'])
    check_sorted(['d', 'b[c]', 'b[a]', 'b[b]', 'c'],
                 ['b[c]', 'b[a]', 'b[b]', 'c', 'd'])
    check_sorted(['a1', 'b[c]', 'b[a]', 'b[b]', 'a2'],
                 ['a1', 'a2', 'b[c]', 'b[a]', 'b[b]'])
