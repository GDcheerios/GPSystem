# GPSystem

The Gentry's Quest Rating system

## Overview

The Gentry's Quest Rating System evaluates and ranks a user's items to determine their **GP (Gentry Points)** and **Ranking**.

### Ratings:

- **Weighted GP**: Prioritizes the user's best items, used for rankings.
- **Unweighted GP**: Total accumulation of all items, not used in rankings to prevent high scores from being inflated by
  quantity over quality.

Using Weighted GP ensures fairness by rewarding players who invest in top-tier items, unlike Unweighted GP which could
favor users with many low-tier items.

## How it works

1. [Factors defined to influence different properties](#defining-factors)
    - [Ranking peaks](#ranking-peaks)
    - [Item type rating info](#item-type-rating-info)
    - [Character rating factors](#character-rating-factors)
    - [Artifact rating factors](#artifact-rating-factors)
    - [Weapon rating factors](#weapon-rating-factors)
    - [Stat rating factors](#stat-rating-factors)
2. [Defining how items are rated](#defining-how-items-are-rated)
    - [Attribute rating](#attributes)
    - [If an item is rateable](#if-an-item-is-rateable)
    - [Character rating](#character-rating)
    - [Artifact rating](#artifact-rating)
    - [Weapon rating](#weapon-rating)
3. [Giving a rank based off points](#giving-a-rank-based-off-points)

___

## Defining factors

All factors are defined inside `GPRater.py` as a static variable.

### Ranking peaks

This is how the ranking values are defined.

`gp_peak` defines how much **minimum** GP is required to become Gentry Warrior.

`get_tiers` retrieves the rankings with their tiers. Inside holds the definition of how much GP a user needs to have to
be a certain ranking.
All the rankings are based off the peak, so it's easier to create relative ranking values.

```py
highest_gp = GPRater.gp_peak

unranked = {
    '1': round(highest_gp * 0)
}

silver = {
    '1': round(highest_gp * 0.1),
    '2': round(highest_gp * 0.115),
    '3': round(highest_gp * 0.130),
    '4': round(highest_gp * 0.145),
    '5': round(highest_gp * 0.16)
}

gentry_warrior = {
    '1': highest_gp
}
```

### Item type rating info

This defines section rating for the weighted GP.

Each section has a `factor` which describes the gradual reduction of that item section's rating A.K.A. where the
weighted rating comes from.

Each section also has a `rating_enabled` which describes whether to apply the section to weighted rating.

`max_item_rating` defines the max amount of items to rate from each section when doing weighted rating.

### Character rating factors

Defines how characters are rated.

`character_star_rating_factor` Defines how many points are given for the character's star rating.

`character_level_factor` Defines how many points are given for the character's star rating.

`character_difficulty_factor` Defines how many points are given for the character's difficulty level.

`character_artifact_factor` Defines bonus points for the character's artifact rating.

`character_weapon_factor` Defines bonus points for the character's weapon rating.

### Artifact rating factors

Defines how artifacts are rated.

`artifact_star_rating_factor` Defines how many points are given for the artifact's star rating.

`artifact_level_factor` Defines how many points are given for the artifact's level.

`artifact_main_attribute_factor` Defines bonus points for the artifact's main attribute.

`artifact_attribute_factor` Defines bonus points for the artifact's attributes.

### Weapon rating factors

Defines how weapons are rated.

`weapon_star_rating_factor` Defines how many points are given for the weapon's star rating.

`weapon_level_factor` Defines how many points are given for the weapon's level.

`weapon_attack_factor` Defines how many points are given for the weapon's damage.

`weapon_attribute_factor` Defines bonus points for the weapon's attribute.

### Stat rating factors

Defines how stats from buffs are rated.

| **ID** | **Stat**       | **Description**   |
|--------|----------------|-------------------|
| 1      | `health`       | Health stat.      |
| 2      | `attack`       | Attack stat.      |
| 3      | `defense`      | Defense stat.     |
| 4      | `crit_rate`    | CritRate stat.    |
| 5      | `crit_damage`  | CritDamage stat.  |
| 6      | `speed`        | Speed stat.       |
| 7      | `attack_speed` | AttackSpeed stat. |
| 8      | `tenacity`     | Tenacity stat.    |

___

## Defining how items are rated

### Attributes

Given an attribute it will check of which type it is, rate it, return the rating.

```py
@staticmethod
def rate_attribute(attribute) -> float:
    rating = 0
    # check attribute type
    # give rating
    return rating
```

### If an item is rateable

To decide whether an item is rateable, the item must have experience.

```py
@staticmethod
def is_ratable(item: dict) -> bool:
    return item["experience"]["xp"] > 0 or item["experience"]["level"] > 1
```

### Character rating

Go through all the character's properties and rate it based on them.

```py
@staticmethod
def get_character_rating(character: dict) -> float:
    character_rating = 0
    difficulty = (character["experience"]["level"] / 20) + 1
    star_rating = character["star rating"] * GPRater.character_star_rating_factor
    level = character["experience"]["level"] * GPRater.character_level_factor
    difficulty = difficulty * GPRater.character_difficulty_factor
    equips = character["equips"]
    for artifact in equips["artifacts"]:
        if artifact:
            character_rating += GPRater.get_artifact_rating(artifact) * GPRater.character_artifact_factor

    try:
        if equips['weapon']:
            character_rating += GPRater.get_weapon_rating(equips['weapon']) * GPRater.character_weapon_factor

    except KeyError:
        pass

    except TypeError:
        pass

    character_rating += difficulty
    character_rating += star_rating
    character_rating += level

    return character_rating
```

### Artifact rating

Go through all the artifact's properties and rate it based on them.

```py
@staticmethod
def get_artifact_rating(artifact: dict) -> float:
    artifact_rating = 0
    star_rating = artifact["star rating"] * GPRater.artifact_star_rating_factor
    level = artifact["experience"]["level"] * GPRater.artifact_level_factor
    main_attribute = GPRater.rate_attribute(
        artifact["stats"]["main attribute"]) * GPRater.artifact_main_attribute_factor
    attributes = []
    for attribute in artifact["stats"]["attributes"]:
        attributes.append(GPRater.rate_attribute(attribute) * GPRater.artifact_attribute_factor)

    artifact_rating += star_rating
    artifact_rating += level
    artifact_rating += main_attribute
    artifact_rating += sum(attributes)

    return artifact_rating
```

### Weapon rating

Go through all the weapon's properties and rate it based on them.

```py
@staticmethod
def get_weapon_rating(weapon: dict) -> float:
    weapon_rating = 0
    star_rating = weapon["star rating"] * GPRater.weapon_star_rating_factor
    level = weapon["experience"]["level"] * GPRater.weapon_level_factor
    buff = GPRater.rate_attribute(weapon["stats"]["buff"]) * GPRater.weapon_attribute_factor
    attack = 0

    weapon_rating += star_rating
    weapon_rating += level
    weapon_rating += attack
    weapon_rating += buff

    return weapon_rating
```

___

## Giving a rank based off points

The `get_rank` method determines a user's rank and tier by comparing their `rating` to predefined thresholds retrieved
from the tier system (`GPRater.get_tiers()`). It iterates through the ranks and tiers, keeping track of the previous
rank and tier as it progresses. When the user's `rating` falls below a threshold, the method assigns the previous rank
and tier, converting the tier into a Roman numeral format. Special handling is included for the `"gentry warrior"` rank,
where the tier is dynamically calculated. The method ultimately returns the user's rank and its corresponding tier in
Roman numeral format.

```py
@staticmethod
def get_rank(rating: int) -> tuple:
    def int_to_roman(num: int) -> str:
        if not 0 < num < 4000:
            raise ValueError("Input must be an integer between 1 and 3999.")

        roman_numerals = {10: 'X', 5: 'V', 4: 'IV', 1: 'I'}

        roman_str = ""
        for value, numeral in roman_numerals.items():
            while num >= value:
                roman_str += numeral
                num -= value

        return roman_str

    tiers = GPRater.get_tiers()

    for rank, levels in tiers.items():
        for tier, threshold in levels.items():
            if rating < threshold:
                return previous_rank, int_to_roman(int(previous_tier))

            previous_rank, previous_tier = rank, tier

    if previous_rank == "gentry warrior":
        warrior_tier = (rating // tiers["gentry warrior"]["1"])
        return "gentry warrior", int_to_roman(warrior_tier)

    return previous_rank, int_to_roman(int(previous_tier))
```
