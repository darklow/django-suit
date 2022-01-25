from setuptools import setup

setup(
    name='django-suit-v2-pm',
    version=__import__('suit').VERSION,
    description='Modern theme for Django admin interface.',
    author='Kaspars Sprogis (darklow) forked by Pulse-Mind',
    author_email='pulse.mind.com@gmail.com',
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10.0',
        'Environment :: Web Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
    ],
    python_requires='>=3.8',                # Minimum version requirement of the package
)
