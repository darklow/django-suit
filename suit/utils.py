import re
from django import VERSION


def django_major_version():
    return float('.'.join([str(i) for i in VERSION][:2]))


def value_by_version(args):
    """
    Return value by version
    Return latest value if version not found
    """
    version_map = args_to_dict(args)
    return version_map.get(django_major_version(),
                           list(version_map.values())[-1])


def args_to_dict(args):
    """
    Convert template tag args to dict
    Format {% suit_bc 1.5 'x' 1.6 'y' %} to { '1.5': 'x', '1.6': 'y' }
    """
    return dict(zip(args[0::2], args[1::2]))


def attrs_by_prefix(html, prefix):
    attrs = re.findall('(%s.+?)="(.+?)"' % prefix, html)
    return dict(attrs)


def dict_to_attrs(attrs_dict):
    return ' '.join(['%s="%s"' % (k, v) for k, v in attrs_dict.items()])
