from setuptools import setup

setup(
    name='django-suit',
    version=__import__('suit').VERSION,
    description='Modern theme for Django admin interface.',
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
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ]
)
