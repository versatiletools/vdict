#
# Copyright (c) 2018 Sungho Park(chywoo@gmail.com)
# This file is under MIT license.
#

__author__ = 'Sungho Park'

import json
import copy


class vdict:
    """
    Manipulate multiple layered multiple data type.
    """
    _data = None
    __prev_key = None
    __prev_dict = _data

    def __init__(self, data=None, deep=False):
        object.__setattr__(self, "__prev_key", None)
        object.__setattr__(self, "__prev_dict", self._data)

        if data is None:
            return

        if isinstance(data, str):
            # if the below code look as "self._data = XXX", self.__setattr__ function is being called.
            # Therefore, object.__setattr__ must be used to prevent from calling self.__setattr__.
            object.__setattr__(self, "_data", json.loads(data))
        else:
            if isinstance(data, self.__class__):
                temp = data._data
            elif isinstance(data, dict):
                temp = data
            else:
                raise TypeError("Not supported data type.")

            if deep:    # deep copy
                object.__setattr__(self, "_data", copy.deepcopy(temp))
            else:
                object.__setattr__(self, "_data", temp)

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    # data.key
    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        if self.__dict__.get("_locked") and key == "data":
            raise AttributeError("vdict does not allow assignment to .data memeber.")
        self.add(key, value)

    def __repr__(self):
        if self._data is not None:
            return json.dumps(self._data)
        else:
            return self

    def __setitem__(self, key, value):
        self.add(key, value)

    # data['key']
    def __getitem__(self, key):
        try:
            if self.__prev_key is not None:
                o = self.__prev_dict[key]
            else:
                o = self._data[key]

            object.__setattr__(self, "__prev_key", None)
            object.__setattr__(self, "__prev_dict", o)
            return o
        except Exception as e:
            # object.__setattr__(self, "_data", {})
            self._data[key] = {}
            object.__setattr__(self, "__prev_key", key)
            object.__setattr__(self, "__prev_dict", self._data[key])
            return self

    def _is_number(self, data):
        try:
            int(data)
            return True
        except ValueError:
            return False

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

        # loop of keys.
        for i in range(key_size):
            key = keys[i]
            if keys[i] == '':
                continue

            if self._is_number(key):
                key = int(key)
                is_list = True
            else:
                is_list = False

            # Initialize self._data
            if self._data is None:
                if is_list:     # if true, the first data is list
                    result = []
                else:
                    result = {}      # else, the first data is dictionary

                object.__setattr__(self, "_data", result)

            if i + 1 == key_size:
                if is_list:
                    result.append(value)
                else:
                    result[key] = value

                break

            try:
                result = result[key]
            except KeyError:
                if self._is_number(keys[i + 1]):
                    result[key] = []
                else:
                    result[key] = {}
                result = result[key]
            except IndexError:
                if self._is_number(keys[i + 1]):
                    result.append([])
                else:
                    result.append({})

                try:
                    result = result[key]
                except IndexError:
                    raise KeyError("list key '%d' is not linear." % key)
            except TypeError as e :
                raise KeyError("Data type of the key is not match. %s" % e.args[0])

    def __get(self, key_path=None):
        """
        Get value internal method. Input key path(key1/key2/key3) and get the value.
        :param key_path: Key path
        :return: Value
        """

        if key_path is None:
            return self._data

        result = self._data

        keys = key_path.split("/")
        self._error_data = ""

        for key in keys:
            if key == '':  # skip blank ex)first '/' at '/fields/description'
                continue
            else:
                if self._error_data == "" and key_path[0] != '/':
                    self._error_data = "%s" % key
                else:
                    self._error_data += "/%s" % key

            if isinstance(result, dict):
                result = result[key]
            elif isinstance(result, list):
                result = result[int(key)]

        return result

    def get(self, key_path=None):
        """
        Get value. Input key path(key1/key2/key3) and get the value.
        :param key_path: Key path
        :return: Value
        """

        try:
            return self.__get(key_path)
        except KeyError as e:
            return None

    def json(self):
        return json.dumps(self._data)

