try:
    from .GPRater import GPRater
except ImportError:
    from GPRater import GPRater


class GPSystem:
    rater = GPRater()
    version = "2.3.0"

    def __init__(self):
        print("You're using GPSystem version ", GPSystem.version)


if __name__ == '__main__':
    import os
    import pyperclip
    import json
    from tabulate import tabulate

    table_style = "pipe"
    file_path = "GPSystem/Data"
    program = GPSystem()
    # if os.path.isdir(file_path):
    #     pass
    # else:
    #     os.mkdir(file_path)

    print(json.dumps(program.rater.get_tiers(), indent=4))

    for i in range(500):
        rating = i * 100
        print(rating, program.rater.get_rank(i * 100))
