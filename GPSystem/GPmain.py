try:
    from .GPRater import GPRater
except ImportError:
    from GPRater import GPRater


class GPSystem:
    rater = GPRater()


def test_rating_tier(recursions: int, factor: int):
    for i in range(recursions + 1, 0, -1):
        rating = i * factor
        print(rating, program.rater.get_rank(i * 100))


if __name__ == '__main__':
    import json

    program = GPSystem()

    print(json.dumps(program.rater.get_tiers(), indent=4))

    rating = 0
    character = program.rater.get_character_rating(test_character_data)
    artifact = program.rater.get_artifact_rating(test_artifact_data)
    weapon = program.rater.get_weapon_rating(test_weapon_data)

    rating += character
    rating += artifact
    rating += weapon

    print(f"""
        Character: {character}
        Artifact: {artifact}
        Weapon: {weapon}
        
        Total: {rating}
    """)

    print(program.rater.get_rank(rating))
