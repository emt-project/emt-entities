import requests
from tqdm import tqdm
from config import br_client, BASEROW_DB_ID
from acdh_geonames_utils.gn_client import gn_as_object


place_table_id = br_client.get_table_by_name(BASEROW_DB_ID, "places")


items = []
filters = {"filter__field_12746__contains": "https", "filter__field_23549__empty": True}
for x in br_client.yield_rows(place_table_id, filters=filters):
    item = x
    items.append(item)

for x in tqdm(items):
    update_object = {}
    update_url = f"{br_client.br_base_url}database/rows/table/{place_table_id}/{x['id']}/?user_field_names=true"
    gn_object = gn_as_object(x["geonames"])
    update_object["lat"] = gn_object["latitude"]
    update_object["long"] = gn_object["longitude"]
    r = requests.patch(
        update_url,
        headers={
            "Authorization": f"Token {br_client.br_token}",
            "Content-Type": "application/json",
        },
        json=update_object,
    )
