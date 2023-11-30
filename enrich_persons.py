import requests
from tqdm import tqdm
from config import br_client, BASEROW_DB_ID
from acdh_geonames_utils.gn_client import gn_as_object
from acdh_id_reconciler import gnd_to_wikidata


current_table = br_client.get_table_by_name(BASEROW_DB_ID, "persons")


items = []
filters = {"filter__field_12742__contains": "https", "filter__field_24995__empty": True}
for x in br_client.yield_rows(current_table, filters=filters):
    item = x
    items.append(item)

for x in tqdm(items):
    update_object = {}
    update_url = f"{br_client.br_base_url}database/rows/table/{current_table}/{x['id']}/?user_field_names=true"
    try:
        wikidata_url = gnd_to_wikidata(x["gnd"])["wikidata"]
        update_object["wikidata_url"] = wikidata_url
        update_object["wikidata_enriched"] = True
    except IndexError:
        update_object["wikidata_enriched"] = True
    r = requests.patch(
        update_url,
        headers={
            "Authorization": f"Token {br_client.br_token}",
            "Content-Type": "application/json",
        },
        json=update_object,
    )
