# -*- coding: utf-8 -*-
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

here = os.path.dirname(os.path.abspath(__file__))

requires = [
    'Sphinx>=2.0',
    # TODO add timingdrawer here
]

setup(
    name='sphinxcontrib-timingdrawer',
    version='0.2.0',
    url='https://github.com/beaverc/sphinxcontrib-timingdrawer',
    download_url='',
    license='BSD',
    author='Christopher Beaver',
    author_email='beavercpb@gmail.com',
    description='Sphinx "timingdrawer" extension',
    long_description='',#open(os.path.join(here, 'README.rst')).read(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 3',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    # packages=['sphinxcontib',],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
namespace_packages=['sphinxcontrib'], )