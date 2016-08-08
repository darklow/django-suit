from django import VERSION
from distutils.version import StrictVersion


def django_major_version(strict_version=False):
    """
    Return django's major version
    """
    version = '.'.join(map(str, VERSION[:2]))

    if strict_version:
        version = StrictVersion(version)

    return version


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
