from setuptools import find_packages, setup

setup(
    name='sncompass',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask-wtf',
        'pymongo',
        'gunicorn',
    ],
    data_files=[
        ('etc', ['sncompass.ini', 'gunicorn.conf.py']),
    ],
    entry_points={
        'console_scripts': [
            'sncompass = sncompass.server:main',
            'subnautica-nav = sncompass.calculate:main',
        ],
    },
)
