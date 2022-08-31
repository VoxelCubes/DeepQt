#!/bin/python
"""
Replaces/restores matching quotes to make them deepl-safe.
Usage: quote-saver <inputtext> <outputtext> --restore
"""
import argparse
import re


# ============================================== Protection ==============================================
p_direct_speech_j_re = re.compile(r"^「(.*)」$")
p_direct_speech_e_re = re.compile(r"^“(.*)”$")
p_direct_speech = (p_direct_speech_j_re, p_direct_speech_e_re, r"[QUOTE]\n\1\n[ENDQUOTE]")

p_thought_speech_j_re = re.compile(r"^『(.*)』$")
p_thought_speech_e_re = re.compile(r"^‘(.*)’$")
p_thought_speech = (p_thought_speech_j_re, p_thought_speech_e_re, r"[TELNET]\n\1\n[ENDTELNET]")

p_thought_internal_j_re = re.compile(r"^（(.*)）$")
p_thought_internal_e_re = re.compile(r"^\((.*)\)$")
p_thought_internal = (p_thought_internal_j_re, p_thought_internal_e_re, r"[THOUGHT]\n\1\n[ENDTHOUGHT]")

p_raphael_j_re = re.compile(r"^《(.*)》$")
p_raphael_e_re = re.compile(r"^<<(.*)>>$")
p_raphael = (p_raphael_j_re, p_raphael_e_re, r"[RAPHAEL]\n\1\n[ENDRAPHAEL]")

# ============================================== Restoration ==============================================
r_direct_speech_re = re.compile(r"\[QUOTE\].*?\n+(.*?)\n+?\[ENDQUOTE\]")
r_direct_speech = (r_direct_speech_re, r"“\1”")

r_thought_speech_re = re.compile(r"\[TELNET\].*?\n+(.*?)\n+?\[ENDTELNET\]")
r_thought_speech = (r_thought_speech_re, r"<\1>")

r_thought_internal_re = re.compile(r"\[THOUGHT\].*?\n+(.*?)\n+?\[ENDTHOUGHT\]")
r_thought_internal = (r_thought_internal_re, r"(\1)")

r_raphael_re = re.compile(r"\[RAPHAEL\].*?\n+(.*?)\n+?\[ENDRAPHAEL\]")
r_raphael = (r_raphael_re, r"<<\1>>")


def protect_line(line: str):
    """
    Apply each protection pattern to a line.
    :param line:
    :return:
    """
    for p_pattern in (p_direct_speech, p_thought_speech, p_thought_internal, p_raphael):
        j_re, e_re, repl = p_pattern
        line = j_re.sub(repl, line)
        line = e_re.sub(repl, line)

    return line


def protect_text(text: str):
    """
    Apply each protection pattern to the full text.
    :param text:
    :return:
    """
    return "\n".join(protect_line(line) for line in text.splitlines())


def restore(text_: str):
    """
    Apply each restoration pattern to the full text due to the line breaks introduced by the protection patterns.
    :param text_:
    :return:
    """
    for r_pattern in (r_direct_speech, r_thought_speech, r_thought_internal, r_raphael):
        r_re, repl = r_pattern
        text_ = r_re.sub(repl, text_)
    return text_


if __name__ == "__main__":
    # Parsing arguments
    parser = argparse.ArgumentParser(description="Replaces/restores matching quotes to make them deepl-safe.")
    parser.add_argument("inputtext", type=str, help="Input text file.")
    parser.add_argument("outputtext", type=str, help="Output text file.")
    parser.add_argument("--restore", action="store_true", help="Restore the text.")
    args = parser.parse_args()

    # Restoration is handled for the whole file at once.
    if args.restore:
        with open(args.inputtext, "r", encoding="utf-8") as f:
            text = f.read()
        text = restore(text)
        with open(args.outputtext, "w", encoding="utf-8") as f:
            f.write(text)

    # Protection is done line by line.
    else:
        with open(args.inputtext, "r", encoding="utf-8") as f:
            lines = f.readlines()
        lines = [protect_line(line) for line in lines]
        with open(args.outputtext, "w", encoding="utf-8") as f:
            f.writelines(lines)
