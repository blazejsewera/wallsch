from setuptools import setup
from pathlib import Path


this_directory = Path(__file__).parent.absolute()
readme = this_directory/Path('README.md')
with readme.open('r') as f:
    long_description = f.read()

setup(name='wallsch',
      version='0.6',
      description='A simple wallpaper changer/scheduler with night/day split',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='Blazej Sewera',
      url='https://github.com/jazzsewera/wallsch',
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
            'wallschd = wallsch.wallschd:main',
            'wallschctl = wallsch.wallschctl:main'
        ]
      })
