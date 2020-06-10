from setuptools import setup, find_packages


setup(
    name='test-fast-api',
    version='0.1.0',
    description='TODO list implementation',
    author='Marian Horban',
    author_email='horban.marian@gmail.com',
    packages=find_packages(
      include=[
          'test_fast_api',
          'test_fast_api.*'
      ]),
    namespace_packages=[
      'test_fast_api',
    ],
    install_requires=[
        'fastapi',
        'mongoengine',
        'uvicorn',
        'pyyaml',
    ],
    entry_points={
      'console_scripts': [
          'test-fast-api = test_fast_api.main:run',
      ]
    },
    zip_safe=True,
    package_data={'': ['*.yaml']})
