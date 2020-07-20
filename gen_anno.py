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
            lines = f.readlines()
        return


def main():
    categories = json.load(open(WORKING_DIR / 'categories.json', encoding='utf-8'))
    cat_dict = {}
    prop_dict = {}
    prop2cat = {}
    for cat in categories:
        cat_dict[cat['id']] = cat['name']
        for prop in cat['properties']:
            prop_dict[prop['id']] = prop['name']
            prop2cat[prop['id']] = cat['id']

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
    node: {"id", "documentId", "propertyId", "parentId", "categoryId", "annotation"}
    annotation: {"id", "page", "uid", "type": span | rectangle, "value", "documentId", "startIndex", "endIndex"}
    """
    node_dict = {node['id']: node for node in nodes}
    for node in nodes:
        doc_id = node['documentId']
        if doc_id not in doc_dict:
            continue
        doc = doc_dict[doc_id]

        if 'categoryId' not in node:
            continue
        cat_id = node['categoryId']
        cat = cat_dict[cat_id]
        if 'parentId' in node and 'propertyId' in node:
            parent_id = node['parentId']
            property_id = node['propertyId']
            prop = prop_dict[property_id]
        else:
            parent_id = None
            property_id = None
            prop = None

        doc_char2pos = doc["char2pos"]
        doc_anno = doc["anno"]
        if 'annotation' in node:
            anno = node['annotation']
            uid = anno['uid']
            user = user_dict.get(uid, uid)
            if 'startIndex' in anno and 'endIndex' in anno:
                start = anno['startIndex'] - 1
                end = anno['endIndex'] - 1
                start = doc_char2pos[start]
                end = doc_char2pos[end]
                # anno_id = f"{start}-{end}-{cat}"
                anno_json = [str(start), str(end), cat, user]
                doc_anno.append(anno_json)

                if parent_id is not None:
                    parent = node_dict[parent_id]
                    parent_start = parent['annotation']['startIndex'] - 1
                    parent_end = parent['annotation']['endIndex'] - 1
                    parent_start = doc_char2pos[parent_start]
                    parent_end = doc_char2pos[parent_end]
                    parent_cat = cat_dict[parent['categoryId']]
                    parent_anno_id = f"{parent_start}-{parent_end}-{parent_cat}"
                    anno_json.append(parent_anno_id)
                    anno_json.append(prop)
            doc_anno.sort(key=lambda x: x[0])

    for doc_id, doc_json in doc_dict.items():
        print(doc_id)
        text_file = WORKING_DIR / f"{doc_id}.txt"
        with open(text_file, "w", encoding='utf-8') as f:
            f.write(doc_json["text"])
        anno_file = WORKING_DIR / f"{doc_id}.anno"
        with open(anno_file, "w", encoding='utf-8') as f:
            for anno in doc_json["anno"]:
                f.write("\t".join(anno))
                f.write("\n")


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        config = json.load(f)
    WORKING_DIR = Path(config['WORKING_DIR'])
    USER_TOKEN = config['USER_TOKEN']
    API_ENDPOINT = config['API_ENDPOINT']
    WORKSPACE = config['WORKSPACE']
    main()
