import unittest
from vdict import vdict

json_data = """
{
    "glossary": {
        "title": "example glossary",
		"GlossDiv": {
            "title": "S",
			"GlossList": {
                "GlossEntry": {
                    "ID": "SGML",
					"SortAs": "SGML",
					"GlossTerm": "Standard Generalized Markup Language",
					"Acronym": "SGML",
					"Abbrev": "ISO 8879:1986",
					"GlossDef": {
                        "para": "A meta-markup language, used to create markup languages such as DocBook.",
						"GlossSeeAlso": ["GML", "XML"]
                    },
					"GlossSee": "markup"
                }
            }
        }
    }
}
"""

list_data = [1,2,3,4,5]

dict_data = {'a': 'A', 'b': 'B'}


class MyTestCase(unittest.TestCase):
    def test_string_parameters(self):
        target = vdict(json_data)

        v = target["glossary/GlossDiv/GlossList/GlossEntry"]

        self.assertEqual(dict, type(v))

    def test_dict_parameters(self):
        target = vdict(dict_data)

        v = target.get()
        self.assertEqual(dict, type(v))

        for i in dict_data.keys():
            self.assertEqual(dict_data[i], target[i])

    # def test_list_parameters(self):
    #     target = vdict(list_data)
    #
    #     self.assertEqual(list, target.get())
    #
    #     for i in range(0, len(list_data)):
    #         self.assertEqual(list_data[i], target[i])


if __name__ == '__main__':
    unittest.main()
