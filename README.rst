======
Pyping
======

.. image:: https://travis-ci.org/twdkeule/pyping.svg?branch=master
    :target: https://travis-ci.org/twdkeule/pyping
.. image:: https://api.codacy.com/project/badge/Grade/1e64c14c480745e5b9db007998909798
    :target: https://www.codacy.com/app/twdkeule/pyping?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=twdkeule/pyping&amp;utm_campaign=Badge_Grade

A python wrapper around the Linux ping command. Developed and tested for python3 on Windows 10 and Ubuntu 17.04 and 12.04.

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
- Docs

Contribute
----------

`Fork <http://help.github.com/fork-a-repo/>`_ this repo on `GitHub <https://github.com/twdkeule/pyping>`_ and `send <http://help.github.com/send-pull-requests>`_ pull requests. Thank you.
