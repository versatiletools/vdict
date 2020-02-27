from setuptools import setup
import vdict

SHORT="vdict is an extension of dict to manipulate complex structured data such as JSON data."
LONG ="When we use a dict to manipulate JSON data, it's not comfortable because many JSON data have nested structures." \
      "With vdict, you can avoid to use redundant square brackets " \
      "like 'data[\"key1/key2/key3\"]' or 'data.key1.key2.key3'."

setup(
    name='vdict',
    version=vdict.__version__,
    packages=['vdict'],
    url=vdict.__url__,
    author=vdict.__author__,
    author_email=vdict.__email__,
    description=SHORT,
    long_description=LONG,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    test_suite='vdict_test',
)
