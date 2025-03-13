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
    import tabulate
    import json
    from PSQLConnector import PSQLConnection as db
    from dotenv import load_dotenv
    import os

    print("Loading .env file...")
    load_dotenv()

    print("Connecting to database...")
    db.connect(
        os.environ['DB_USERNAME'],
        os.environ['DB_PASSWORD'],
        os.environ['DB_HOST'],
        os.environ['DB_DATABASE'],
    )

    print("Fetching data...")
    users = db.fetch_all_to_dict(
        """
        select 
            id,
            c_weighted
        from rankings
        order by c_weighted desc
        limit 5
        """
    )

    items = []

    for user in users:
        items.extend(
            db.fetch_all_to_dict(
                """
                select
                    id,
                    type,
                    rating,
                    metadata,
                    owner
                from
                    gentrys_quest_items
                where owner = %s
                """, params=(user['id'],)
            )
        )

    program = GPSystem()

    print("Processing data...")
    for item in items:
        if item["type"] == "artifact":
            item["new rating"] = program.rater.get_artifact_rating(item["metadata"])
        elif item["type"] == "character":
            item["new rating"] = program.rater.get_character_rating(item["metadata"])
        else:
            item["new rating"] = program.rater.get_weapon_rating(item["metadata"])

        item["new rating"] = round(item["new rating"])

    items.sort(key=lambda x: x["new rating"], reverse=True)

    for user in users:
        new_rating = 0
        counter = 0

        for item in items:
            if item["owner"] == user["id"]:
                if item["type"] == "artifact" and program.rater.artifact_rating_enabled:
                    new_rating += round(item["new rating"] * program.rater.artifact_factor ** counter)
                    counter += 1
                elif item["type"] == "character" and program.rater.character_rating_enabled:
                    new_rating += round(item["new rating"] * program.rater.character_factor ** counter)
                    counter += 1
                elif item["type"] == "weapon" and program.rater.weapon_rating_enabled:
                    new_rating += round(item["new rating"] * program.rater.weapon_factor ** counter)
                    counter += 1

            if counter == program.rater.max_item_rating:
                break

        user["new rating"] = new_rating

    user_table = tabulate.tabulate(
        [(user["id"], user["c_weighted"], user["new rating"]) for user in users],
        headers=["User ID", "Current Rating", "New Rating"],
        tablefmt="pretty"
    )
    print("User Ratings Table:")
    print(user_table)

    item_table = tabulate.tabulate(
        [(item["id"], item["owner"], item["type"], item["rating"], item["new rating"]) for item in items[:10]],
        headers=["Item ID", "Owner", "Type", "Rating", "New Rating"],
        tablefmt="pretty"
    )
    print("Item Ratings Table:")
    print(item_table)
