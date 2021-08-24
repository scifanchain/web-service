import re


def comma_splitter(tag_string):
    return [t.strip().lower() for t in re.split("[,，]", tag_string) if t.strip()]
