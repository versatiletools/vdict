# Overview
## What is vdict?
vdict(Versatile Dictionary) is a extension of python dict object for manipulate structured data such as a JSON data.

## Why use this?

When we use a dict object to manipulate JSON data in python, it's not comfortable because many JSON data have nested structure.

For example,

    json_data = """{
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
    
    json_dict = json.load(json_data)

If we want to get the value of 'description', we write the code like the following

    value = json_dict['query']['filtered']['query']['match']['description']

If the JSON is complicated, it makes our head complicated. Therefore we need more easy dictionary class for our head.

# How to use

## Getting value

You can't avoid to use key names of JSON, but now you can avoid to use redundant square brackets with vdict.

    value = json_dict['query/filtered/query/match/language']

You can access array of JSON.

    json_data = """
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
    
    # value is 'Python'
    value = vdict["query/filtered/0/query/match/language"]
    

## Setting value

You can set data to dictionary. Especially, you can set data in nested keys.

    v_dict = vdict()
    
    v_dict["query/sql/0/select"] = "name, address, phone"
    v_dict["query/sql/1"] = new_select
    v_dict["query/filtered"] = new_filter


## Support data format
- JSON formats are supported.
