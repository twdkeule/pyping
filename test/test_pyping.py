import pyping

def test_google_dns():
    g_dns = '8.8.8.8'
    r = pyping.ping(g_dns)
    print(r)
    _asserts(r, g_dns)

def test_google_com():
    g_com = 'google.com'
    r = pyping.ping(g_com)
    print(r)
    _asserts(r, g_com)


def _asserts(r, orig_dest):
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

def _test_float(f):
    try:
        float(f)
        return True
    except ValueError:
        return False
