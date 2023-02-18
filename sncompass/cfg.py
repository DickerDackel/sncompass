import sys
import os.path

from configparser import ConfigParser

conf = ConfigParser()
for f in ['sncompass.ini',
          os.path.join(sys.prefix, 'etc', 'sncompass.ini'),
          os.path.join('/etc', 'sncompass.ini')]:
    if os.path.isfile(f):
        conf.read(f)
        break
