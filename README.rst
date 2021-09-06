..................................
aiowc - Asynchronous Python Client
..................................

Asynchronous Python wrapper for WooCommerce REST API.

Gives you asynchronous access to the REST API. 
Based on `aiohttp <https://github.com/aio-libs/aiohttp>`_ and `wc-api-python <https://github.com/woocommerce/wc-api-python>`_.

**PRs are highly appreciated!**

Installation
~~~~~~~~~~~~
``pip install aiowc`` or ``python3 -m pip install aiowc``

Getting started
~~~~~~~~~~~~~~~
* `Generate API credentials <http://woocommerce.github.io/woocommerce-rest-api-docs/#rest-api-keys>`_

* Import aiowc:

.. code-block:: python

    from aiowc import API, APISession

* Set API parameters:
    
.. code-block:: python

    wcapi = API(
        url="https://example.com",
        consumer_key="ck_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        consumer_secret="cs_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        version="wc/v3",
        timeout=30
    )

* Make request with aiohttp session:

.. code-block:: python

    async def main():
        async with APISession(wcapi) as session:
            res = await session.get('products/categories', params={'per_page': 5})
            json = await res.json()
            print(json)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

Options and request types:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fully compatible with `wc-api-python <https://github.com/woocommerce/wc-api-python>`_ 