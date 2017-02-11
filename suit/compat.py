try:
    # Python 3.
    from urllib.parse import parse_qs
except ImportError:
    # Python 2.6+
    from urlparse import parse_qs
