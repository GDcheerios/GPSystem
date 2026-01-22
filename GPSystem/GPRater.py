class GPRater:
    gp_peak = 10000

    # section factors
    character_factor = 1
    character_rating_enabled = True
    artifact_factor = 1
    artifact_rating_enabled = True
    weapon_factor = 1
    weapon_rating_enabled = True
    max_item_rating = 100

    # character factors
    character_star_rating_factor = 5
    character_level_factor = 2
    character_difficulty_factor = 100
    character_artifact_factor = 1
    character_weapon_factor = 1

    # artifact factors
    artifact_star_rating_factor = 2
    artifact_level_factor = 1.2
    artifact_main_attribute_factor = 2
    artifact_attribute_factor = 1

    # weapon factors
    weapon_star_rating_factor = 2
    weapon_level_factor = 1.5
    weapon_attack_factor = 0.2
    weapon_attribute_factor = 1

    # stat attributes
    health = 1
    attack = 1.25
    defense = 1
    crit_rate = 1.5
    crit_damage = 1.5
    speed = 1
    attack_speed = 1
    tenacity = 1

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
        """
        retrieve the ranking tier values.

        :return: rank data
        """

        highest_gp = GPRater.gp_peak

        unranked = {
            '1': round(highest_gp * 0)
        }

        copper = {
            '1': round(highest_gp * 0.03),
            '2': round(highest_gp * 0.0325),
            '3': round(highest_gp * 0.035),
            '4': round(highest_gp * 0.0375),
            '5': round(highest_gp * 0.04)
        }

        bronze = {
            '1': round(highest_gp * 0.05),
            '2': round(highest_gp * 0.06),
            '3': round(highest_gp * 0.07),
            '4': round(highest_gp * 0.08),
            '5': round(highest_gp * 0.09)
        }

        silver = {
            '1': round(highest_gp * 0.1),
            '2': round(highest_gp * 0.115),
            '3': round(highest_gp * 0.130),
            '4': round(highest_gp * 0.145),
            '5': round(highest_gp * 0.16)
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
        """
        With a given attribute, rate it.

        :param attribute: Attribute to rate
        :return: Rating of attribute
        """

        try:
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
        except Exception as e:
            print(f"GPRater found an issue: {e}")
            return 0

    @staticmethod
    def is_ratable(item: dict) -> bool:
        """
        Check if an item has experience then it is ratable.

        :param item: Item to check.
        :return: If the item is ratable.
        """

        try:
            return item["CurrentXp"] > 0 or item["Level"] > 1
        except KeyError as e:
            print(f"GPRater found an issue: {e}")
            return False

    @staticmethod
    def get_artifact_rating(artifact: dict) -> float:
        """
        Go through an artifact and rate it.

        :param artifact: The artifact to rate.
        :return: Artifact rating.
        """

        try:
            artifact_rating = 0
            star_rating = artifact["StarRating"] * GPRater.artifact_star_rating_factor
            level = artifact['Level'] * GPRater.artifact_level_factor
            # main_attribute = GPRater.rate_attribute(artifact["stats"]["main attribute"]) * GPRater.artifact_main_attribute_factor
            # attributes = []
            # for attribute in artifact["stats"]["attributes"]:
            #     attributes.append(GPRater.rate_attribute(attribute) * GPRater.artifact_attribute_factor)

            artifact_rating += star_rating
            artifact_rating += level
            # artifact_rating += main_attribute
            # artifact_rating += sum(attributes)

            return artifact_rating
        except Exception as e:
            print(f"GPRater found an issue: {e}")
            return 0

    @staticmethod
    def get_weapon_rating(weapon: dict) -> float:
        """
        Go through a weapon and rate it.

        :param weapon: The weapon to rate.
        :return: Weapon rating.
        """

        try:
            weapon_rating = 0
            star_rating = weapon["StarRating"] * GPRater.weapon_star_rating_factor
            level = weapon["Level"] * GPRater.weapon_level_factor
            # buff = GPRater.rate_attribute(weapon["stats"]["buff"]) * GPRater.weapon_attribute_factor
            attack = 0

            weapon_rating += star_rating
            weapon_rating += level
            # weapon_rating += attack
            # weapon_rating += buff

            return weapon_rating
        except Exception as e:
            print(f"GPRater found an issue: {e}")
            return 0

    @staticmethod
    def get_character_rating(character: dict) -> float:
        """
        Go through a character and rate it.

        :param character: The character to rate.
        :return: Character rating.
        """

        try:
            character_rating = 0

            if not GPRater.is_ratable(character):
                return 0

            difficulty = (character["Level"] / 20) + 1
            star_rating = character["StarRating"] * GPRater.character_star_rating_factor
            level = character["Level"] * GPRater.character_level_factor
            difficulty = difficulty * GPRater.character_difficulty_factor
            for artifact in character["Artifacts"]:
                if artifact:
                    character_rating += GPRater.get_artifact_rating(artifact) * GPRater.character_artifact_factor

            try:
                if character['CurrentWeapon']:
                    character_rating += GPRater.get_weapon_rating(character['CurrentWeapon']) * GPRater.character_weapon_factor

            except KeyError:
                pass

            except TypeError:
                pass

            character_rating += difficulty
            character_rating += star_rating
            character_rating += level

            return character_rating
        except Exception as e:
            print(f"GPRater found an issue: {e}")
            return 0

    @staticmethod
    def int_to_roman(num: int) -> str:
        """
        turns an integer to a roman.

        :param num: Integer to convert
        :return: str of roman numeral
        """

        if not 0 < num < 4000:
            raise ValueError("Input must be an integer between 1 and 3999.")

        roman_numerals = {10: 'X', 5: 'V', 4: 'IV', 1: 'I'}

        roman_str = ""
        for value, numeral in roman_numerals.items():
            while num >= value:
                roman_str += numeral
                num -= value

        return roman_str

    @staticmethod
    def get_rank(rating: int) -> tuple:
        """
        Converts rating(GP) into a rank.

        :param rating: The GP to convert
        :return: Ranking
        """

        tiers = GPRater.get_tiers()

        for rank, levels in tiers.items():
            for tier, threshold in levels.items():
                if rating < threshold:
                    return previous_rank, int(previous_tier)

                previous_rank, previous_tier = rank, tier

        if previous_rank == "gentry warrior":
            warrior_tier = (rating // tiers["gentry warrior"]["1"])
            return "gentry warrior", warrior_tier

        return previous_rank, int(previous_tier)

    @staticmethod
    def get_rating(type: str, metadata: dict) -> float:
        """
        Get the rating based off the type and metadata of item.
        
        :param type: A string representing the type of item
        :param metadata: The data of the item
        :return: An integer representing the GP
        """

        if type == "artifact":
            return GPRater.get_artifact_rating(metadata)
        elif type == "character":
            return GPRater.get_character_rating(metadata)
        elif type == "weapon":
            return GPRater.get_weapon_rating(metadata)
        else:
            return 0

    @staticmethod
    def get_user_rating(items: list, testing: bool = False) -> float:
        """
        Grabs the rating of the user based off the items the user has.

        :param items: The list of the user's items
        :param testing: If testing new values
        :return: User's GP
        """

        rating = 0
        counter = 0

        if testing:
            items.sort(key=lambda x: x["new rating"], reverse=True)
        else:
            items.sort(key=lambda x: x["rating"], reverse=True)

        for item in items:
            if item["type"] == "artifact" and GPRater.artifact_rating_enabled:
                rating += round(item["rating"] * GPRater.artifact_factor ** counter)
            elif item["type"] == "character" and GPRater.character_rating_enabled:
                rating += round(item["rating"] * GPRater.character_factor ** counter)
            elif item["type"] == "weapon" and GPRater.weapon_rating_enabled:
                rating += round(item["rating"] * GPRater.weapon_factor ** counter)
            else:
                rating += 0

            counter += 1

            if counter == GPRater.max_item_rating:
                break

        return rating