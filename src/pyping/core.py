#!/usr/bin/env python3
# coding: utf-8

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

"""
	pyping.py
	Parses linux ping command.
	For now only IPv4 support.
	Not (yet) tested on Windows.
"""

import subprocess
import re

class Response(object):
	def __init__(self, returnvalue, output, platform_is_windows):
		self.succes = returnvalue == 0
		self.output = output
		self.max_rtt = None
		self.min_rtt = None
		self.avg_rtt = None
		self.mdev = None
		self.ttl = None
		self.total_time = None
		self.packet_size = None
		self.destination = None
		self.destination_ip = None
		self.packets_sent = None
		self.packets_received = None
		self.percentage_lost = None
		try:
			self.parse_output(platform_is_windows)
		except ValueError as ver:
			print('Could not parse output: ' + str(ver) + '\n\n' + output)

	def __str__(self):
		return self.output

	def parse_output(self, platform_is_windows):
		lines = self.output.splitlines()
		statisticts_start = 0
		for line in lines:
			if 'statistics' in line:
				break
			statisticts_start += 1
		if platform_is_windows:
			if not self._parse_header_ipv4_win(lines[1]):
				return
			self._parse_packet_stats_win(lines[statisticts_start + 1])
			if self.succes:
				self._parse_time_stats_win(lines[statisticts_start + 3])
		else:
			if not self._parse_header_ipv4_linux(lines[0]):
				return
			self._parse_packet_stats_linux(lines[statisticts_start + 1])
			if self.succes:
				self._parse_time_stats_linux(lines[statisticts_start + 2])

	#########
	# Linux #
	#########
	"""
		PING google.com (216.58.206.110) 56(84) bytes of data.
		PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
		64 bytes from 8.8.8.8: icmp_seq=1 ttl=47 time=27.4 ms
		64 bytes from 8.8.8.8: icmp_seq=2 ttl=47 time=14.6 ms
		64 bytes from 8.8.8.8: icmp_seq=3 ttl=47 time=12.6 ms
		--- 8.8.8.8 ping statistics ---
		3 packets transmitted, 3 received, 0% packet loss, time 2003ms
		rtt min/avg/max/mdev = 12.668/18.256/27.449/6.551 ms
	"""
	def _parse_header_ipv4_linux(self, line):
		parts = line.split(' ')
		if parts[0] != 'PING':
			if 'not known' in parts[0]:
				self.destination = parts[1].strip(':')
			return False
		self.destination = parts[1]
		self.destination_ip = parts[1]
		if '(' ==  parts[2][0] and ')' == parts[2][-1]:
			self.destination_ip = parts[2].strip('()')
		match = re.search(r'(\d+)\(\d+\) bytes of data\.', line)
		if match is None:
			raise ValueError('Header: cannot parse: ' + line)
		self.packet_size = int(match.group(1))
		return True

	def _parse_time_stats_linux(self, line):
		rtt, vars, _, values, ms = line.split(' ')
		if rtt != 'rtt' or ms != 'ms':
			raise ValueError('Time statistics: too many/few items: ' + line)
		vars = vars.split('/')
		values = values.split('/')
		if len(vars) != len(values):
			raise ValueError('Time statistics: # items does not match: ' + line)
		for i, var in enumerate(vars):
			if var == 'min':
				self.min_rtt = float(values[i]) / 1000
			elif var == 'avg':
				self.avg_rtt = float(values[i]) / 1000
			elif var == 'max':
				self.max_rtt = float(values[i]) / 1000
			elif var == 'mdev':
				self.mdev = float(values[i]) / 1000

	def _parse_packet_stats_linux(self, line):
		match = re.search(r'(\d+) packets transmitted, (\d+) received, (\d+)(|\.(\d+))% packet loss, time (\d+)ms', line)
		if match is None:
			raise ValueError('Packet statistics: cannot parse: ' + line)
		self.packets_sent = int(match.group(1))
		self.packets_received = int(match.group(2))
		self.percentage_lost = int(match.group(3))
		loss_comma = match.group(5)
		self.total_time = int(match.group(6)) / 1000
		if loss_comma is not None:
			self.percentage_lost += int(loss_comma) / (10 ** len(loss_comma))

	###########
	# Windows #
	###########
	"""
		Pinging 8.8.8.8 with 32 bytes of data:
		Pinging google.com [216.58.208.46] with 32 bytes of data:
		Reply from 216.58.208.46: bytes=32 time=23ms TTL=51
		Reply from 216.58.208.46: bytes=32 time=26ms TTL=51
		Reply from 216.58.208.46: bytes=32 time=23ms TTL=51
		Reply from 216.58.208.46: bytes=32 time=27ms TTL=51

		Ping statistics for 216.58.208.46:
			Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
		Approximate round trip times in milli-seconds:
			Minimum = 23ms, Maximum = 27ms, Average = 24ms
	"""
	def _parse_header_ipv4_win(self, line):
		parts = line.split(' ')
		if parts[0] != 'Pinging':
			# if 'not known' in parts[0]:
			# 	self.destination = parts[1].strip(':')
			return False
		self.destination = parts[1]
		self.destination_ip = parts[1]
		if '[' ==  parts[2][0] and ']' == parts[2][-1]:
			self.destination_ip = parts[2].strip('[]')
		match = re.search(r'with (\d+) bytes of data', line)
		if match is None:
			raise ValueError('Header: cannot parse: ' + line)
		self.packet_size = int(match.group(1))
		return True

	def _parse_packet_stats_win(self, line):
		match = re.search(r'Packets: Sent = (\d+), Received = (\d+), Lost = (\d+) ', line)
		if match is None:
			raise ValueError('Packet statistics: cannot parse: ' + line)
		self.packets_sent = int(match.group(1))
		self.packets_received = int(match.group(2))
		packets_lost = int(match.group(3))
		self.percentage_lost = packets_lost / self.packets_sent

	def _parse_time_stats_win(self, line):
		match = re.search(r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms', line)
		if match is None:
			raise ValueError('Packet statistics: cannot parse: ' + line)
		self.min_rtt = float(match.group(1)) / 1000
		self.max_rtt = float(match.group(2)) / 1000
		self.avg_rtt = float(match.group(3)) / 1000

class Ping(object):
	ping = 'ping'
	has_ipv4_flag = None
	platform_is_windows = False

	def __init__(self, destination, count=1, timeout=-1.0, packet_size=-1, interval=-1.0, sourceaddress=None, ttl=-1):
		self.destination = str(destination)
		self.count = int(count)
		self.timeout = float(timeout)
		self.packet_size = int(packet_size)
		self.interval = float(interval)
		self.sourceaddress = sourceaddress
		self.ttl = int(ttl)

	@staticmethod
	def _check_exe():
		from sys import platform as _platform
		if _platform == "linux" or _platform == "linux2":
		   # linux
		   pass
		elif _platform == "darwin":
		   # MAC OS X
		   pass
		elif _platform == "win32":
	   		Ping.platform_is_windows = True
		ret = subprocess.run([Ping.ping, '-h'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		if '4' in ret.stdout.decode() or Ping.platform_is_windows:
			Ping.has_ipv4_flag = True
		else:
			Ping.has_ipv4_flag = False

	def run(self):
		if Ping.has_ipv4_flag is None:
			Ping._check_exe()
		args = [Ping.ping]
		if Ping.has_ipv4_flag:
			args.append('-4')
		if Ping.platform_is_windows:
			args += ['-n', str(self.count)]
			if self.timeout > 0:
				args += ['-w', str(self.timeout)]
			if self.packet_size > 0:
				args += ['-l', str(self.packet_size)]
			if self.ttl > 0:
				args += ['-i', str(self.ttl)]
			if self.sourceaddress is not None:
				args += ['-S', str(self.sourceaddress)]
		else:
			# Linux
			if self.timeout > 0:
				max_timeout = int(self.count * self.timeout)
				args += ['-W', str(self.timeout)]
			else:
				max_timeout = self.count
			args += ['-w', str(max_timeout)]
			if self.packet_size > 0:
				args += ['-s', str(self.packet_size)]
			if self.interval > 0:
				args += ['-i', str(self.interval)]
			if self.ttl > 0:
				args += ['-t', str(self.ttl)]
			if self.sourceaddress is not None:
				args += ['-I', str(self.sourceaddress)]
		args.append(self.destination)
		compl_proc = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		return Response(compl_proc.returncode, compl_proc.stdout.decode(), Ping.platform_is_windows)

def ping(hostname, count=3, *args, **kwargs):
	p = Ping(hostname, count, *args, **kwargs)
	return p.run()
