class GPRater:
    gp_peak = 10000

    # section factors
    character_factor = 0.95
    character_rating_enabled = True
    artifact_factor = 0.5
    artifact_rating_enabled = False
    weapon_factor = 0.85
    weapon_rating_enabled = False
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
    def is_ratable(item: dict) -> bool:
        return item["experience"]["xp"] > 0 or item["experience"]["level"] > 1

    @staticmethod
    def get_artifact_rating(artifact) -> float:
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

        return artifact_rating

    @staticmethod
    def get_weapon_rating(weapon) -> float:

        weapon_rating = 0
        star_rating = weapon["star rating"] * GPRater.weapon_star_rating_factor
        level = weapon["experience"]["level"] * GPRater.weapon_level_factor
        attack = 0

        weapon_rating += star_rating
        weapon_rating += level
        weapon_rating += attack

        return weapon_rating

    @staticmethod
    def get_character_rating(character) -> float:

        character_rating = 0
        difficulty = (character["experience"]["level"] / 20) + 1
        star_rating = character["star rating"] * GPRater.character_star_rating_factor
        level = character["experience"]["level"] * GPRater.character_level_factor
        difficulty = difficulty * GPRater.character_difficulty_factor
        equips = character["equips"]
        for artifact in equips["artifacts"]:
            if artifact:
                character_rating += GPRater.get_artifact_rating(artifact)

        try:
            if equips['weapon']:
                character_rating += GPRater.get_weapon_rating(equips['weapon'])

        except KeyError:
            pass

        except TypeError:
            pass

        character_rating += difficulty
        character_rating += star_rating
        character_rating += level

        return character_rating

    @staticmethod
    def get_rank(rating) -> tuple:
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
