class GPRater:
    def __init__(self):
        self.character_factor = 0.95
        self.artifact_factor = 1
        self.weapon_factor = 1

    def generate_power_rating(self, json_data) -> dict:
        details = {
            'rating': None,
            'totals': {
                'characters': None,
                'weapons': None,
                'artifacts': None
            },
            'per object rating': {
                'characters': [],
                'weapons': [],
                'artifacts': []
            }
        }

        def attribute_rater(attribute):
            if isinstance(attribute, dict):
                attribute = attribute["buff"]
            rating = 0
            if attribute[0] == 1:
                rating += attribute[2] * 1.5

            elif attribute[0] == 2:
                rating += attribute[2] * 2.5

            elif attribute[0] == 3:
                rating += attribute[2] * 1

            elif attribute[0] == 4:
                rating += attribute[2] * 3

            elif attribute[0] == 5:
                rating += attribute[2] * 2

            return rating

        power_level = 0

        # characters
        character_names = []
        character_ratings = []
        for character in json_data["inventory"]["characters"]:
            character_rating = 0
            character_name = character["name"]
            difficulty = character["experience"]["level"] / 20
            character_rating += character["star rating"]
            character_rating += character["experience"]["level"] * 2
            character_rating += (difficulty + 1) * 10
            equips = character["equips"]
            family_names = []
            for artifact in equips["artifacts"]:
                family_names.append(artifact["family"])
                character_rating += artifact["star rating"] * 1.20
                character_rating += artifact["experience"]["level"]
                character_rating += ((artifact["experience"]["level"] / 4) * 2) + 1
                character_rating += attribute_rater(artifact["stats"]["main attribute"])
                for attribute in artifact["stats"]["attributes"]:
                    character_rating += attribute_rater(attribute)

            unique_family_names = []
            for name in family_names:
                if name not in unique_family_names:
                    unique_family_names.append(name)

            name_occurences = {}

            for unique_name in unique_family_names:
                count = 0
                for name in family_names:
                    if unique_name == name:
                        count += 1

                name_occurences[unique_name] = count

            for name in name_occurences:
                if name_occurences[name] >= 3:
                    character_rating += 10

                if name_occurences[name] == 5:
                    character_rating += 5

            try:
                character_rating += equips["weapon"]["star rating"] * 1.5
                character_rating += equips["weapon"]["experience"]["level"]
                character_rating += equips["weapon"]["stats"]["attack"] / 10
                character_rating += attribute_rater(equips["weapon"]["stats"]["buff"])
            except KeyError:
                pass

            except TypeError:
                pass

            if character["experience"]["xp"] > 0 or character["experience"]["level"] > 1:
                character_names.append(character_name)
                character_ratings.append(character_rating)

        # artifacts
        artifact_names = []
        artifact_ratings = []
        for artifact in json_data["inventory"]["artifacts"]:
            artifact_rating = 0
            artifact_name = artifact['name']
            artifact_rating += artifact["star rating"] * 1.20
            artifact_rating += ((artifact["experience"]["level"] / 4) * 2) + 1

            if artifact["experience"]["xp"] > 0 or artifact["experience"]["level"] > 1:
                artifact_ratings.append(artifact_rating)
                artifact_names.append(artifact_name)

        # weapons
        weapon_names = []
        weapon_ratings = []
        for weapon in json_data["inventory"]["weapons"]:
            weapon_rating = 0
            weapon_name = weapon["name"]
            weapon_rating += weapon["star rating"] * 1.50
            weapon_rating += weapon["experience"]["level"] * 1.26
            weapon_rating += weapon["stats"]["attack"] / 2

            if weapon["experience"]["xp"] > 0 or weapon["experience"]["level"] > 1:
                weapon_ratings.append(weapon_rating)
                weapon_names.append(weapon_name)


        weapons_sorted = sorted(weapon_ratings)

        zipped_weapons = zip(weapons_sorted, weapon_names)

        sorted_names = [element for _, element in sorted(zipped_weapons)]
        details['per object rating']['weapons'].append()

        for character_rating in character_ratings:
            power_level += character_rating * (self.character_factor ** (character_ratings.index(character_rating)))

            # factored_character_rating = '{:,}'.format(character_rating * character_factor**(character_ratings.index(character_rating)))
            # new_character_rating = '{:,}'.format(character_rating)
            # print(f"character #{character_ratings.index(character_rating) + 1} {factored_character_rating} | {new_character_rating}")

        for artifact_rating in artifact_ratings:
            power_level += artifact_rating * (self.artifact_factor ** (artifact_ratings.index(artifact_rating)))

            # factored_artifact_rating = '{:,}'.format(artifact_rating * artifact_factor**(artifact_ratings.index(artifact_rating)))
            # new_artifact_rating = '{:,}'.format(artifact_rating)
            # print(f"artifact #{artifact_ratings.index(artifact_rating) + 1} {factored_artifact_rating} | {new_artifact_rating}")

        for weapon_rating in weapon_ratings:
            power_level += weapon_rating * (self.weapon_factor ** (weapon_ratings.index(weapon_rating)))

            # factored_weapon_rating = '{:,}'.format(weapon_rating * weapon_factor**(weapon_ratings.index(weapon_rating)))
            # new_weapon_rating = '{:,}'.format(weapon_rating)
            # print(f"weapon #{weapon_ratings.index(weapon_rating) + 1} {factored_weapon_rating} | {new_weapon_rating}")

        # print(power_level)
        details['rating'] = power_level
        return details