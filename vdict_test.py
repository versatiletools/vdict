#-*- coding: utf-8 -*-

import unittest
from vdict import vdict


class BasicDictinaryFunctionTestCase(unittest.TestCase):
    def test_setget(self):
        test_dict = vdict()

        data = "a"
        test_dict.prop1 = data
        self.assertEqual(data, test_dict.prop1)

        data = {"file1", "file2"}
        test_dict.dir1.files = data
        self.assertEqual(data, test_dict.dir1.files)


class JSONDataTestCase(unittest.TestCase):
    def test_jira_issue(self):
        with open("test-data/jiraissue.json", mode="r", encoding="utf-8") as fp:
            data = ""
            for i, line in enumerate(fp):
                data += line

            json_dict = vdict(data)

        self.assertEqual("PROJ-918", json_dict.key)


if __name__ == '__main__':
    unittest.main()
