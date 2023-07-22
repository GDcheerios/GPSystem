import json


class GPRater:
    # ranking
    gp_peak = 1800

    @staticmethod
    def get_tiers() -> dict:
        highest_gp = GPRater.gp_peak
        copper = {
            '5': round(highest_gp * 0.06),
            '4': round(highest_gp * 0.07),
            '3': round(highest_gp * 0.08),
            '2': round(highest_gp * 0.09),
            '1': round(highest_gp * 0.1),
        }

        bronze = {
            '5': round(highest_gp * 0.12),
            '4': round(highest_gp * 0.14),
            '3': round(highest_gp * 0.16),
            '2': round(highest_gp * 0.18),
            '1': round(highest_gp * 0.2),
        }

        silver = {
            '5': round(highest_gp * 0.22),
            '4': round(highest_gp * 0.24),
            '3': round(highest_gp * 0.26),
            '2': round(highest_gp * 0.28),
            '1': round(highest_gp * 0.3),
        }

        gold = {
            '5': round(highest_gp * 0.35),
            '4': round(highest_gp * 0.4),
            '3': round(highest_gp * 0.45),
            '2': round(highest_gp * 0.5),
            '1': round(highest_gp * 0.55),
        }

        platinum = {
            '3': round(highest_gp * 0.6),
            '2': round(highest_gp * 0.7),
            '1': round(highest_gp * 0.8),
        }

        diamond = {
            '2': round(highest_gp * 0.9),
            '1': round(highest_gp * 0.95)
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
    artifact_factor = 1
    weapon_factor = 1

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
    weapon_attack_factor = 0.8

    @staticmethod
    def generate_power_details(json_data, integer_values: bool = False) -> dict:
        details = {
            'rating': {
                'unweighted': 0,
                'weighted': 0
            },
            'ranking': {
                'tier': 'unranked',
                'tier value': ''
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

        # characters
        character_names = []
        character_ratings = []
        for character in json_data["inventory"]["characters"]:
            character_rating = 0
            character_name = character["name"]
            difficulty = (character["experience"]["level"] / 20) + 1
            character_rating += character["star rating"] * GPRater.character_star_rating_factor
            character_rating += character["experience"]["level"] * GPRater.character_level_factor
            character_rating += difficulty * GPRater.character_difficulty_factor
            equips = character["equips"]
            for artifact in equips["artifacts"]:
                if artifact:
                    character_rating += artifact["star rating"] * GPRater.artifact_star_rating_factor
                    character_rating += artifact["experience"]["level"] * GPRater.artifact_level_factor
                    character_rating += attribute_rater(artifact["stats"]["main attribute"])
                    for attribute in artifact["stats"]["attributes"]:
                        character_rating += attribute_rater(attribute)

            try:
                character_rating += equips["weapon"]["star rating"] * GPRater.character_star_rating_factor
                character_rating += equips["weapon"]["experience"]["level"] * GPRater.weapon_level_factor
                character_rating += equips["weapon"]["stats"]["attack"] * GPRater.weapon_attack_factor
                character_rating += attribute_rater(equips["weapon"]["stats"]["buff"])

            except KeyError:
                pass

            except TypeError:
                pass

            if character["experience"]["xp"] > 0 or character["experience"]["level"] > 1:
                character_names.append(character_name)
                character_ratings.append(character_rating)

        characters_sorted = sorted(character_ratings)

        zipped_characters = zip(character_ratings, character_names)

        sorted_names = [element for _, element in sorted(zipped_characters)]

        for i in range(len(sorted_names)):
            details['per object rating']['characters'].append({sorted_names[i]: characters_sorted[i]})

        # artifacts
        artifact_names = []
        artifact_ratings = []
        for artifact in json_data["inventory"]["artifacts"]:
            artifact_rating = 0
            artifact_name = artifact['name']
            artifact_rating += artifact["star rating"] * GPRater.artifact_star_rating_factor
            artifact_rating += artifact["experience"]["level"] * GPRater.artifact_level_factor
            artifact_rating += attribute_rater(artifact["stats"]["main attribute"])
            for buff in artifact["stats"]["attributes"]:
                artifact_rating += attribute_rater(buff)

            if artifact["experience"]["xp"] > 0 or artifact["experience"]["level"] > 1:
                artifact_ratings.append(artifact_rating)
                artifact_names.append(artifact_name)

        artifacts_sorted = sorted(artifact_ratings)

        zipped_artifacts = zip(artifact_ratings, artifact_names)

        sorted_names = [element for _, element in sorted(zipped_artifacts)]

        for i in range(len(sorted_names)):
            details['per object rating']['artifacts'].append({sorted_names[i]: artifacts_sorted[i]})

        # weapons
        weapon_names = []
        weapon_ratings = []
        for weapon in json_data["inventory"]["weapons"]:
            weapon_rating = 0
            weapon_name = weapon["name"]
            weapon_rating += weapon["star rating"] * GPRater.weapon_star_rating_factor
            weapon_rating += weapon["experience"]["level"] * GPRater.weapon_level_factor
            weapon_rating += weapon["stats"]["attack"] * GPRater.weapon_attack_factor

            if weapon["experience"]["xp"] > 0 or weapon["experience"]["level"] > 1:
                weapon_ratings.append(weapon_rating)
                weapon_names.append(weapon_name)

        weapons_sorted = sorted(weapon_ratings)

        zipped_weapons = zip(weapon_ratings, weapon_names)

        sorted_names = [element for _, element in sorted(zipped_weapons)]

        for i in range(len(sorted_names)):
            details['per object rating']['weapons'].append({sorted_names[i]: weapons_sorted[i]})

        details['totals']['characters']['unweighted'] = (
            int(sum(character_ratings)) if integer_values else round(sum(character_ratings), 2))
        details['totals']['artifacts']['unweighted'] = (
            int(sum(artifact_ratings)) if integer_values else round(sum(artifact_ratings), 2))
        details['totals']['weapons']['unweighted'] = (
            int(sum(weapon_ratings)) if integer_values else round(sum(weapon_ratings), 2))

        section_pl = 0
        # print(characters_sorted)
        for character_rating in characters_sorted:
            rating = character_rating * (GPRater.character_factor ** (characters_sorted.index(character_rating)))
            section_pl += rating
            power_level += rating

        details['totals']['characters']['weighted'] = int(section_pl) if integer_values else round(section_pl, 2)

        # print(artifacts_sorted)
        section_pl = 0
        for artifact_rating in artifacts_sorted:
            rating = artifact_rating * (GPRater.artifact_factor ** (artifacts_sorted.index(artifact_rating)))
            section_pl += rating
            power_level += rating

        details['totals']['artifacts']['weighted'] = int(section_pl) if integer_values else round(section_pl, 2)

        # print(weapons_sorted)
        section_pl = 0
        for weapon_rating in weapons_sorted:
            rating = weapon_rating * (GPRater.weapon_factor ** (weapons_sorted.index(weapon_rating)))
            section_pl += rating
            power_level += rating

        details['totals']['weapons']['weighted'] = int(section_pl) if integer_values else round(section_pl, 2)

        if integer_values:
            unweighted = int(sum(character_ratings) + sum(artifact_ratings) + sum(weapon_ratings))
            weighted = int(power_level)
        else:
            unweighted = round(sum(character_ratings) + sum(artifact_ratings) + sum(weapon_ratings), 2)
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

        details['ranking']['tier'] = rank[0]
        details['ranking']['tier value'] = rank[1]

        return details
