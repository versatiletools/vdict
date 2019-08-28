# Overview
## What is vdict?
vdict(Versatile Dictionary) is a extension of python dict object for JSON data.

## Why use this?

When we use dict object to manipulate JSON data in python. But it's not comfortable because JSON data contains nested and nested data.

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

You can't avoid to use key names of JSON, but now you can avoid to use redundant square brackets.

    value = v_dict['query/filtered/query/match/description']
    value = v_dict.query.filtered.query.match.description
    # exception will be thrown if there are many 'description' data
    value = v_dict.by_name('description') 
    value = v_dict.by_name('match/description')
    value = v_dict.by_name('query/*/description')
    value = v_dict.by_name('query/*/match/description')

You can access array of JSON.

    json_data = """{
        "query": {
            "filtered": {
                "query": {
                    "match": {"language": "Python"}
                },
                "filter": {
                    "term": {"created": "2019-03-05"}
                }
            },
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
    
    # value is 'Python'
    value = v_dict["query/filtered/0/query/match/language"]
    value = v_dict.query.filtered[0].query.match.description
    

With a value, we can find the keys that contain the value.

    keys = v_dict.by_value('Mats')

## Setting value

You can set data to dictionary. Especially, you can set data in nested keys.

    v_dict = vdict()
    
    v_dict["query/sql/0/select"] = "name, address, phone"
    v_dict.query.sql[0].select = "name, address, phone"
    
    v_dict["query/sql/1"] = new_vdict
    v_dict["query/sql"].add(new_vdict)
    v_dict["query/filtered"].add(new_filter)
    v_dict.query.filtered.add(new_filter)

## Filtering values

    filtered_vdict = v_dict.filter(key="language").filter(value="Python")
    filtered_vdict = v_dict.filter(key="language", value="Python")

## Short cut

    yaml_data =
    """
    query: 
      filtered: 
        query: 
    	    match: 
            language: Python
          filter: 
              term: 
                created: 2019-03-05
      filtered: 
        query: 
          match: 
            language: C/C++
          filter: 
            term: 
              created: 2018-11-23
    """
    
    v_dict.add_shortcut("query/sql/query/0/match/language", language)
    language = v_dict.language
    
    v_dict.add_shortcut("query/sql/query", query)  # key name 'query' is duplicated yaml's 'query' key.
    v_dict.add_shortcut("query/sql/query", querylist)  # key name 'query' is duplicated yaml's 'query' key.
    
    first_query = v_dict.querylist[0]
    first_query = v_dict["querylist/0"] # can't use this form.

## Support data format
- YAML, JSON formats are supported.

