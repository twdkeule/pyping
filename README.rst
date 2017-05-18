======
Pyping
======

.. image:: https://travis-ci.org/twdkeule/pyping.svg?branch=master
    :target: https://travis-ci.org/twdkeule/pyping

A python wrapper around the Linux ping command. Developed and tested for python3.

Usage
-----
Use as a Python lib::

    >>> import pyping
    >>> r = pyping.ping('google.com')
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

- Add IPv6 support
- Add Windows support
- Docs
- Tests

Contribute
----------

`Fork <http://help.github.com/fork-a-repo/>`_ this repo on `GitHub <https://github.com/twdkeule/pyping>`_ and `send <http://help.github.com/send-pull-requests>`_ pull requests. Thank you.
