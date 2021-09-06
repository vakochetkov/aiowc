import os
import sys

from setuptools import setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# check python version
MINIMAL_PY_VERSION = (3, 7)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('aiowc works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


setup(
    name='aiowc',                    
    version='1.0',                          
    description='Asynchronous Python wrapper for WooCommerce REST API',  
    author="Vladislav Kochetkov",    
    url='https://github.com/vakochetkov/aiowc',  
    license="MIT License",    
    packages=[
        "aiowc"
    ],
    include_package_data=False,
    platforms=['any'],
    install_requires=[
        "aiohttp>=3.7.4"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords='python woocommerce rest api',
    project_urls={
        'Source': 'https://github.com/vakochetkov/aiowc',
        'Tracker': 'https://github.com/vakochetkov/aiowc/issues',
    },            
)  
