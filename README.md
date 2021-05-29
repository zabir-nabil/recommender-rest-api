# recommender-rest-api

### Data schema

```
[
{ "strIdent": "-DfX3_CO2bU", "intTimestamp": 1617826241445, "strTitle": "Why you don't need certainty to be influential", "intCount": 1 },
{ ... },
{ ... },
...
]
```
#### Request schema

Each POST request should send data in json format with following structure:

```
data = {
       "userIdent" : "someUniqueStringToIdentifyUser",
       "userHistory":
       [
            { "strIdent": "-DfX3_CO2bU", "intTimestamp": 1617826241445, "strTitle": "Why you don't need certainty to be influential", "intCount": 1 },
            { ... },
            { ... },
            ...
        ]

}
```

* `userIdent` : user_ID

* `strIdent` : video_ID

* `strTitle` : video_title

* `intTimestamp` : integer_timestamp # we can retrieve the actual timestamp from this for additional feature

* `intCount` : number_of_views

