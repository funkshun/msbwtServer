# msBWT Server

## msBWT Name Resolution and Web Service

msbwtServer provides a lightweight management server for instances of [msbwtCloud](https://github.com/funkshun/msbwtCloud).
msbwtServer provides name resolution, data validation, and query composition for remote msBWTs.

## Installation

- Clone this repository on to the device hosting the BWT datastructure.
- Rename `def_config.py` to `config.py` and change values to match desired values
- Run `python setup.py install`
- Run `waitress-serve --call 'msbwtCloud:create_app'` to create server on port 8080

## msBWTCloud

msBWTCloud provides the primary interface for interacting with remote BWT data structures. The following functions are exposed at:

`/<function_name>?args=[args_list]&kwargs={kwargs_list}`

### Status Codes

`202`: Query properly received and queued  
`400`: Improper arguments  
`404`: Function not found

### Additional Flags

`async`: set this to true to enable the non-blocking functionality of the server. Omitting this flag or a false value will default to legacy blocking behavior for compatibility.

### countOccurrencesOfSeq

Queries the number of times a sequence occurrs in the target dataset.

- Arguments  
    `seq::String`: the target sequence to be counted  
    `givenRange::(Long, Long)`: (OPTIONAL) Restricts the query to the given range
- Sample Call  
`http://test.test/countOccurrencesOfSeq?args=["CATAGAT"]`  
Queries the number of occurrences of `CATAGAT` between
`1346091641L` and `15700916349L` in the dataset held by `test.test`

### recoverString

Queries the string at the index given in the target dataset.

- Arguments  
    `index::Integer`: the target sequence to be counted  
- Sample Call  
`http://test.test/recoverString?args=[426689]`  
Queries the string at index `426689` in the dataset held by `test.test`

### findIndicesOfStr

Queries the index if the given string.

- Arguments  
    `seq::String`: the target sequence to be counted  
    `givenRange::(Long, Long)`: (OPTIONAL) Restricts the query to the given range  
- Sample Call  
`http://test.test/findIndicesOfStr?args=["CATAGAT"]`  
Queries the dataset for the index for the string `CATAGAT` in the dataset held by `test.test`

### getSequenceDollarID

Queries the BWT end marker index for the given sequence

- Arguments  
    `seq::String`: the target sequence to be counted  
    `returnOffset::Boolean`: (OPTIONAL - defaults to false) True will query the offset
- Sample Call  
`http://test.test/getSequenceDollarID?args=["CATAGAT"]`  
Queries the dataset for the index for the string `CATAGAT` in the dataset held by `test.test`

### Optional Arguments

Optional arguments may be specified as an additional url parameter in the form:  
`&argument_name=argument_value`  
after the `args` parameter

#### Example

`http://test.test/getSequenceDollarID?args=["CATAGAT"]&returnOffset=True`

### Batch Queries

The following batch functions queue several queries of the same type under a single token

#### batchRecoverString

Queries all strings in the given range of indices

- Arguments  
    `startIndex:Long`: the start of the range of indices to be queried  
    `endIndex:Long`: the end of the range of indices to be queried  
    `returnOffset::Boolean`: (OPTIONAL - defaults to false) True will query the offset
- Sample Call  
`http://test.test/batchRecoverString?args=[1346091641L, 15700916349L]`

#### batchCountOccurrencesOfSeq

Queries counts of a list of sequences

- Arguments  
    `seqList::List<String>`: List of sequences to be counted  
    `givenRange::(Long, Long)`: (OPTIONAL) Restricts the query to the given range
- Sample Call  
`http://test.test/batchCountOccurrencesOfSeq?args=["CATAGAT", "GATTACA"]`

#### batchFastCountOccurrences

Optimized Routine to count occurrences of a list of sequences

- Arguments  
    `seqList::List<String>`: List of sequences to be counted  
- Sample Call  
`http://test.test/batchFastCountOccurrences?args=['CATAGAT', 'GATTACA']`

### Return Structure

#### Legacy Behavior

The default behavior of this server emulates the functionality of previous implementations for compatibility.
To enable the non-blocking features, pass the argument `async=true` in the API call.
Queries made without the `async` flag will not be stored and the results are not retrievable outside of the initial return.  
The legacy return is a json structure.

```json
    {
        "result": "Return Value"
    }
```

#### Async Behavior

If the `async` flag is set to true, the functions above do not directly return their results to prevent blocking on long running calls.
Instead, a token is given that can be used to retrieve the status of a query.  

#### Sample Return JSON for countOccurrencesOfSeq

```json
{
    "function": "countOccurrencesOfSeq",
    "token"   : "SqFg2Pjrko8qhFz",
    "args"    : ["CATAGAT"],
    "kwargs"  : {},
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male",
                "load"        : 4
    }
}
```

### Obtaining Results

The status of a query can be obtained using the token value returned by the above functions. The token is passed to the url:  

`/results/<token>`

#### Return Status Codes

`200`: Successfully retrieved token status  
`404`: Token not found  

#### Sample Results JSON for Running Query

``` json
{
    "date"    : "01/01/1990, 00:00:00",
    "function" : "countOccurrencesOfSeq",
    "args"    : ["CATAGAT"],
    "kwargs"  : {},
    "status"  : "RUNNING",
    "result"  : null,
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male",
                "load"        : 4
    }
}
```

#### Sample Results JSON for Successful Quey

```json
{
    "date"    : "01/01/1990, 00:00:00",
    "function" : "countOccurrencesOfSeq",
    "args"    : ["CATAGAT"],
    "kwargs"  : {},
    "status"  : "SUCCESS",
    "result"  : 9327856,
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male",
                "load"        : 4
    }
}
```

#### Sample Results JSON for Failed Quey

``` json
{
    "date"    : "01/01/1990, 00:00:00",
    "function" : "countOccurrencesOfSeq",
    "args"    : ["CATAGAT", "TAGA", "GATACCA"],
    "kwargs"  : {},
    "status"  : "FAILED",
    "result"  : "ValueError: countOccurrencesOfSeq takes exactly one argument",
    "data"    :{
                "name"        : "CC027M756_UNC_NYGC",
                "description" : "Collaborative Cross Dataset 27 Male",
                "load"        : 4
    }
}
```
