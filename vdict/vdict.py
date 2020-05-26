#
# Copyright (c) 2018 Sungho Park(chywoo@gmail.com)
# This file is under MIT license.
#

__author__ = 'Sungho Park'

import json


class vdict(dict):
    """
    Manipulate multiple layered multiple data type.
    """
    def __init__(self, args=None):
        if args is None:
            return

        if isinstance(args, str):
            self.update(json.loads(args))
        elif isinstance(args, self.__class__):
            self.update(args)
        elif isinstance(args, dict):
            self.update(args)
        else:
            raise TypeError("Not supported data type.")

    def __call__(self):
        """
        The same with __repr__ function.
        """
        self.__repr__()

    def __getattr__(self, item):
        """
        Get value of specified attributes.
        Keep in your mind that this doesn't throw KeyError
        but just assign a vdict object.

        The below code just print a empty dict like {}.

          data = vdict()
          print(data.a.b.c)

        :param item:
        :return:
        """
        # Don't use __missing__ function to get KeyError with a use of []
        o = super().get(item)
        if o is None:
            self[item] = vdict()
            o = super().get(item)
        return o

    def __setattr__(self, key, value):
        if isinstance(value, dict):
             value = vdict(value)

        super().__setitem__(key, value)

    def __setitem__(self, key, value, dict_setitem=dict.__setitem__):
        if isinstance(value, dict):
            value = vdict(value)

        # super().__setitem__(key, value)
        self.add(key, value, dict_setitem)

    def __getitem__(self, item):
        return self.__get(item)

    def __get(self, key_path):
        """
        Get value internal method. Input key path(key1/key2/key3) and get the value.
        :param key_path: Key path
        :return: Value
        """
        if key_path is None:
            return self

        data = self

        keys = key_path.split("/")
        _error_data = ""

        for key in keys:
            if key == '':  # skip blank ex) the first '/' in '/fields/description'
                continue
            else:
                if _error_data == "" and key_path[0] != '/':
                    _error_data = "%s" % key
                else:
                    _error_data += "/%s" % key

            if isinstance(data, vdict):
                data = super(vdict, data).get(key)
            elif isinstance(data, dict):    # class dict doesn't have super class.
                data = data.get(key)
            elif isinstance(data, list):
                data = data[int(key)]

            if data is None:
                raise KeyError(_error_data)

        return data

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

    def add(self, keypath, value, dict_setitem=dict.__setitem__):
        """
        Add list or dictionary data with key path
        :param keypath: data path. eg) 0/a/b/d
        :param value: data to store
        :return: Nothing
        """
        assert (keypath is not None and value is not None)

        keys = keypath.split("/")

        result = self
        key_size = len(keys)

        for i in range(key_size):
            key = keys[i]
            if keys[i] == '':
                continue

            if self.is_number(key):
                if self == {}:  # When the first date is list, throw a exception.
                    raise TypeError("First data must not be a list")

                key = int(key)
                is_list_type = True
            else:
                is_list_type = False

            # internal data must be a collection.
            if i < key_size - 1:
                try:
                    result = result[key]
                except KeyError:    # when dict
                    if self.is_number(keys[i + 1]):
                        dict_setitem(result, key, [])
                    else:
                        dict_setitem(result, key, {})

                    result = result[key]
                except IndexError:  # when list
                    if self.is_number(keys[i + 1]):
                        result.append([])
                    else:
                        result.append({})

                    try:
                        result = result[key]
                    except IndexError:
                        raise KeyError("list key '%d' is not linear." % key)
                except TypeError as e :
                    raise KeyError("Data type of the key is not match. %s" % e.args[0])
            # at leaf
            else:
                if is_list_type:
                    result.append(value)
                else:
                    # super().__setitem__(key, value)
                    dict_setitem(result, key, value)

                break

    def json(self):
        return json.dumps(self)

    def is_number(self, data):
        try:
            int(data)
            return True
        except ValueError:
            return False
