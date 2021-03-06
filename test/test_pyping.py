# Copyright (C) 2017  Thomas De Keulenaer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Tests for pyping """

import random
import pyping


GOOGLE_HOST = 'google.com'
LOCALHOST = 'localhost'

def test_google_dns():
	g_dns = '8.8.8.8'
	r = pyping.ping(g_dns, fast=True)
	_assert_succesfull_ping(r, g_dns)
	assert is_valid_ip4_address(r.destination_ip)

def test_google():
	r = pyping.ping(GOOGLE_HOST, fast=True)
	_assert_succesfull_ping(r, GOOGLE_HOST)

def test_packets_sent():
	num_of_packets = random.randint(1, 10)
	result = pyping.ping(hostname=LOCALHOST, count=num_of_packets, interval=0.2)
	_assert_succesfull_ping(result, LOCALHOST)
	assert result.packets_sent == num_of_packets

def test_is_alive():
	assert pyping.is_host_alive(LOCALHOST)
	assert pyping.is_host_alive(GOOGLE_HOST) # of course this fails if Google is down


def _assert_succesfull_ping(r, orig_dest):
	try:
		assert r.succes
		assert r.destination == orig_dest

		assert _test_float(r.avg_rtt)
		assert _test_float(r.min_rtt)
		assert _test_float(r.max_rtt)
		avg_rtt = float(r.avg_rtt)
		min_rtt = float(r.min_rtt)
		max_rtt = float(r.max_rtt)

		assert max_rtt > 0
		assert min_rtt > 0
		assert avg_rtt > 0
		assert max_rtt >= avg_rtt
		assert avg_rtt >= min_rtt
	except AssertionError:
		print("Ping unsuccesful failed.\n### Ping output:")
		print(r.output)
		print('### end of output.')
		raise

def _test_float(f):
	try:
		float(f)
		return True
	except ValueError:
		return False

def is_valid_ip4_address(addr):
	parts = addr.split(".")
	if not len(parts) == 4:
		return False
	for part in parts:
		try:
			number = int(part)
		except ValueError:
			return False
		if number > 255:
			return False
	return True
