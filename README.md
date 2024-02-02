# GPSystem
The Gentry's Quest Rating system

## Installation
unzip source into project.

or use `pip install git+https://github.com/GDcheeriosYT/GPSystem.git`

If you're testing you'll need the [tabulate](https://pypi.org/project/tabulate/) module

## Usage
You can test ratings by running GPmain. It will create a directory named **Data**. You can put *JSON* files containing gentry's quest data inside the directory. Characters are named based off the *JSON* file name.

Testing should result in a table like this:
```
|   rank | player     |   weighted gp |   unweighted gp |
|-------:|:-----------|--------------:|----------------:|
|      1 | GDcheerios |        841.65 |           848.2 |
```

Upon selecting a player you'll get the overview of their different sections like so:
```
|   section number | section type   |   weighted gp |   unweighted gp |
|-----------------:|:---------------|--------------:|----------------:|
|                1 | characters     |       797.046 |           803.6 |
|                2 | artifacts      |        44.6   |            44.6 |
|                3 | weapons        |         0     |             0   |
```

The player power rating details are returned from the GPSystem's rater class.

here's an example:
```py
from GPmain import GPSystem
import json

with open("Data/GDcheerios.json", "r") as f:
  player_data = json.loads(f.read())

program = GPSystem()

program.rater.generate_power_details(player_data)
```

result:
```json
{
    "rating":{
        "unweighted":848.2,
        "weighted":841.65
    },
    "totals":{
        "characters":{
            "unweighted":803.6,
            "weighted":797.0464374999999
        },
        "weapons":{
            "unweighted":0,
            "weighted":0
        },
        "artifacts":{
            "unweighted":44.6,
            "weighted":44.6
        }
    },
    "per object rating":{
        "characters":[
            {
                "Brayden Messerschmidt":14.5
            },
            {
                "Kelly Krysa":21.5
            },
            {
                "Gavin Knudsen":28.5
            },
            {
                "Matheu Sliger":739.1
            }
        ],
        "weapons":[
            
        ],
        "artifacts":[
            {
                "Budweiser":13.8
            },
            {
                "Pepsi Bottle":13.8
            },
            {
                "Angry Anubis":17.0
            }
        ]
    }
}
```
