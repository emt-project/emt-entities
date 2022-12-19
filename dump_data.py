import os
from config import br_client, BASEROW_DB_ID, JSON_FOLDER

os.makedirs(JSON_FOLDER, exist_ok=True)

files = br_client.dump_tables_as_json(BASEROW_DB_ID, folder_name="json_dumps", indent=2)
print(files)
