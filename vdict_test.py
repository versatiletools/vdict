# -*- coding: utf-8 -*-

import unittest
from vdict import vdict


class BasicDictionaryFunctionTestCase(unittest.TestCase):
    def test_1_attr_and_brace_must_be_the_same(self):
        print("1. With a plain vdict")
        test_dict = vdict()

        test_dict.attr1 = "test data"
        print(f" - test_dict.attr1    = '{test_dict.attr1}'")
        print(f" - test_dict['attr1'] = '{test_dict['attr1']}'")

        self.assertEqual(test_dict.attr1, test_dict['attr1'], "The values by attribute and brace must be the same.")

        print()
        print("2. With a initialized vdict by JSON")
        test_dict = vdict('{ "type": "CONNECT" }')

        test_dict.attr1 = "test data"
        print(f" - test_dict.attr1    = '{test_dict.attr1}'")
        print(f" - test_dict['attr1'] = '{test_dict['attr1']}'")

        self.assertEqual(test_dict.attr1, test_dict['attr1'], "The values by attribute and brace must be the same.")

        print()
        print("3. With values of vdict initialized by JSON")
        test_dict = vdict('{ "attr1": "test data" }')
        print(f" - test_dict.attr1    = '{test_dict.attr1}'")
        print(f" - test_dict['attr1'] = '{test_dict['attr1']}'")

        self.assertEqual(test_dict.attr1, test_dict['attr1'], "The values by attribute and brace must be the same.")

    def test_2_constuctors(self):
        dict_data = vdict({"a": 1, "b": 2, "c": "3"})

        print(f"dict_data['a'] = {dict_data['a']}")
        print(f"dict_data['b'] = {dict_data['b']}")
        print(f"dict_data['c'] = {dict_data['c']}")

        with  self.assertRaises(KeyError):
            dict_data["d"]

        # TODO At this time, there is not way to find how many attributes are specified at code.
        #  So dict_data.d.e return just a dict object instead of AttributeError. Fix this later.
        self.assertEqual(dict_data.d.e, {})

        json_dict = vdict('{ "type": "CONNECT" }')
        self.assertEqual(json_dict["type"], "CONNECT")

    def test_3_errors(self):
        test_dict = vdict()

        test_dict.a = 1

        with self.assertRaises(KeyError):
            test_dict['b']

        # self.assertRaises(KeyError, test_dict['b'])
        self.assertIsNone(test_dict.get('b'))
        self.assertEqual({}, test_dict.b)

        test_dict.attr1.attr2.attr3 = 1
        test_dict.attr1.attr2.attr4 = 2

        with self.assertRaises(KeyError):
            test_dict["attr1/attr2/attr5"]
            test_dict["attr1.attr3.attr2"]

        self.assertIsNone(test_dict.get("attr1/attr2/attr5"))
        self.assertIsNone(test_dict.get("attr1.attr3.attr2"))
        self.assertEqual({}, test_dict.attr1.attr2.attr5)
        self.assertEqual({}, test_dict.attr1.attr3.attr2)

        with self.assertRaises(AttributeError):
            test_dict.attr1.attr2.attr3.new_data = 1

    def test_5_setget_by_braces(self):
        name = vdict()

        name["given"] = "Sungho"
        name["family"] = "Park"
        name["addr/city"] = "Seoul"

        with self.assertRaises(TypeError):
            name["family/first"] = "Junha"

        info = vdict()
        info["name"] = name

        data3 = {"phone": "123-4567", "addr": {"city": "Seoul", "country": "Korea"}}
        info["etc"] = data3

        self.assertEqual(info["name/given"], "Sungho")
        self.assertEqual(info["name/family"], "Park")
        self.assertEqual(info["name"], name)
        self.assertEqual(info["etc/addr/city"], "Seoul")

        info["card/0/number"] = "12345"
        info["card/1/number"] = "67890"
        info["card/2"] = 100

        self.assertEqual(info["card/0/number"], "12345")
        self.assertEqual(info["card/1/number"], "67890")
        self.assertEqual(info["card/2"], 100)

        query = vdict()
        query["query/sql/0/select"] = name
        query["query/sql/1"] = data3
        query["query/filtered"] = info

        self.assertEqual(query["query/sql/0/select/given"]    , "Sungho")
        self.assertEqual(query["query/sql/0/select/family"]   , "Park")
        self.assertEqual(query["query/sql/1/phone"]           , "123-4567")
        self.assertEqual(query["query/sql/1/addr/country"]    , "Korea")
        self.assertEqual(query["query/sql/1/addr/city"]       , "Seoul")
        self.assertEqual(query["query/filtered/card/0/number"], "12345")
        self.assertEqual(query["query/filtered/card/1/number"], "67890")
        self.assertEqual(query["query/filtered/card/2"]       , 100)


    def test_6_setget_by_attrs(self):
        test_dict = vdict()

        data = "data"
        test_dict.prop1 = data
        self.assertEqual(data, test_dict.prop1)

        data = {"file1", "file2"}
        test_dict.dir1.files = data
        self.assertEqual(data, test_dict.dir1.files)

        data = [1, 2, 3]
        test_dict.dir1.seq = data
        self.assertEqual(data, test_dict.dir1.seq)

        test_dict = vdict()
        test_dict.attr1.attr2.attr3 = {"item1": 1, "item2": 2}
        self.assertEqual(test_dict.attr1.attr2.attr3.item1, 1)
        self.assertEqual(test_dict.attr1.attr2.attr3.item2, 2)

        self.assertEqual(test_dict["attr1/attr2/attr3/item1"], 1)
        self.assertEqual(test_dict["attr1/attr2/attr3/item2"], 2)

        self.assertEqual(test_dict.get("attr1/attr2/attr3/item1"), 1)
        self.assertEqual(test_dict.get("attr1/attr2/attr3/item2"), 2)

    def test_7_with_list_data(self):
        data = vdict()

        data["files/0"] = "a.dat"
        data["files/1"] = "b.dat"
        data["files/2"] = "c.dat"

        self.assertEqual(data["files/0"], "a.dat")
        self.assertEqual(data["files/1"], "b.dat")
        self.assertEqual(data["files/2"], "c.dat")
        self.assertTrue(isinstance(data["files"], list))

    def test_8_json_data(self):
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
        self.assertEqual(v, "C/C++")

        data2 = vdict(json_data2)
        v = data2["query/filtered/0/query/match/language"]

        self.assertEqual(v, "Python")

    def test_9_sub_dict(self):
        test_dict = vdict()

        test_dict.a.b=1
        print(test_dict.json())

        test2 = test_dict.a
        print(test2)
        print(test2.__class__)

        test2.b = 2
        print(test_dict)
        print(test2)


        self.assertEqual(test_dict.a.b, test2.b)
        self.assertTrue(isinstance(test2, vdict))

if __name__ == '__main__':
    unittest.main()
