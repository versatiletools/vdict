# -*- coding: utf-8 -*-

# Copyright: Sungho Park(chywoo@gmail.com)
# License: MIT
# URL: https://github.com/chywoo/versatiledict
#
#

"""
Versatile Dicionary Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~


"""
__author__ = 'Sungho Park'

import json


def is_number(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


class vdict:
    """
    Manipulate multiple layered multiple data type.
    """
    _data = None

    def __init__(self, obj=None):
        if obj is None:
            self._data = None
            return

        if isinstance(obj, self.__class__):
            self._data = obj._data
        elif isinstance(obj, dict):
            self._data = obj
        elif isinstance(obj, str):
            self._data = json.loads(obj)
        else:
            raise TypeError("Not supported data type. Support types are dict and vdict.")

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __setattr__(self, key, value):
        if self.__dict__.get("_locked") and key == "data":
            raise AttributeError("VersatileDict does not allow assignment to .data memeber.")
        self.__dict__[key] = value

    def __repr__(self):
        if self._data is not None:
            return json.dumps(self._data)
        else:
            return self

    def __len__(self):
        return len(self._data)

    def add(self, keypath, value):
        """
        Add list or dictionary data with key path
        :param keypath: data path. eg) 0/a/b/d
        :param value: data to store
        :return: Nothing
        """
        assert (keypath is not None and value is not None)

        keys = keypath.split("/")

        result = self._data
        key_size = len(keys)

        for i in range(key_size):
            key = keys[i]
            if keys[i] == '':
                continue

            if is_number(key):
                key = int(key)
                is_data_list = True
            else:
                is_data_list = False

            # Initialize self._data
            if self._data is None:
                if is_data_list:     # if true, the first data is list
                    result = []
                else:
                    result = {}                 # else, the first data is dictionary

                self._data = result

            if i + 1 == key_size:
                if is_data_list:
                    result.append(value)
                else:
                    result[key] = value

                break

            try:
                result = result[key]
            except KeyError:
                if is_number(keys[i + 1]):
                    result[key] = []
                else:
                    result[key] = {}
                result = result[key]
            except IndexError:
                if is_number(keys[i + 1]):
                    result.append([])
                else:
                    result.append({})

                try:
                    result = result[key]
                except IndexError:
                    raise KeyError("list key '%d' is not linear." % key)
            except TypeError as e :
                raise KeyError("Data type of the key is not match. %s" % e.args[0])

    def get(self, keystring=None):
        """
        Get value from JSON format data. Input key path(key1/key2/key3) and get the value.
        :param keystring: Key path
        :return: Value
        """

        if keystring is None:
            return self._data

        result = self._data
        keys = keystring.split("/")

        for key in keys:
            if key == '': # skip blank ex)first '/' at '/fields/description'
                continue

            if isinstance(result, dict):
                result = result[key]
            elif isinstance(result, list):
                try:
                    result = result[int(key)]
                except ValueError as e:
                    raise KeyError("'%s' is not index value of List. Type of the value is List. Index must be integer." % key)

        if isinstance(result, dict) or isinstance(result, list):
            tmp = json.dumps(result)
            result = vdict(tmp)
        return result

    def json(self):
        return json.dumps(self._data)

