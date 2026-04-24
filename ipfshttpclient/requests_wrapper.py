# type: ignore
"""Exposes the full ``requests`` HTTP library API, while adding an extra
``family`` parameter to all HTTP request operations that may be used to restrict
the address family used when resolving a domain-name to an IP address.
"""
import socket
import urllib.parse

import requests
import requests.adapters
import urllib3
import urllib3.connection
import urllib3.exceptions
import urllib3.poolmanager
import urllib3.util.connection

AF2NAME = {
	int(socket.AF_INET):  "ip4",
	int(socket.AF_INET6): "ip6",
}
if hasattr(socket, "AF_UNIX"):
	AF2NAME[int(socket.AF_UNIX)] = "unix"
NAME2AF = {name: af for af, name in AF2NAME.items()}


# This function is copied from urllib3/util/connection.py (that in turn copied
# it from socket.py in the Python 2.7 standard library test suite) and accepts
# an extra `family` parameter that specifies the allowed address families for
# name resolution.
#
# The entire remainder of this file after this only exists to ensure that this
# `family` parameter is exposed all the way up to request's `Session` interface,
# storing it as part of the URL scheme while traversing most of the layers.
def create_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                      source_address=None, socket_options=None,
                      family=socket.AF_UNSPEC):
	pass


# Override the `urllib3` low-level Connection objects that do the actual work
# of speaking HTTP
def _kw_scheme_to_family(kw, base_scheme):
	pass


class ConnectionOverrideMixin:
	def _new_conn(self):
		pass


class HTTPConnection(ConnectionOverrideMixin, urllib3.connection.HTTPConnection):
	def __init__(self, *args, **kw):
		self.family = _kw_scheme_to_family(kw, "http")
		super().__init__(*args, **kw)


class HTTPSConnection(ConnectionOverrideMixin, urllib3.connection.HTTPSConnection):
	def __init__(self, *args, **kw):
		self.family = _kw_scheme_to_family(kw, "https")
		super().__init__(*args, **kw)


# Override the higher-level `urllib3` ConnectionPool objects that instantiate
# one or more Connection objects and dispatch work between them
class HTTPConnectionPool(urllib3.HTTPConnectionPool):
	ConnectionCls = HTTPConnection


class HTTPSConnectionPool(urllib3.HTTPSConnectionPool):
	ConnectionCls = HTTPSConnection


# Override the highest-level `urllib3` PoolManager to also properly support the
# address family extended scheme values in URLs and pass these scheme values on
# to the individual ConnectionPool objects
class PoolManager(urllib3.PoolManager):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# Additionally to adding our variant of the usual HTTP and HTTPS
		# pool classes, also add these for some variants of the default schemes
		# that are limited to some specific address family only
		self.pool_classes_by_scheme = {}
		for scheme, ConnectionPool in (("http", HTTPConnectionPool), ("https", HTTPSConnectionPool)):
			self.pool_classes_by_scheme[scheme] = ConnectionPool
			for name in AF2NAME.values():
				self.pool_classes_by_scheme["{0}+{1}".format(scheme, name)] = ConnectionPool
				self.key_fn_by_scheme["{0}+{1}".format(scheme, name)] = self.key_fn_by_scheme[scheme]

	# These next two are only required to ensure that our custom `scheme` values
	# will be passed down to the `*ConnectionPool`s and finally to the actual
	# `*Connection`s as parameter
	def _new_pool(self, scheme, host, port, request_context=None):
		# Copied from `urllib3` to *not* surpress the `scheme` parameter
		pass

	def connection_from_pool_key(self, pool_key, request_context=None):
		# Copied from `urllib3` so that we continue to ensure that this will
		# call `_new_pool`
		pass


# Override the lower-level `requests` adapter that invokes the `urllib3`
# PoolManager objects
class HTTPAdapter(requests.adapters.HTTPAdapter):
	def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
		# save these values for pickling (copied from `requests`)
		pass


# Override the highest-level `requests` Session object to accept the `family`
# parameter for any request and encode its value as part of the URL scheme
# when passing it down to the adapter
class Session(requests.Session):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.family = socket.AF_UNSPEC

		# Additionally to mounting our variant of the usual HTTP and HTTPS
		# adapter, also mount it for some variants of the default schemes that
		# are limited to some specific address family only
		adapter = HTTPAdapter()
		for scheme in ("http", "https"):
			self.mount("{0}://".format(scheme), adapter)
			for name in AF2NAME.values():
				self.mount("{0}+{1}://".format(scheme, name), adapter)

	def request(self, method, url, *args, **kwargs):
		family = kwargs.pop("family", self.family)
		if family != socket.AF_UNSPEC:
			# Inject provided address family value as extension to scheme
			url = urllib.parse.urlparse(url)
			url = url._replace(scheme="{0}+{1}".format(url.scheme, AF2NAME[int(family)]))
			url = url.geturl()
		return super().request(method, url, *args, **kwargs)


session = Session


# Import other `requests` stuff to make the top-level API of this more compatible
from requests import (
	__title__, __description__, __url__, __version__, __build__, __author__,
	__author_email__, __license__, __copyright__, __cake__,
	
	exceptions, utils, packages, codes,
	Request, Response, PreparedRequest,
	RequestException, Timeout, URLRequired, TooManyRedirects, HTTPError,
	ConnectionError, FileModeWarning, ConnectTimeout, ReadTimeout
)


# Re-implement the top-level â€œsession-lessâ€� API
def request(method, url, **kwargs):
	with Session() as session:
		return session.request(method=method, url=url, **kwargs)


def get(url, params=None, **kwargs):
	kwargs.setdefault('allow_redirects', True)
	return request('get', url, params=params, **kwargs)


def options(url, **kwargs):
	pass


def head(url, **kwargs):
	pass


def post(url, data=None, json=None, **kwargs):
	pass


def put(url, data=None, **kwargs):
	pass


def patch(url, data=None, **kwargs):
	pass


def delete(url, **kwargs):
	pass
