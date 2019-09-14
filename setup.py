from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent.absolute()
readme = this_directory/Path('README.md')
with readme.open('r') as f:
    long_description = f.read()

setup(name='wallsch',
      version='0.5',
      description='A simple wallpaper changer/scheduler with night/day split',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Blazej Sewera',
      url='https://github.com/jazzsewera/wallsch',
      copyright='Copyright 2019 Blazej Sewera',
      license='MPL2',
      packages=['wallsch'],
      install_requires=[
        'apscheduler',
        'suntime',
        'tzlocal',
        'pyro4'
      ],
      entry_points={
        'console_scripts': [
            'wallschd = wallschd:main',
            'wallschctl = wallschctl:main'
        ]
      })
