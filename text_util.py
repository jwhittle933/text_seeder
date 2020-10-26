import os
import re
from pathlib import Path

HEBREW = '[^אבגדהשזחטיכךלמםנןסעפףצץֹקרשׂשׁתֵֶַָֹוֹֻוְֱֲֳִֹּּ־ ]'
GREEK = '[αβγδεζηθικλμνξοπρσςτθφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ᾽῾´῀`ι῎.,῍῏¨΅¨῟῭ ]'

SKIP_HEBREW = re.compile('^xxxx[ ]{,4}[a-zA-Z0-9]*')
CHAPTER_HEBREW = re.compile('^xxxx  Chapter ([0-9]{,3})')
VERSE_HEBREW = re.compile('([0-9]{,3})')

BREAK_GREEK = re.compile('^@@@+')
CHAPTER_GREEK = re.compile('^#([a-zA-Z0-9]{,5}) ([0-9]{,3}):([0-9]{,3})')
CHAPTER_GREEK_ALT = re.compile(
    '^#([a-zA-Z0-9]{,5}) ([a-zA-Z0-9]{,5}) ([0-9]{,3}):([0-9]{,3})')


def bookname(path):
    """Return the file name witout extension

    File will be of the form Bookname_with_underscores.<vow|con|acc>.txt
    """
    return os.path.splitext(Path(path).stem)[0]


def should_skip_hebrew(text):
    if SKIP_HEBREW.match(text.encode('ascii',
                                     errors='ignore').decode()) is None:
        return False
    return True


def is_hebrew_chapter(text):
    m = CHAPTER_HEBREW.match(text.encode('ascii', errors='ignore').decode())
    if m is not None:
        return int(m.group(1))
    return None


def hebrew_chars(text):
    return re.sub(HEBREW, '', text)


def greek_chars(text):
    "replaces all character in the string that are not Greek chars"
    return re.sub(GREEK, '', text)


def should_break_greek(text):
    if BREAK_GREEK.match(text) is None:
        return False
    return True


def is_greek_chapter(text):
    """Locates chapter line in LXX files
    and matches the chapter and verse number"""
    m = CHAPTER_GREEK.match(text.encode('ascii', errors='ignore').decode())
    if m is not None:
        return int(m.group(2)), int(m.group(3))

    m = CHAPTER_GREEK_ALT.match(text.encode('ascii', errors='ignore').decode())
    if m is not None:
        return int(m.group(3)), int(m.group(4))
    return None


def split_greek_verses(text):
    """Each Greek chapter is a single line of verses, split
    the verse number. This function splits the string on verse
    numbers and yields each verse."""
    return re.split(r'\d+', text)
