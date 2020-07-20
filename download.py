import sys
import os
import requests
import json
import gzip
from pathlib import Path
import unicodedata


def get_api_response(apipath):
    headers = {}
    headers['deepscholar-user-token'] = USER_TOKEN
    response = requests.get(f'{API_ENDPOINT}/workspaces/{WORKSPACE}/{apipath}', headers=headers)
    return response.content


def save_api_response(apipath, filename):
    res = get_api_response(apipath)
    with open(filename, 'wb') as f:
        f.write(res)
    return res


def save_documents():
    docs = save_api_response('documents', WORKING_DIR / "documents.json")
    docs = json.loads(docs)
    print(f"Number of documents: {len(docs)}")
    for doc in docs:
        doc_id = doc['id']
        print(doc_id)
        if doc_id.endswith(".pdf"):
            # save_api_response(f'documents/{doc_id}', work_dir / doc_id)
            filetype = "txt.gz"
            save_api_response(f'documents/{doc_id}?filetype={filetype}', WORKING_DIR / (doc_id + ".txt.gz"))
        else:
            save_api_response(f'documents/{doc_id}', WORKING_DIR / doc_id)
        #if filename.exists():
        #    print(f"{filename} exists. Skip downloading")
        #    continue
    print("")


def main():
    if not WORKING_DIR.exists():
        raise Exception("Error: WORKING_DIR does not exist.")

    print("Downloading nodes...")
    save_api_response('nodes', WORKING_DIR / "nodes.json")

    print("Downloading categories...")
    save_api_response('categories', WORKING_DIR / "categories.json")

    print("Downloading documents")
    save_documents()


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        config = json.load(f)
    WORKING_DIR = Path(config['WORKING_DIR'])
    USER_TOKEN = config['USER_TOKEN']
    API_ENDPOINT = config['API_ENDPOINT']
    WORKSPACE = config['WORKSPACE']
    main()
