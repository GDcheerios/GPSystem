# GPSystem
The Gentry's Quest Rating system

## Installation
unzip source into project.

If you're testing you'll need the [tabulate](https://pypi.org/project/tabulate/) module

## Usage
You can test ratings by running GPmain. It will create a directory named **Data**. You can put *JSON* files containing gentry's quest data inside the directory. Characters are named based off the *JSON* file name.

Testing should result in a table like this:
```
|   rank | player     |   weighted gp |   unweighted gp |
|-------:|:-----------|--------------:|----------------:|
|      1 | coolPlayer |          46.8 |            46.8 |
```

Upon selecting a player you'll get the overview of their different sections like so:
```
|   section number | section type   |   weighted gp |   unweighted gp |
|-----------------:|:---------------|--------------:|----------------:|
|                1 | characters     |          46.8 |            46.8 |
|                2 | artifacts      |           0   |             0   |
|                3 | weapons        |           0   |             0   |
```

The player power rating details are returned from the GPSystem's rater class.

here's an example:
```py
from GPmain import GPSystem
import json

with open("Data/coolPlayer.json", "r") as f:
  player_data = json.loads(f.read())

program = GPSystem()

program.rater.generate_power_details(player_data)
```

result:
```json
{
    "rating":{
        "unweighted":46.8,
        "weighted":46.8
    },
    "totals":{
        "characters":{
            "unweighted":46.8,
            "weighted":46.8
        },
        "weapons":{
            "unweighted":0,
            "weighted":0
        },
        "artifacts":{
            "unweighted":0,
            "weighted":0
        }
    },
    "per object rating":{
        "characters":[
            {
                "cool character":46.8
            }
        ],
        "weapons":[
            
        ],
        "artifacts":[
            
        ]
    }
}
```
