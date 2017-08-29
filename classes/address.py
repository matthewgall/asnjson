#!/usr/bin/env python3

import os, sys, socket
from cymruwhois import Client

class Address:

	def __init__(self, address):
		self.address = address
		if not self._valid_ipv4() and not self._valid_ipv6():
			raise AttributeError("Invalid address")

	def _valid_ipv4(self):
		try:
			socket.inet_pton(socket.AF_INET, self.address)
		except AttributeError:  # no inet_pton here, sorry
			try:
				socket.inet_aton(self.address)
			except socket.error:
				return False
			return address.count('.') == 3
		except socket.error:  # not a valid address
			return False

		self.ip_class = 4
		return True

	def _valid_ipv6(self):
		try:
			socket.inet_pton(socket.AF_INET6, self.address)
		except socket.error:  # not a valid address
			return False

		self.ip_class = 6
		return True

	def lookup(self):
		try:
			return Client().lookup(ip)
		except:
			raise SystemError