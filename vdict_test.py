# -*- coding: utf-8 -*-

"""
Test cases for vdict module.
"""

import pytest
from vdict import vdict


def test_1_constructors():
    """
    constructor with various data types.
    """

    print("1. Constructing with a simple JSON")
    json_str = '{ "a": 1, "b": 2, "c": "3"}'
    json_vdict = vdict(json_str)

    print(f"json_vdict['a'] = {json_vdict['a']}")
    print(f"json_vdict['b'] = {json_vdict['b']}")
    print(f"json_vdict['c'] = {json_vdict['c']}")

    for i in range(1, 1000):
        assert json_vdict['a'] == 1
        assert json_vdict['b'] == 2
        assert json_vdict['c'] == "3"

        # there is not attirbute "d" in the variable and KeyError must be risen.
        with pytest.raises(KeyError):
            json_vdict["d"]

    # TODO When you call sub attribute 'e' of non-exist attribute 'd',
    #  vdict doesn't know if the code is for setting a value or getting a value.
    #  So vdict just make dicts for 'd' and 'e'.
    #  In fact, if the code is for getting value, vdict must throw AttributeError.
    #  But now vdict return dict object. Fix this later.
    assert json_vdict.d.e == {}

    print()
    print("2. Constructing with a dict object.")
    dict_data = {"a": 1, "b": 2, "c": "3"}
    dict_data2 = {"firstname": "Sungho", "lastname": "Park", "mail": "chywoo@gmail.com", "nooffamily": 4}
    dict_data["d"] = dict_data2

    dict_vdict = vdict(dict_data)

    print(f"dict_vdict['a'] = {dict_vdict['a']}")
    print(f"dict_vdict['b'] = {dict_vdict['b']}")
    print(f"dict_vdict['c'] = {dict_vdict['c']}")
    print(f"dict_vdict['d'] = {dict_vdict['d']}")

    for i in range(1, 1000):
        assert dict_vdict['a'] == 1
        assert dict_vdict['b'] == 2
        assert dict_vdict['c'] == "3"
        assert dict_vdict['d']['firstname'] == "Sungho"
        assert dict_vdict['d']['lastname'] == "Park"
        assert dict_vdict['d']['mail'] == "chywoo@gmail.com"
        assert dict_vdict['d']['nooffamily'] == 4

        with pytest.raises(KeyError):
            dict_vdict["e"]

def test_2_attr_and_brace_must_be_the_same():
    """
    Values added with attribute must be the same with values added with brace.
    ex) value.key == value['key'].
    """
    print("1. With a plain vdict")
    plain_vdict = vdict()

    plain_vdict.attr1 = "test data"
    print(f" - test_dict.attr1    = '{plain_vdict.attr1}'")
    print(f" - test_dict['attr1'] = '{plain_vdict['attr1']}'")

    assert plain_vdict.attr1, plain_vdict['attr1'] == "The values by attribute and brace must be the same."

    print()
    json_vdict = vdict()
    print("2. With a vdict initialized by JSON")
    json_vdict = vdict('{ "type": "CONNECT" }')
    print(f" - test_dict.type    = '{json_vdict.type}'")
    print(f" - test_dict['type'] = '{json_vdict['type']}'")

    assert json_vdict.type, json_vdict['type'] == "The values by attribute and brace must be the same."

    print()
    print("3. With values of vdict initialized by JSON")
    jsonattr_vdict = vdict('{ "type": "CONNECT" }')

    jsonattr_vdict.attr1 = "test data"
    print(f" - test_dict.attr1    = '{jsonattr_vdict.attr1}'")
    print(f" - test_dict['attr1'] = '{jsonattr_vdict['attr1']}'")

    assert jsonattr_vdict.attr1, jsonattr_vdict['attr1'] == "The values by attribute and brace must be the same."

def test_3_errors():
    test_dict = vdict()

    test_dict.a = 1

    with pytest.raises(KeyError):
        test_dict['b']

    # pytest.raises(KeyError, test_dict['b'])
    assert test_dict.get('b') is None
    assert {} == test_dict.b

    test_dict.attr1.attr2.attr3 = 1
    test_dict.attr1.attr2.attr4 = 2

    with pytest.raises(KeyError):
        test_dict["attr1/attr2/attr5"]
        test_dict["attr1.attr3.attr2"]

    assert test_dict.get("attr1/attr2/attr5") is None
    assert test_dict.get("attr1.attr3.attr2") is None
    assert {} == test_dict.attr1.attr2.attr5
    assert {} == test_dict.attr1.attr3.attr2

    with pytest.raises(AttributeError):
        test_dict.attr1.attr2.attr3.new_data = 1

def test_5_setget_by_braces():
    name = vdict()

    name["given"] = "Sungho"
    name["family"] = "Park"
    name["addr/city"] = "Seoul"

    with pytest.raises(TypeError):
        name["family/first"] = "Junha"

    info = vdict()
    info["name"] = name

    data3 = {"phone": "123-4567", "addr": {"city": "Seoul", "country": "Korea"}}
    info["etc"] = data3
    assert info["name/given"] == "Sungho"
    assert info["name/family"]== "Park"
    assert info["name"] == name
    assert info["etc/addr/city"] == "Seoul"

    info["card/0/number"] = "12345"
    info["card/1/number"] = "67890"
    info["card/2"] = 100

    assert info["card/0/number"] == "12345"
    assert info["card/1/number"] == "67890"
    assert info["card/2"] == 100

    query = vdict()
    query["query/sql/0/select"] = name
    query["query/sql/1"] = data3
    query["query/filtered"] = info

    assert query["query/sql/0/select/given"]     == "Sungho"
    assert query["query/sql/0/select/family"]    == "Park"
    assert query["query/sql/1/phone"]            == "123-4567"
    assert query["query/sql/1/addr/country"]     == "Korea"
    assert query["query/sql/1/addr/city"]        == "Seoul"
    assert query["query/filtered/card/0/number"] == "12345"
    assert query["query/filtered/card/1/number"] == "67890"
    assert query["query/filtered/card/2"]        == 100

def test_6_setget_by_attrs():
    test_dict = vdict()

    data = "data"
    test_dict.prop1 = data
    assert data == test_dict.prop1

    data = {"file1", "file2"}
    test_dict.dir1.files = data
    assert data == test_dict.dir1.files

    data = [1, 2, 3]
    test_dict.dir1.seq = data
    assert data == test_dict.dir1.seq

    test_dict = vdict()
    test_dict.attr1.attr2.attr3 = {"item1": 1, "item2": 2}
    assert test_dict.attr1.attr2.attr3.item1 == 1
    assert test_dict.attr1.attr2.attr3.item2 == 2

    assert test_dict["attr1/attr2/attr3/item1"] == 1
    assert test_dict["attr1/attr2/attr3/item2"] == 2

    assert test_dict.get("attr1/attr2/attr3/item1") == 1
    assert test_dict.get("attr1/attr2/attr3/item2") == 2

def test_7_with_list_data():
    data = vdict()

    data["files/0"] = "a.dat"
    data["files/1"] = "b.dat"
    data["files/2"] = "c.dat"

    assert data["files/0"] == "a.dat"
    assert data["files/1"] == "b.dat"
    assert data["files/2"] == "c.dat"
    assert isinstance(data["files"], list)

def test_8_json_data():
    json_data1 = """{
        "query": {
            "filtered": {
                "query": {
                    "match": {"language": "C/C++"}
                },
                "filter": {
                    "term": {"created": "2018-11-23"}
                }
            }
        }
    }"""

    json_data2 = """
        {
            "query": {
                "filtered": [{
                    "query": {
                        "match": {
                            "language": "Python"
                        }
                    },
                    "filter": {
                        "term": {
                            "created": "2019-03-05"
                        }
                    }
                }, {
                    "query": {
                        "match": {
                            "language": "C/C++"
                        }
                    },
                    "filter": {
                        "term": {
                            "created": "2018-11-23"
                        }
                    }
                }]
            }
        }
    """

    data1 = vdict(json_data1)
    v = data1["query/filtered/query/match/language"]
    assert v == "C/C++"

    v = data1.query.filtered.query.match.language
    assert v == "C/C++"

    data2 = vdict(json_data2)
    v = data2["query/filtered/0/query/match/language"]

    assert v == "Python"

def test_9_sub_dict():
    test_dict = vdict()

    test_dict.a.b=1
    print(test_dict.json())

    test2 = test_dict.a
    print(test2)
    print(test2.__class__)

    test2.b = 2
    print(test_dict)
    print(test_dict.a.json())
    print(test2)

    assert test_dict.a.b == test2.b
    assert isinstance(test2, vdict)

    test2_dict = vdict()
    test2_dict["sub1/sub2"] = 1
    print(test2_dict.sub1.json())

def test_10_json_sub_dict():
    json_data = {"type": "AUTH", "server": "1.1.1.1",
                 "authentication": {"type": "BASIC", "id": "user", "password": "password"}}
    jdict = vdict(json_data)

    mdict = vdict()
    mdict.type = "AUTH"
    mdict.server="1.1.1.1"
    mdict.authentication.type = "BASIC"
    mdict.authentication.id = "user"
    mdict.authentication.password = "password"

    auth = jdict.authentication

    assert mdict.authentication.type.__class__ == jdict.authentication.type.__class__

def test_11_callable():
    json_data = {"type": "AUTH", "server": "1.1.1.1",
                 "authentication": {"type": "BASIC", "id": "user", "password": "password"}}

    json_dict = vdict(json_data)

    print(json_dict())
    assert json_dict() is None, "Must be a callable object."

def test_12_shallow_copy():
    json_data = {"type": "AUTH", "server": "1.1.1.1",
                 "authentication": {"type": "BASIC", "id": "user", "password": "password"}}
    jdict = vdict(json_data)
    jdict.funcs = ["A", "B"]

    adict = jdict.copy()
    assert isinstance(adict, vdict), "The copyied object must be a vdict."
    assert not adict is jdict
    assert adict.funcs is jdict.funcs

    jdict.funcs[0] = "C"
    assert not adict is jdict
    assert jdict == adict
    assert jdict.funcs == adict.funcs

def test_13_deep_copy():
    json_data = {"type": "AUTH", "server": "1.1.1.1",
                 "authentication": {"type": "BASIC", "id": "user", "password": "password"}}
    jdict = vdict(json_data)
    jdict.funcs = ["A", "B"]

    adict = jdict.deepcopy()
    assert isinstance(adict, vdict)
    assert not adict is jdict
    assert not adict.funcs is jdict.funcs

    jdict.funcs[0] = "C"
    assert not adict is jdict
    assert jdict != adict
    assert jdict.funcs != adict.funcs

    new_dict = vdict()
    new_dict.name1 = "Sungho"
    new_dict.name2 = "Junha"

    jdict.names = new_dict

    bdict = jdict.deepcopy()
    assert isinstance(bdict, vdict)
    assert not bdict is jdict
    assert bdict.names.name1 == jdict.names.name1
    assert bdict.names.name2 == jdict.names.name2

    bdict.names.name2 = "Juha"
    assert bdict.names.name1 == jdict.names.name1
    assert bdict.names.name2 != jdict.names.name2


if __name__ == '__main__':
    pytest.main()
