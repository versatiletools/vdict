# vdict (Versatile Dictionary)
Extension of python dict object for JSON data. When you use json file with Python,you should use json module. It is a good module, but it is too difficult to navigate deep json data like to below:

~~~
 "expand": "renderedFields,names,schema,operations,editmeta,changelog,versionedRepresentations",
    "id": "38118",
    "self": "http://jira.mysystem.com/rest/api/latest/issue/38118",
    "key": "TS-17952",
    "fields": {
        "fixVersions": [],
        "customfield_10110": null,
        "customfield_11200": null,
        "resolution": {
            "self": "http://jira.mysystem.com/rest/api/2/resolution/10000",
            "id": "10000",
            "description": "GreenHopper Managed Resolution",
            "name": "Done"
        },
        "issuelinks": [{
            "outwardIssue": {
                "id": "38116",
                "key": "TS-17951",
                "self": "http://jira.mysystem.com/rest/api/2/issue/38116",
                "fields": {
                    "summary": "My work",
                    "status": {
                        "self": "http://jira.mysystem.com/rest/api/2/status/6",
                        "name": "Closed",
                        "id": "6",
                        "statusCategory": {
                            "self": "http://jira.mysystem.com/rest/api/2/statuscategory/3",
                            "id": 3,
~~~
With vdict, you can use it more easer than json module.
