from vdict.vdict import vdict

import json


data = """
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

dict_obj = json.loads(data)
vdict_obj = vdict(data, True)

print(vdict_obj.get("glossary/title"))
print(vdict_obj["glossary/title"])


try:
    print("dict with noidex: ", dict_obj["glossary/test"])
except BaseException as e:
    print(e)

try:
    print("vdict with noidex: ", vdict_obj["glossary/test"])
except BaseException as e:
    print(e)

print("dict with noidex: ", vdict_obj.get("glossary/test"))

vdict_obj["glossary/test"] = dict_obj
print(vdict_obj["glossary/test"])
print(vdict_obj)

print(len(vdict_obj["glossary"]))