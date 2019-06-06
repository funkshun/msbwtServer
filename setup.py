from setuptools import find_packages, setup

setup(
    name='msbwtServer',
    version='0.1.0',
    author="Boo Fullwood",
    description="A flask-based name resolution and server management tool for msbwtCloud",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'requests',
        'waitress',
        'apscheduler',
        'msbwt==0.3.0'
    ],
    dependency_links=[
        'git+ssh://git@github.com/txje/msbwt/tarball/master#egg=msbwt-0.3.0'
    ]
)