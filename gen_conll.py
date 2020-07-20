import sys
import os
import json
import gzip
from pathlib import Path
import unicodedata


def parse_doc(doc_id, file):
    if file.name.endswith(".pdf"):
        try:
            with gzip.open(str(file) + ".txt.gz", 'rt', encoding='utf-8') as f:
                lines = f.readlines()
            if len(lines) == 0:
                print(f"PDF parse error: {doc_id}")
                return
            else:
                chars = []
                delims = []
                for line in lines:
                    items = line.rstrip().split("\t")
                    chars.append(items[1])
                    delims.append(items[3])
                return {"filename": file.name, "chars": chars, "delims": delims}
        except:
            pass
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

    documents = json.load(open(WORKING_DIR / 'documents.json', encoding='utf-8'))
    doc_dict = {}
    for doc in documents:
        doc_id = doc['id']
        file = WORKING_DIR / doc_id
        doc_json = parse_doc(file)
        if doc_json is not None:
            doc_dict[doc_id] = doc_json

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
        else:
            parent_id = None
            property_id = None

        if 'annotation' in node:
            anno = node['annotation']
            anno_id = anno['id']
            if 'startIndex' in anno and 'endIndex' in anno:
                start = anno['startIndex'] - 1
                end = anno['endIndex'] - 1
                doc[start][-2] = "B-" + cat
                for k in range(start+1,end):
                    doc[k][-2] = "I-" + cat
                if start < end:
                    doc[end][-2] = "E-" + cat
                if parent_id is not None:
                    parent = node_dict[parent_id]
                    parent_start = parent['annotation']['startIndex']
                    prop = prop_dict[property_id]
                    doc[start][-1] = f"{parent_start} {prop}"

    for doc_id, data in doc_dict.items():
        path = WORKING_DIR / f"{doc_id}.conll"
        print(doc_id)
        with open(path, "w", encoding='utf-8') as f:
            for line in data:
                f.write('\t'.join(line))
                f.write("\n")


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        config = json.load(f)
    WORKING_DIR = Path(config['WORKING_DIR'])
    USER_TOKEN = config['USER_TOKEN']
    API_ENDPOINT = config['API_ENDPOINT']
    WORKSPACE = config['WORKSPACE']
    main()
    print("done")
