import string


def multiline_input() -> str:
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return '\n'.join(lines)


def compare(s_1: str, s_2: str) -> bool:
    remove = string.punctuation + string.whitespace
    translation = str.maketrans(dict.fromkeys(remove))
    return s_1.translate(translation) == s_2.translate(translation)
