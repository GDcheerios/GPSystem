try:
    from .GPRater import GPRater
except ImportError:
    from GPRater import GPRater


class GPSystem:
    rater = GPRater()


def rank(length: int = 0) -> tuple[list, list]:
    """
    assumes that the database is already connected

    :param length: how many users to show
    :return: the users and items
    """

    print("Fetching data...")
    if length == 0:
        users = db.fetch_all_to_dict(
            """
            select 
                id,
                weighted,
                rank,
                tier
            from gq_rankings
            order by weighted desc
            """
        )
    else:
        users = db.fetch_all_to_dict(
            """
            select 
                id,
                weighted,
                rank,
                tier
            from gq_rankings
            order by weighted desc
            limit %s
            """,
            params=(length,)
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
                    gq_items
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
        user["new rank"], user["new tier"] = program.rater.get_rank(user["new rating"])

    user_table = tabulate.tabulate(
        [(user["id"], user["weighted"], user["rank"], user["tier"], user["new rating"], user["new rank"],
          user["new tier"]) for user in users],
        headers=["User ID", "Current Rating", "Current Rank", "Current Tier", "New Rating", "New Rank", "New Tier"],
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

    return users, items


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

    rank(5)

    answer = input("Would you like to apply this rating to the database? (yes/no)")

    print("Applying rating to database...")
    print("This may take a while...")

    result = rank()
    users = result[0]
    items = result[1]

    if answer == "yes":
        print("rating users")
        for user in users:
            print(f"Applying rating to user {user['id']}...")
            unweighted = 0
            for item in items:
                if item["owner"] == user["id"]:
                    unweighted += item["new rating"]

            db.execute(
                """
                UPDATE gq_rankings
                SET 
                    weighted = %s,
                    unweighted = %s,
                    rank = %s,
                    tier = %s
                WHERE id = %s
                """,
                params=(user["new rating"], unweighted, user["new rank"], user["new tier"],
                        user["id"])
            )

        item_data = [(item["id"], item["new rating"]) for item in items]
        ids = [item["id"] for item in items]
        case_statements = " ".join(f"WHEN id = {id} THEN {rating}" for id, rating in item_data)
        query = f"""
                UPDATE gentrys_quest_items
                SET rating = CASE {case_statements} END
                WHERE id IN ({', '.join(map(str, ids))})
                """
        db.execute(query)

