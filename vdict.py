#
# Copyright (c) 2018 Sungho Park(chywoo@gmail.com)
# This file is under MIT license.
#

__author__ = 'Sungho Park'

import json
import copy


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
    _error_data = None

    def __init__(self, data=None, deep=False):
        if data is None:
            self._data = None
            return

        if isinstance(data, str):
            self._data = json.loads(data)
        else:
            if isinstance(data, self.__class__):
                temp = data._data
            elif isinstance(data, dict):
                temp = data
            else:
                raise TypeError("Not supported data type.")

            if deep:    # deep copy
                self._data = copy.deepcopy(temp)
            else:
                self._data = temp

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __setattr__(self, key, value):
        if self.__dict__.get("_locked") and key == "data":
            raise AttributeError("vdict does not allow assignment to .data memeber.")
        self.__dict__[key] = value

    def __repr__(self):
        if self._data is not None:
            return json.dumps(self._data)
        else:
            return self

    def __setitem__(self, key, value):
        self.add(key, value)

    def __getitem__(self, item):
        r = self.get(item)

        if r is None:
            raise KeyError(self._error_data)
        else:
            return r

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

    def get(self, key_path=None):
        """
        Get value. Input key path(key1/key2/key3) and get the value.
        :param key_path: Key path
        :return: Value
        """

        if key_path is None:
            return self._data

        result = self._data

        keys = key_path.split("/")
        self._error_data = ""

        for key in keys:
            if key == '': # skip blank ex)first '/' at '/fields/description'
                continue
            else:
                self._error_data += "/%s" % key

            if isinstance(result, dict):
                try:
                    result = result[key]
                except KeyError as e:
                    return None
            elif isinstance(result, list):
                try:
                    result = result[int(key)]
                except ValueError as e:
                    return None

        return result

    def json(self):
        return json.dumps(self._data)
