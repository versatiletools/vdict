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

data2 = '{ "type": "CONNECT" }'

# from addict import Dict
#
# data = Dict()
# data.a="data a"
# print(data.a)
# print(data["a"])
# print(data["b"])
#
# data.b.c="data c"
# print(data.b.__class__)
# print(data.b.c)
#
# exit(0)

from vdict.vdict import vdict
test_dict = vdict()

test_dict.attr1 = "test data"
print(f"test_dict.attr1={test_dict.attr1}")
print(f"test_dict.attr1={test_dict['attr1']}")

test_dict.attr2.attr3.a="a"
print(f"test_dict.attr2.attr3.a={test_dict.attr2.attr3.a}")

test_dict.attr1.b="c"
exit(0)

data = vdict(data)
data.a="data a"
print(f"data.a={data.a}")
print(f"data['a'] = {data['a']}")

exit(0)
data.b.c="data c"


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