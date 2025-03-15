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
        item["new rating"] = program.rater.get_rating(item["type"], item["metadata"])
        item["new rating"] = round(item["new rating"])

    for user in users:
        new_rating = 0
        counter = 0

        user_items = [item for item in items if item["owner"] == user["id"]]
        user["new rating"] = program.rater.get_user_rating(user_items, True)

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
