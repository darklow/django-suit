from setuptools import setup
from suit import VERSION

setup(
    name='django-suit',
    version=VERSION,
    description='Modern theme for Django admin interface.',
    author='Kaspars Sprogis (darklow)',
    author_email='info@djangosuit.com',
    url='http://djangosuit.com',
    packages=['suit', 'suit.templatetags'],
    install_requires=[
        'Django>=1.4',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: Free for non-commercial use',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ]
)
