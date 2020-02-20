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
        list_data = vdict([1, 2, "3"])
        dict_data = vdict({"a": 1, "b": 2, "c": "3"})

        print(f"list_data[0]   = {list_data[0]}")
        print(f"list_data[1]   = {list_data[1]}")
        print(f"list_data[2]   = {list_data[2]}")
        print(f"list_data['0'] = {list_data['0']}")
        print(f"list_data['1'] = {list_data['1']}")
        print(f"list_data['2'] = {list_data['2']}")

        self.assertRaises(Exception, list_data["a"])
        self.assertRaises(Exception, list_data.a)

    def test_3_errors(self):
        test_dict = vdict()

        test_dict.a = 1
        with self.assertRaises(KeyError):
            test_dict['b']
        self.assertIsNone(test_dict.get('b'))
        self.assertEqual({}, test_dict.b)

        test_dict.attr1.attr2.attr3 = 1
        test_dict.attr1.attr2.attr4 = 2

        with self.assertRaises(KeyError):
            test_dict["attr1/attr2/attr5"]

        with self.assertRaises(KeyError):
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

        info = vdict()
        info["name"] = name

        data3 = {"phone": "123-4567", "addr": {"city": "Seoul", "country": "Korea"}}
        info["etc"] = data3

        self.assertEqual(info["name/given"], "Sungho")
        self.assertEqual(info["name/family"], "Park")
        self.assertEqual(info["name"], name)
        self.assertEqual(info["name/addr/city"], "Seoul")

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


#     def test_setget(self):
#         test_dict = vdict()
#
#         data = "a"
#         test_dict.prop1 = data
#         self.assertEqual(data, test_dict.prop1)
#
#         data = {"file1", "file2"}
#         test_dict.dir1.files = data
#         self.assertEqual(data, test_dict.dir1.files)
#
#     def test_compatibility_with_dict(self):
#         a = vdict(one=1, two=2, three=3)
#         b = {'one': 1, 'two': 2, 'three': 3}
#         c = vdict(zip(['one', 'two', 'three'], [1, 2, 3]))
#         d = vdict([('two', 2), ('one', 1), ('three', 3)])
#         e = vdict({'three': 3, 'one': 1, 'two': 2})
#         self.assertEqual(True, a == b == c == d == e)
#
#     def test_combination(self):
#         a1 = vdict()
#         a2 = vdict()
#         b = vdict()
#
#
#         a1["key1"] = "value1"
#         a2["subkey1"] = "subvalue1"
#         a1["key2"] = a2
#
#         b["key2/subkey1"] = "subvalue1"
#
#         self.assertEqual(a1["key2/subkey1"], b["key2/subkey1"])
#
#
# class JSONDataTestCase(unittest.TestCase):
#     def test_jira_issue(self):
#         with open("test-data/jiraissue.json", mode="r", encoding="utf-8") as fp:
#             data = ""
#             for i, line in enumerate(fp):
#                 data += line
#
#             json_dict = vdict(data)
#
#         self.assertEqual("PROJ-918", json_dict.key)


if __name__ == '__main__':
    unittest.main()
