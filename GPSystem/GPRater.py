import json


class GPRater:
    # ranking
    gp_peak = 3000

    @staticmethod
    def get_tiers() -> dict:
        highest_gp = GPRater.gp_peak
        copper = {
            '1': round(highest_gp * 0.06),
            '2': round(highest_gp * 0.07),
            '3': round(highest_gp * 0.08),
            '4': round(highest_gp * 0.09),
            '5': round(highest_gp * 0.1),
        }

        bronze = {
            '1': round(highest_gp * 0.12),
            '2': round(highest_gp * 0.14),
            '3': round(highest_gp * 0.16),
            '4': round(highest_gp * 0.18),
            '5': round(highest_gp * 0.2),
        }

        silver = {
            '1': round(highest_gp * 0.22),
            '2': round(highest_gp * 0.24),
            '3': round(highest_gp * 0.26),
            '4': round(highest_gp * 0.28),
            '5': round(highest_gp * 0.3),
        }

        gold = {
            '1': round(highest_gp * 0.35),
            '2': round(highest_gp * 0.4),
            '3': round(highest_gp * 0.45),
            '4': round(highest_gp * 0.5),
            '5': round(highest_gp * 0.55),
        }

        platinum = {
            '1': round(highest_gp * 0.6),
            '2': round(highest_gp * 0.7),
            '3': round(highest_gp * 0.8),
        }

        diamond = {
            '1': round(highest_gp * 0.9),
            '2': round(highest_gp * 0.95)
        }

        gentry_warrior = {
            'gentry warrior': highest_gp
        }

        return {
            'copper': copper,
            'bronze': bronze,
            'silver': silver,
            'gold': gold,
            'platinum': platinum,
            'diamond': diamond,
            'gentry warrior': gentry_warrior,
        }

    # section factors
    character_factor = 0.95
    character_rating_enabled = True
    artifact_factor = 0.95
    artifact_rating_enabled = False
    weapon_factor = 0.95
    weapon_rating_enabled = False

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
            attack = 2.5
            defense = 2
            crit_rate = 4
            crit_damage = 3

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

        def rate_artifact(artifact):
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

                artifact_details["rating"] = artifact_rating
                artifact_details["star_rating"] = star_rating
                artifact_details["level"] = level
                artifact_details["main attribute"] = main_attribute
                artifact_details["attributes"] = sum(attributes)

                return artifact_details

        def rate_weapon(weapon):
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

            weapon_details["rating"] = weapon_rating

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
                    rating_details = rate_artifact(artifact)
                    artifact_rating += rating_details["rating"]
                    artifacts.append(rating_details)

            character_details["artifacts"] = artifacts

            try:
                if equips['weapon']:
                    rating_details = rate_weapon(equips["weapon"])
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

            character_details["rating"] = character_rating
            character_details["star_rating"] = character["star rating"] * GPRater.character_star_rating_factor
            character_details["level"] = character["experience"]["level"] * GPRater.character_level_factor
            character_details["difficulty"] = difficulty * GPRater.character_difficulty_factor

            return character_details

        # characters
        character_ratings = [rate_character(character) for character in json_data["inventory"]["characters"]]
        character_ratings.sort(key=lambda x: x["rating"])
        details['per object rating']['characters'] = character_ratings

        # artifacts
        artifact_ratings = [rate_artifact(artifact) for artifact in json_data["inventory"]["artifacts"]]
        artifact_ratings.sort(key=lambda x: x["rating"])
        details['per object rating']['artifacts'] = artifact_ratings

        # weapons
        weapon_ratings = [rate_weapon(weapon) for weapon in json_data["inventory"]["weapons"]]
        weapon_ratings.sort(key=lambda x: x["rating"])
        details['per object rating']['weapons'] = weapon_ratings

        def get_rating(rating_details):
            return rating_details["rating"]

        def get_ratings(entity_list: list, get_index: bool = False):
            ratings = []
            for entity in entity_list:
                ratings.append((get_rating(entity), entity_list.index(entity))) if get_index else ratings.append(get_rating(entity))

            return ratings

        details['totals']['characters']['unweighted'] = (int(sum(get_ratings(character_ratings))) if integer_values else round(sum(get_ratings(character_ratings)), 2))
        details['totals']['artifacts']['unweighted'] = (int(sum(get_ratings(artifact_ratings))) if integer_values else round(sum(get_ratings(artifact_ratings)), 2))
        details['totals']['weapons']['unweighted'] = (int(sum(get_ratings(weapon_ratings))) if integer_values else round(sum(get_ratings(weapon_ratings)), 2))

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
            details['totals']['characters']['unweighted'] = 0

        section_pl = 0
        if GPRater.artifact_rating_enabled:
            for artifact_rating in get_ratings(artifact_ratings, True):
                rating = weight_rater(artifact_rating[0], GPRater.artifact_factor, artifact_rating[1])
                section_pl += rating
                power_level += rating

            details['totals']['artifacts']['weighted'] = int(section_pl) if integer_values else round(section_pl, 2)
        else:
            details['totals']['artifacts']['weighted'] = 0
            details['totals']['artifacts']['unweighted'] = 0

        section_pl = 0
        if GPRater.weapon_rating_enabled:
            for weapon_rating in get_ratings(weapon_ratings, True):
                rating = weight_rater(weapon_rating[0], GPRater.weapon_factor, weapon_rating[1])
                section_pl += rating
                power_level += rating

            details['totals']['weapons']['weighted'] = int(section_pl) if integer_values else round(section_pl, 2)
        else:
            details['totals']['weapons']['weighted'] = 0
            details['totals']['weapons']['unweighted'] = 0

        if integer_values:
            unweighted = int(sum(get_ratings(character_ratings)) + sum(get_ratings(artifact_ratings)) + sum(get_ratings(weapon_ratings)))
            weighted = int(power_level)
        else:
            unweighted = round(sum(get_ratings(character_ratings)) + sum(get_ratings(artifact_ratings)) + sum(get_ratings(weapon_ratings)), 2)
            weighted = round(power_level, 2)

        details['rating']['unweighted'] = unweighted
        details['rating']['weighted'] = weighted

        def int_to_roman(num: int) -> str:
            if not 0 < num < 4000:
                raise ValueError("Input must be an integer between 1 and 3999.")

            roman_numerals = {5: 'V', 4: 'IV', 1: 'I'}

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
                    if tier_value == tier_name:
                        rank = tier_name, ""
                    else:
                        rank = tier_name, int_to_roman(int(tier_value))
                    break

            if rank[0] != 'unranked':
                break

        details['ranking']['rank'] = rank[0]
        details['ranking']['tier'] = rank[1]

        return details
