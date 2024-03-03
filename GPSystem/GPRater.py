import json


class GPRater:
    # ranking
    gp_peak = 10000

    rating_colors = {
        "unranked": "#082b3b",
        "copper": "red",
        "bronze": "brown",
        "silver": "gray",
        "gold": "gold",
        "platinum": "blue",
        "diamond": "cyan",
        "champion": "purple",
        "gentry warrior": "lime",
    }

    @staticmethod
    def get_tiers() -> dict:
        highest_gp = GPRater.gp_peak

        unranked = {
            '1': round(highest_gp * 0)
        }

        copper = {
            '1': round(highest_gp * 0.03),
            '2': round(highest_gp * 0.0325),
            '3': round(highest_gp * 0.035),
            '4': round(highest_gp * 0.0375),
            '5': round(highest_gp * 0.04),
        }

        bronze = {
            '1': round(highest_gp * 0.05),
            '2': round(highest_gp * 0.06),
            '3': round(highest_gp * 0.07),
            '4': round(highest_gp * 0.08),
            '5': round(highest_gp * 0.09),
        }

        silver = {
            '1': round(highest_gp * 0.1),
            '2': round(highest_gp * 0.115),
            '3': round(highest_gp * 0.130),
            '4': round(highest_gp * 0.145),
            '5': round(highest_gp * 0.16),
        }

        gold = {
            '1': round(highest_gp * 0.18),
            '2': round(highest_gp * 0.2),
            '3': round(highest_gp * 0.22),
            '4': round(highest_gp * 0.24),
            '5': round(highest_gp * 0.26)
        }

        platinum = {
            '1': round(highest_gp * 0.3),
            '2': round(highest_gp * 0.34),
            '3': round(highest_gp * 0.38),
            '4': round(highest_gp * 0.42)
        }

        diamond = {
            '1': round(highest_gp * 0.5),
            '2': round(highest_gp * 0.58),
            '3': round(highest_gp * 0.64)
        }

        champion = {
            '1': round(highest_gp * 0.8)
        }

        gentry_warrior = {
            '1': highest_gp
        }

        return {
            'unranked': unranked,
            'copper': copper,
            'bronze': bronze,
            'silver': silver,
            'gold': gold,
            'platinum': platinum,
            'diamond': diamond,
            'champion': champion,
            'gentry warrior': gentry_warrior,
        }

    # section factors
    character_factor = 0.95
    character_rating_enabled = True
    artifact_factor = 0.5
    artifact_rating_enabled = True
    weapon_factor = 0.85
    weapon_rating_enabled = True

    # character factors
    character_star_rating_factor = 4
    character_level_factor = 1.5
    character_difficulty_factor = 14.5

    # artifact factors
    artifact_star_rating_factor = 2
    artifact_level_factor = 1.2

    # weapon factors
    weapon_star_rating_factor = 2
    weapon_level_factor = 1.5
    weapon_attack_factor = 0.2

    @staticmethod
    def generate_power_details(json_data, integer_values: bool = False) -> dict:
        details = {
            'version': 'Classic',
            'rating': {
                'unweighted': 0,
                'weighted': 0
            },
            'ranking': {
                'rank': 'unranked',
                'tier': ''
            },
            'totals': {
                'characters': {
                    'unweighted': 0,
                    'weighted': 0
                },
                'weapons': {
                    'unweighted': 0,
                    'weighted': 0
                },
                'artifacts': {
                    'unweighted': 0,
                    'weighted': 0
                }
            },
            'per object rating': {
                'characters': [],
                'weapons': [],
                'artifacts': []
            }
        }

        def attribute_rater(attribute):
            rating = 0

            health = 1.5
            attack = 4
            defense = 1.2
            crit_rate = 5
            crit_damage = 4.5

            try:
                if isinstance(attribute, dict):
                    attribute = attribute["buff"]

                if attribute[0] == 1:  # health
                    rating += attribute[2] * health

                elif attribute[0] == 2:  # attack
                    rating += attribute[2] * attack

                elif attribute[0] == 3:  # defense
                    rating += attribute[2] * defense

                elif attribute[0] == 4:  # crit rate
                    rating += attribute[2] * crit_rate

                elif attribute[0] == 5:  # crit damage
                    rating += attribute[2] * crit_damage
            except KeyError:
                details['version'] = "Ursina"
                if attribute['stat'] == 'Health':
                    rating += attribute['level'] * health
                elif attribute['stat'] == 'Attack':
                    rating += attribute['level'] * attack
                elif attribute['stat'] == 'Defense':
                    rating += attribute['level'] * defense
                elif attribute['stat'] == 'CritRate':
                    rating += attribute['level'] * crit_rate
                elif attribute['stat'] == 'CritDamage':
                    rating += attribute['level'] * crit_damage
                else:
                    rating += attribute['level']

            return rating

        power_level = 0

        def check_xp(object):
            return object["experience"]["xp"] > 0 or object["experience"]["level"] > 1

        def rate_artifact(artifact, is_equipped = False):
            if artifact:
                artifact_details = {
                    "rating": 0,
                    "name": artifact["name"],
                    "star_rating": 0,
                    "level": 0,
                    "main attribute": 0,
                    "attributes": 0
                }

                artifact_rating = 0
                star_rating = artifact["star rating"] * GPRater.artifact_star_rating_factor
                level = artifact["experience"]["level"] * GPRater.artifact_level_factor
                main_attribute = attribute_rater(artifact["stats"]["main attribute"])
                attributes = []
                for attribute in artifact["stats"]["attributes"]:
                    attributes.append(attribute_rater(attribute))

                artifact_rating += star_rating
                artifact_rating += level
                artifact_rating += main_attribute
                artifact_rating += sum(attributes)

                artifact_details["rating"] = artifact_rating if (check_xp(artifact) or is_equipped) else 0
                artifact_details["star_rating"] = star_rating
                artifact_details["level"] = level
                artifact_details["main attribute"] = main_attribute
                artifact_details["attributes"] = sum(attributes)

                return artifact_details

        def rate_weapon(weapon, is_equipped = False):
            weapon_details = {
                "rating": 0,
                "name": weapon["name"],
                "star_rating": 0,
                "attack": 0,
                "level": 0,
                "buff": 0
            }

            weapon_rating = 0
            star_rating = weapon["star rating"] * GPRater.weapon_star_rating_factor
            level = weapon["experience"]["level"] * GPRater.weapon_level_factor
            attack = 0

            try:
                attack = weapon["stats"]["attack"] * GPRater.weapon_attack_factor
                weapon_details["attack"] = attack
            except KeyError:  # gentry's quest classic only uses this
                details['version'] = "Ursina"
                pass

            weapon_rating += star_rating
            weapon_rating += level
            weapon_rating += attack

            weapon_details["rating"] = weapon_rating if (check_xp(weapon) or is_equipped) else 0

            return weapon_details

        def rate_character(character):
            character_details = {
                "rating": 0,
                "name": character["name"],
                "star_rating": 0,
                "level": 0,
                "difficulty": 0,
                "weapon": None,
                "artifacts": None
            }

            character_rating = 0
            difficulty = (character["experience"]["level"] / 20) + 1
            star_rating = character["star rating"] * GPRater.character_star_rating_factor
            level = character["experience"]["level"] * GPRater.character_level_factor
            difficulty = difficulty * GPRater.character_difficulty_factor
            equips = character["equips"]
            weapon_rating = 0
            artifacts = []
            artifact_rating = 0
            for artifact in equips["artifacts"]:
                if artifact:
                    rating_details = rate_artifact(artifact, True)
                    artifact_rating += rating_details["rating"]
                    artifacts.append(rating_details)

            character_details["artifacts"] = artifacts

            try:
                if equips['weapon']:
                    rating_details = rate_weapon(equips["weapon"], True)
                    weapon_rating = rating_details["rating"]
                    character_details['weapon'] = rating_details

            except KeyError:
                pass

            except TypeError:
                pass

            character_rating += difficulty
            character_rating += star_rating
            character_rating += level
            character_rating += weapon_rating
            character_rating += artifact_rating

            character_details["rating"] = character_rating if check_xp(character) else 0
            character_details["star_rating"] = character["star rating"] * GPRater.character_star_rating_factor
            character_details["level"] = character["experience"]["level"] * GPRater.character_level_factor
            character_details["difficulty"] = difficulty * GPRater.character_difficulty_factor

            return character_details

        # characters
        character_ratings = [rate_character(character) for character in json_data["inventory"]["characters"]]
        character_ratings.sort(key=lambda x: x["rating"], reverse=True)
        details['per object rating']['characters'] = character_ratings

        # artifacts
        artifact_ratings = [rate_artifact(artifact) for artifact in json_data["inventory"]["artifacts"]]
        artifact_ratings.sort(key=lambda x: x["rating"], reverse=True)
        details['per object rating']['artifacts'] = artifact_ratings

        # weapons
        weapon_ratings = [rate_weapon(weapon) for weapon in json_data["inventory"]["weapons"]]
        weapon_ratings.sort(key=lambda x: x["rating"], reverse=True)
        details['per object rating']['weapons'] = weapon_ratings

        def get_rating(rating_details):
            return rating_details["rating"]

        def get_ratings(entity_list: list, get_index: bool = False):
            ratings = []
            for entity in entity_list:
                ratings.append((get_rating(entity), entity_list.index(entity))) if get_index else ratings.append(get_rating(entity))

            ratings.sort()

            return ratings

        details['totals']['characters']['unweighted'] = (int(sum(get_ratings(character_ratings))) if integer_values else round(sum(get_ratings(character_ratings)), 2)) if GPRater.character_rating_enabled else 0
        details['totals']['artifacts']['unweighted'] = (int(sum(get_ratings(artifact_ratings))) if integer_values else round(sum(get_ratings(artifact_ratings)), 2)) if GPRater.artifact_rating_enabled else 0
        details['totals']['weapons']['unweighted'] = (int(sum(get_ratings(weapon_ratings))) if integer_values else round(sum(get_ratings(weapon_ratings)), 2)) if GPRater.weapon_rating_enabled else 0

        def weight_rater(object_rating, factor, index):
            return object_rating * (factor ** index)

        section_pl = 0
        if GPRater.character_rating_enabled:
            for character_rating in get_ratings(character_ratings, True):
                rating = weight_rater(character_rating[0], GPRater.character_factor, character_rating[1])
                section_pl += rating
                power_level += rating

            details['totals']['characters']['weighted'] = int(section_pl) if integer_values else round(section_pl, 2)
        else:
            details['totals']['characters']['weighted'] = 0

        section_pl = 0
        if GPRater.artifact_rating_enabled:
            for artifact_rating in get_ratings(artifact_ratings, True):
                rating = weight_rater(artifact_rating[0], GPRater.artifact_factor, artifact_rating[1])
                section_pl += rating
                power_level += rating

            details['totals']['artifacts']['weighted'] = int(section_pl) if integer_values else round(section_pl, 2)
        else:
            details['totals']['artifacts']['weighted'] = 0

        section_pl = 0
        if GPRater.weapon_rating_enabled:
            for weapon_rating in get_ratings(weapon_ratings, True):
                rating = weight_rater(weapon_rating[0], GPRater.weapon_factor, weapon_rating[1])
                section_pl += rating
                power_level += rating

            details['totals']['weapons']['weighted'] = int(section_pl) if integer_values else round(section_pl, 2)
        else:
            details['totals']['weapons']['weighted'] = 0

        if integer_values:
            unweighted = int(
                details['totals']['characters']['unweighted'] +
                details['totals']['artifacts']['unweighted'] +
                details['totals']['weapons']['unweighted']
            )
            weighted = int(power_level)
        else:
            unweighted = round(
                details['totals']['characters']['unweighted'] +
                details['totals']['artifacts']['unweighted'] +
                details['totals']['weapons']['unweighted'],
                2
            )
            weighted = round(power_level, 2)

        details['rating']['unweighted'] = unweighted
        details['rating']['weighted'] = weighted

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

        rank = 'unranked', ''

        for tier_name, tier_values in reversed(GPRater.get_tiers().items()):
            for tier_value, gp_value in reversed(tier_values.items()):
                if weighted >= gp_value:
                    if tier_name == "gentry warrior":
                        print(weighted, tier_value)
                        print(int((weighted/int(tier_value))))
                        rank = tier_name, int_to_roman(int((weighted/int(gp_value)) + 1))
                    else:
                        rank = tier_name, int_to_roman(int(tier_value))
                    break

            if rank[0] != 'unranked':
                break

        details['ranking']['rank'] = rank[0]
        details['ranking']['tier'] = rank[1]

        return details
