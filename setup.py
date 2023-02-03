from setuptools import setup

setup(
    name="subnautica-navigator",
    version="0.1.0",
    packages=[],
    entry_points={
        'console_scripts': [
            'server = server:main',
            'subnautica-nav = subnautica:main',
        ],
    },
)
