import json
import os

from config import JSON_FOLDER


seed_file = os.path.join(JSON_FOLDER, "places.json")
source_file = os.path.join(JSON_FOLDER, "events.json")

with open(seed_file, "r") as f:
    seed_data = json.load(f)

with open(source_file, "r") as f:
    source_data = json.load(f)

for key, value in source_data.items():
    old_values = value["took_place_at"]
    new_values = []
    for x in old_values:
        new_values.append(seed_data[f"{x['id']}"])
    value["took_place_at"] = new_values

seed_file = os.path.join(JSON_FOLDER, "persons.json")
with open(seed_file, "r") as f:
    seed_data = json.load(f)

for key, value in source_data.items():
    old_values = value["related_persons"]
    new_values = []
    for x in old_values:
        new_values.append(seed_data[f"{x['id']}"])
    value["related_persons"] = new_values


with open(source_file, "w") as f:
    json.dump(source_data, f, ensure_ascii=False, indent=4)
