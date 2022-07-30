def to_link(header: str):
    result = header.lower()
    result = result.strip(" ?!.")
    result = result.replace(" ", "-")
    return "#" + result


def to_code_block(code: str) -> str:
    indent = "    "

    result = ""

    for line in code.splitlines():
        result += indent + line + "\n"

    return result


class Section:
    def __init__(self,
                 link,
                 header,
                 text):
        self.link = link
        self.header = header
        self.text = text
