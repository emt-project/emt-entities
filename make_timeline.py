import json
import os
from config import JSON_FOLDER


print("Lets make the Timeline data")
with open(os.path.join(JSON_FOLDER, "events.json")) as f:
    data = json.load(f)

events = []
timeline = {
    "title": {
        "text": {
            "headline": "Familiensache im Kontext",
            "text": "Ein Zeitstrahl zur Wirkungsperiode Kaiserin Eleonora Magdalenas von Pfalz-Neuburg",
        },
        "media": {
            "url": "bio-pics/emt_person_id__9.jpg",
            "credit": "Kaiserin Eleonora Magdalena, geb. Pfalz-Neuburg",
            "caption": "wikicommons",
        },
    },
    "events": [],
}

for key, value in data.items():
    try:
        year, month, day = value["not_before"].split("-")
    except AttributeError:
        continue
    event = {}
    event["start_date"] = {
        "year": f"{int(year)}",
        "month": f"{int(month)}",
        "day": f"{int(day)}",
    }
    event["text"] = {"headline": value["name"], "text": ""}

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

    if value["not_before"] != value["not_after"]:
        try:
            year, month, day = value["not_after"].split("-")
        except AttributeError:
            continue
        event["end_date"] = {
            "year": f"{int(year)}",
            "month": f"{int(month)}",
            "day": f"{int(day)}",
        }
    timeline["events"].append(event)

with open(os.path.join(JSON_FOLDER, "timeline.json"), "w") as f:
    json.dump(timeline, f, ensure_ascii=False, indent=2)
