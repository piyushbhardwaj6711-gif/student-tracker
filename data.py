
# from pathlib import Path
# import json

# data_file = Path("students.json")

# def load_students() -> list[dict]:
#     if not data_file.exists():
#         return []

#     with open(data_file, "r", encoding="utf-8") as f:
#         return json.load(f)

# if __name__ == "__main__":
#     print(load_students())

from pathlib import Path
import json

data_file = Path("students.json")

def load_students():
    if not data_file.exists():
        return []

    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    print(load_students())