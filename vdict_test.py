#-*- coding: utf-8 -*-

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

        print(f"dict_data['a']   = {dict_data['a']}")
        print(f"dict_data['b']   = {dict_data['b']}")
        print(f"dict_data['c']   = {dict_data['c']}")

        self.assertRaises(Exception, dict_data["a"])
        self.assertRaises(Exception, dict_data.a)

        json_dict = vdict('{ "type": "CONNECT" }')
        self.assertEqual(json_dict["type"], "CONNECT")

    def test_3_errors(self):
        test_dict = vdict()

        test_dict.a = 1

        self.assertRaises(KeyError, test_dict['b'])
        self.assertIsNone(test_dict.get('b'))
        self.assertEqual({}, test_dict.b)

        test_dict.attr1.attr2.attr3 = 1
        test_dict.attr1.attr2.attr4 = 2

        self.assertRaises(KeyError, test_dict["attr1/attr2/attr5"])
        self.assertRaises(KeyError, test_dict["attr1.attr3.attr2"])

        self.assertIsNone(test_dict.get("attr1/attr2/attr5"))
        self.assertIsNone(test_dict.get("attr1.attr3.attr2"))
        self.assertEqual({}, test_dict.attr1.attr2.attr5)
        self.assertEqual({}, test_dict.attr1.attr3.attr2)

        try:
            test_dict.attr1.attr2.attr3.new_data = 1
            self.fail("AttributeError must be raised.")
        except Exception as e:
            self.assertRaises(AttributeError, e)

    def test_5_setget_by_braces(self):
        name = vdict()

        name["given"] = "Sungho"
        name["family"] = "Park"
        name["addr/city"] = "Seoul"
        try:
            name["family/first"] = "Junha"
            self.fail("Must fail to assign data to object which is not a container.")
        except TypeError:
            pass

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
        test_dict.attr1.attr2.attr3={"item1": 1, "item2": 2}
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


if __name__ == '__main__':
    unittest.main()
