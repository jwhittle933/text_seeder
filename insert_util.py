import requests

from json_util import serialize


def insert_new(doc):
    r = requests.post('http://127.0.0.1:5984/texts',
                      headers={"content-type": "application/json"},
                      data=serialize(doc).encode('utf-8'))
    print(r.text)


def try_insert(document, should, **kwargs):
    if should:
        # if kwargs.get("overwrite", False):
        insert_new(document)
        # input("Enter to proceed.")
