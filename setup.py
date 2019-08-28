from setuptools import setup
import vdict

SHORT='vdict(Versatile Dictionary) is a extension of python dict object for manipulate structured data such as a JSON data.'
LONG=('vdict(Versatile Dictionary) is a extension of python dict object for manipulate structured data such as a JSON data.')

setup(
    name='vdict',
    version=vdict.__version__,
    packages=['vdict'],
    url='https://github.com/versatiletools/vdict',
    author=vdict.__author__,
    author_email='chywoo@gmail.com',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description=SHORT,
    long_description=LONG,
    test_suite='test_addict',
    package_data={'': ['LICENSE']}
)
