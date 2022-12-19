import glob
import os
import json
import jinja2

from acdh_tei_pyutils.tei import TeiReader

from AcdhArcheAssets.uri_norm_rules import get_normalized_uri


templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(
    loader=templateLoader, trim_blocks=True, lstrip_blocks=True
)
out_dir = "./indices"

os.makedirs(out_dir, exist_ok=True)
files = glob.glob("./json_dumps/*.json")

for x in files:
    _, tail = os.path.split(x)
    with open(x, "r") as f:
        data = json.load(f)
    context = {}
    context["objects"] = [value for key, value in data.items()]
    ent_type = tail.replace("s.json", "")
    template_name = f"list{ent_type}.xml"
    template = templateEnv.get_template(template_name)
    xml_name = os.path.join(out_dir, template_name)
    xml_data = template.render(context)
    doc = TeiReader(xml_data)
    for idno in doc.any_xpath(".//tei:body//tei:idno"):
        old_uri = idno.text
        new_uri = get_normalized_uri(old_uri)
        idno.text = new_uri
    doc.tree_to_file(xml_name)
