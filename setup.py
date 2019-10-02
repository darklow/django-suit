from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='django-suit',
    version=__import__('suit').VERSION,
    description='Modern theme for Django admin interface.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Kaspars Sprogis (darklow)',
    author_email='info@djangosuit.com',
    url='http://djangosuit.com',
    packages=['suit', 'suit.templatetags'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: Free for non-commercial use',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ]
)
