import sys
import os
import json
import gzip
from pathlib import Path
import unicodedata


def parse_doc(file):
    if file.name.endswith(".pdf"):
        try:
            with gzip.open(str(file) + ".txt.gz", 'rt', encoding='utf-8') as f:
                lines = f.readlines()
        except:
            print(f"PDF parse error: {file.name}")
            return
        if len(lines) == 0:
            print(f"PDF parse error: {file.name}")
            return
        else:
            chars = []
            char2pos = []
            pos = 0
            for line in lines:
                items = line.strip().split("\t")
                char = items[1]
                chars.append(char)
                char2pos.append(pos)
                pos += len(char)
                delim = items[3]
                if delim == "S":
                    chars.append(" ")
                    pos += 1
                elif delim == "N":
                    chars.append("\n")
                    pos += 1
            text = "".join(chars)
            return {"text": text, "char2pos": char2pos, "anno": []}
    else:
        with open(file, 'rt', encoding='utf-8') as f:
            text = f.read()
        char2pos = [i for i in range(len(text))]
        return {"text": text, "char2pos": char2pos, "anno": []}


def main():
    categories = json.load(open(WORKING_DIR / 'categories.json', encoding='utf-8'))
    cat_dict = {}
    prop_dict = {}
    prop2cat = {}
    for cat in categories:
        cat_dict[cat['id']] = cat['name']
        for prop in cat['properties']:
            prop_dict[prop['id']] = prop
            prop2cat[prop['id']] = cat['id']

    entities = json.load(open(WORKING_DIR / 'entities.json', encoding='utf-8'))
    entity_dict = {}
    for ent in entities:
        entity_dict[ent['id']] = ent

    nodes = json.load(open(WORKING_DIR / 'nodes.json', encoding='utf-8'))

    members = json.load(open(WORKING_DIR / 'members.json', encoding='utf-8'))
    users = []
    for member in members:
        type = member["type"]
        if type == "user":
            users.append(member)
        elif type == "group":
            u = filter(lambda m: m["type"] == "user", member["members"])
            users.extend(u)
    user_dict = {}
    for user in users:
        user_dict[user["id"]] = user["name"]

    documents = json.load(open(WORKING_DIR / 'documents.json', encoding='utf-8'))
    doc_dict = {}
    for doc in documents:
        doc_id = doc['id']
        file = WORKING_DIR / doc_id
        doc_json = parse_doc(file)
        if doc_json is not None:
            doc_dict[doc_id] = doc_json

    """
    annotation node: {"id", "documentId", "propertyId", "parentId", "categoryId", "annotation"}
    value node: {"id", "documentId", "propertyId", "parentId", "value"}
    annotation: {"id", "page", "uid", "type": span | rectangle, "value", "documentId", "startIndex", "endIndex"}
    """
    node_dict = {node['id']: node for node in nodes}
    for node in nodes:
        doc_id = node['documentId']
        if doc_id not in doc_dict:
            continue
        doc = doc_dict[doc_id]
        doc_char2pos = doc["char2pos"]

        if 'categoryId' in node:
            cat_id = node['categoryId']
            cat = cat_dict[cat_id]
        else:
            cat = None
        if 'parentId' in node and 'propertyId' in node:
            parent_id = node['parentId']
            property_id = node['propertyId']
            prop = prop_dict[property_id]['name']
            parent = node_dict[parent_id]
            parent_start = parent['annotation']['startIndex'] - 1
            parent_end = parent['annotation']['endIndex'] - 1
            parent_start = doc_char2pos[parent_start]
            parent_end = doc_char2pos[parent_end]
            parent_cat = cat_dict[parent['categoryId']]
            parent_anno_id = f"{parent_start}-{parent_end}-{parent_cat}"
        else:
            parent_id = None
            property_id = None
            prop = "_"
        if 'value' in node:
            value = node['value']
            if property_id is not None and prop_dict[property_id]['type'] == 'entity':
                if value in entity_dict:
                    value = entity_dict[value]['title']
        else:
            value = "_"

        doc_anno = doc["anno"]
        # annotation node
        if 'annotation' in node:
            anno = node['annotation']
            uid = anno['uid']
            user = user_dict.get(uid, uid)
            if 'startIndex' in anno and 'endIndex' in anno:
                start = anno['startIndex'] - 1
                end = anno['endIndex'] - 1
                start = doc_char2pos[start]
                end = doc_char2pos[end]
                doc_anno.append([start, end, cat, user, parent_anno_id, prop, value])
        # value node
        elif value is not None:
            doc_anno.append([-1, -1, '_', '_', parent_anno_id, prop, value])

    for doc_id, doc_json in doc_dict.items():
        print(doc_id)
        if doc_id.endswith(".pdf"):
            text_file = WORKING_DIR / f"{doc_id}.txt"
            with open(text_file, "w", encoding='utf-8') as f:
                f.write(doc_json["text"])

        if len(doc_json["anno"]) > 0:
            anno_file = WORKING_DIR / f"{doc_id}.anno"
            doc_json["anno"].sort(key=lambda x: x[0])
            with open(anno_file, "w", encoding='utf-8') as f:
                for anno in doc_json["anno"]:
                    f.write("\t".join(map(str, anno)))
                    f.write("\n")


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        config = json.load(f)
    WORKING_DIR = Path(config['WORKING_DIR'])
    USER_TOKEN = config['USER_TOKEN']
    API_ENDPOINT = config['API_ENDPOINT']
    WORKSPACE = config['WORKSPACE']
    main()
