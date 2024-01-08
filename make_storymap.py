import json
import os
from config import JSON_FOLDER

print("lets make the StoryMap data")
with open(os.path.join(JSON_FOLDER, "events.json")) as f:
    data = json.load(f)


def my_filtering_function(pair):
    key, value = pair
    if value["not_before"]:
        return True
    else:
        return False


result = {
    "storymap": {
        "call_to_action": True,
        "call_to_action_text": "",
        "map_as_image": False,
        "map_type": "osm:standard",
        "language": "de",
        "slides": [
            {
                "date": "",
                "text": {
                    "headline": "EMT-Storymap",
                    "text": "<div><div><span>Ereignisse rund um das Leben von EMT</span></div></div><br>",
                },
                "media": {
                    "url": "bio-pics/emt_person_id__9.jpg",
                    "credit": "Kaiserin Eleonora Magdalena, geb. Pfalz-Neuburg",
                    "caption": "wikicommons",
                },
                "location": {"line": True},
                "type": "overview",
            },
        ],
    }
}

filtered_dict = dict(filter(my_filtering_function, data.items()))
sorted_dict = dict(sorted(filtered_dict.items(), key=lambda x: x[1]["not_before"]))

for key, value in sorted_dict.items():
    try:
        year, month, day = value["not_before"].split("-")
    except AttributeError:
        continue
    event = {}
    event["start_date"] = value["not_before"]
    event["text"] = {"headline": f'{value["not_before"]} - {value["name"]}', "text": ""}

    if value["took_place_at"]:
        location_text = ""
        for pl in value["took_place_at"]:
            location_text += f"""<a href="{pl['emt_id']}.html">{pl["name"]}</a>"""
        event["text"]["text"] += f"Das Ereignis fand in {location_text} statt.<br>"

    if value["related_persons"]:
        person_text = "Folgende Personen waren daran beteiligt:<br>"
        for person in value["related_persons"]:
            person_text += (
                f"""<a href="{person['emt_id']}.html">{person['name']}</a><br>"""
            )
        event["text"]["text"] += person_text

    if value["img_url"]:
        event["media"] = {
            "url": value["img_url"],
            "caption": value["img_caption"],
            "credit": value["img_right"],
        }
    try:
        lat = value["took_place_at"][0]["lat"]
        lon = value["took_place_at"][0]["long"]
    except (KeyError, IndexError):
        continue
    event["location"] = {"lat": float(lat), "lon": float(lon), "line": True, "zoom": 12}
    result["storymap"]["slides"].append(event)

with open(os.path.join(JSON_FOLDER, "storymap.json"), "w") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
