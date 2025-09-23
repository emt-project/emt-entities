import requests
from tqdm import tqdm
from config import br_client, BASEROW_DB_ID
from AcdhArcheAssets.uri_norm_rules import get_norm_id

current_table = br_client.get_table_by_name(BASEROW_DB_ID, "persons")
WIKIDATA_EP = "https://www.wikidata.org/w/api.php?action=wbgetclaims&property=P18&entity={}&format=json"

DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}


items = []
filters = {"filter__field_24994__contains": "http", "filter__field_24997__empty": True}
for x in br_client.yield_rows(current_table, filters=filters):
    item = x
    items.append(item)

for x in tqdm(items):
    update_object = {}
    update_url = f"{br_client.br_base_url}database/rows/table/{current_table}/{x['id']}/?user_field_names=true"
    wd_id = get_norm_id(x["wikidata_url"])
    url = WIKIDATA_EP.format(wd_id)
    r = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
    try:
        img_name = r.json()["claims"]["P18"][0]["mainsnak"]["datavalue"]["value"]
        img_source = r.json()["claims"]["P18"][0]["mainsnak"]["datatype"]
        update_object["img_fetched"] = True
        update_object["img_name"] = img_name
        update_object["img_source"] = img_source
    except KeyError:
        update_object["img_fetched"] = True
    r = requests.patch(
        update_url,
        headers={
            "Authorization": f"Token {br_client.br_token}",
            "Content-Type": "application/json",
        },
        json=update_object,
    )
