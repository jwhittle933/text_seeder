import json


def new_doc(bk, src, *args, **kwargs):
    cont = kwargs.get('content', [])
    return dict(source=src, book=bk, content=cont)


def get_chapters(doc):
    return doc['content']


def get_current_chapter(chapters, ch):
    for chapter in chapters:
        if chapter.chapter == ch:
            return chapter
        return None


def add_chapter(doc, ch):
    # create new document
    newdoc = new_doc(doc.get('book'), doc.get('source'))
    new_chapter = dict(chapter=ch, content=[])
    current_chapters = get_chapters(doc)
    newdoc['content'] = [*current_chapters, *[new_chapter]]
    return newdoc


def add_verse(doc, vs, txt):
    # get the chapter content
    current_chapters = get_chapters(doc)
    current_chapters[-1]['content'] = [
        *current_chapters[-1]['content'], *[dict(verse=vs, text=txt)]
    ]

    # create new document and return
    newdoc = new_doc(doc.get('book'),
                     doc.get('source'),
                     content=current_chapters)

    return newdoc


def serialize(doc):
    return json.dumps(doc, sort_keys=True, indent=2,
                      ensure_ascii=False).encode('utf8').decode()
