from setuptools import setup

setup(
    name="subnautica-navigator",
    version="0.1.0",
    packages=[],
    entry_points={
        'console_scripts': [
            'sncompass = sncompass.server:main',
            'subnautica-nav = sncompass.calculate:main',
        ],
    },
)
