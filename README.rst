======
Pyping  .. image:: https://travis-ci.org/twdkeule/pyping.svg?branch=master
    :target: https://travis-ci.org/twdkeule/pyping
======

A pure python ping implementation using raw sockets. Developed and tested for python3.

Note that ICMP messages can only be sent from processes running as root
(in Windows, you must run this script as 'Administrator').

Original Version from Matthew Dixon Cowles.

* Copyleft 1989-2011 by the python-ping team, see `AUTHORS <https://raw.github.com/socketubs/pyping/master/AUTHORS>`_ for more details.
* License: GNU GPL v2, see `LICENCE <https://raw.github.com/Socketubs/Pyping/master/LICENSE>`_ for more details.

Usage
-----
Use as a Python lib::

    >>> import pyping
    >>> r = pyping.ping('google.com')                # Need to be root or
    >>> r = pyping.ping('google.com', udp = True)    # But it's udp, not real icmp. This may not work currently
    >>> r.ret_code
    0
    >>> r.destination
    'google.com'
    >>> r.max_rtt
    '69.374'
    >>> r.avg_rtt
    '68.572'
    >>> r.min_rtt
    '67.681'
    >>> r.destination_ip
    '172.217.17.78'

Todo
----

- Docs
- Refactor core.py
- Tests

Contribute
----------

`Fork <http://help.github.com/fork-a-repo/>`_ this repo on `GitHub <https://github.com/twdkeule/pyping>`_ and `send <http://help.github.com/send-pull-requests>`_ pull requests. Thank you.
