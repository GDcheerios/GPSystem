from GPSystem.ItemType import ItemType


class GPRater:
    gp_peak = 10000

    # section factors
    character_factor = 0.95
    character_rating_enabled = True
    artifact_factor = 0.5
    artifact_rating_enabled = True
    weapon_factor = 0.85
    weapon_rating_enabled = True
    max_item_rating = 100

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

    # stat attributes
    health = 1.5
    attack = 4
    defense = 1.2
    crit_rate = 5
    crit_damage = 4.5
    speed = 2
    attack_speed = 2

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
    def get_tiers(item_type: ItemType = None) -> dict:
        if item_type:
            if item_type == ItemType.Character:
                highest_gp = 1000
            elif item_type == ItemType.Artifact:
                highest_gp = 100
            elif item_type == ItemType.Weapon:
                highest_gp = 200
        else:
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

    @staticmethod
    def rate_attribute(attribute) -> float:
        rating = 0

        try:
            if isinstance(attribute, dict):
                attribute = attribute["buff"]

            if attribute[0] == 1:  # health
                rating += attribute[2] * GPRater.health

            elif attribute[0] == 2:  # attack
                rating += attribute[2] * GPRater.attack

            elif attribute[0] == 3:  # defense
                rating += attribute[2] * GPRater.defense

            elif attribute[0] == 4:  # crit rate
                rating += attribute[2] * GPRater.crit_rate

            elif attribute[0] == 5:  # crit damage
                rating += attribute[2] * GPRater.crit_damage
        except KeyError:
            if attribute['stat'] == 'Health':
                rating += attribute['level'] * GPRater.health
            elif attribute['stat'] == 'Attack':
                rating += attribute['level'] * GPRater.attack
            elif attribute['stat'] == 'Defense':
                rating += attribute['level'] * GPRater.defense
            elif attribute['stat'] == 'CritRate':
                rating += attribute['level'] * GPRater.crit_rate
            elif attribute['stat'] == 'CritDamage':
                rating += attribute['level'] * GPRater.crit_damage
            else:
                rating += attribute['level']

        return rating

    @staticmethod
    def check_xp(item: dict) -> bool:
        return item["experience"]["xp"] > 0 or item["experience"]["level"] > 1

    @staticmethod
    def rate_artifact(artifact, is_equipped=False):
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
            main_attribute = GPRater.rate_attribute(artifact["stats"]["main attribute"])
            attributes = []
            for attribute in artifact["stats"]["attributes"]:
                attributes.append(GPRater.rate_attribute(attribute))

            artifact_rating += star_rating
            artifact_rating += level
            artifact_rating += main_attribute
            artifact_rating += sum(attributes)

            artifact_details["rating"] = artifact_rating if (GPRater.check_xp(artifact) or is_equipped) else 0
            artifact_details["star_rating"] = star_rating
            artifact_details["level"] = level
            artifact_details["main attribute"] = main_attribute
            artifact_details["attributes"] = sum(attributes)

            return artifact_details

    @staticmethod
    def rate_weapon(weapon, is_equipped=False):
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
            pass

        weapon_rating += star_rating
        weapon_rating += level
        weapon_rating += attack

        weapon_details["rating"] = weapon_rating if (GPRater.check_xp(weapon) or is_equipped) else 0

        return weapon_details

    @staticmethod
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
                rating_details = GPRater.rate_artifact(artifact, True)
                artifact_rating += rating_details["rating"]
                artifacts.append(rating_details)

        character_details["artifacts"] = artifacts

        try:
            if equips['weapon']:
                rating_details = GPRater.rate_weapon(equips["weapon"], True)
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

        character_details["rating"] = character_rating if GPRater.check_xp(character) else 0
        character_details["star_rating"] = character["star rating"] * GPRater.character_star_rating_factor
        character_details["level"] = character["experience"]["level"] * GPRater.character_level_factor
        character_details["difficulty"] = difficulty * GPRater.character_difficulty_factor

        return character_details
