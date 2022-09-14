#########################################################################################
#
#  This file isn't explicitly used in the project, but it is useful for reading a
#  slightly different glossary file format.
#  This one has the input term to the right, and the replacement on the left.
#  However, here the key is on the left.
#  It's an inverted glossary, if you will.
#
#########################################################################################

import re
from pathlib import Path
from typing import Any
import argparse

import pyexcel

import deepqt.structures as st


def main():
    # Use argparse to gather the input and output paths.
    parser = argparse.ArgumentParser(description="Swap left and right terms in a glossary. Export simplified format.")
    parser.add_argument("glossary", type=Path, help="The glossary file to read.")
    parser.add_argument(
        "output",
        type=Path,
        help="The glossary file to write. Whatever file extension is used, it will try to generate that file type.",
    )
    args = parser.parse_args()

    glossary = st.Glossary()
    parse_glossary_file(args.glossary, glossary)
    dump_glossary_ods(glossary, args.output)


def parse_glossary_file(path: Path, glossary: st.Glossary):
    """
    Parse an ods file into a glossary.
    Exceptions need to be handled by the caller.

    :param path: The ods file to parse.
    :param glossary: The glossary structure to write into.
    """

    workbook = pyexcel.get_book_dict(file_name=str(path))

    # Pyexcel inserts comment text into cells, which we need to remove using the comment pattern.
    pattern = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.*?\n")

    for sheet in workbook.values():

        for row in sheet:
            for x in range(1, len(row)):
                # Start one from the left, since the keyed term will be the right one from among two.
                # This way we cannot have an out-of-bounds error.
                original = row[x]
                replacement = row[x - 1]

                parse_cell(original, replacement, glossary, pattern)


def dump_glossary_ods(glossary: st.Glossary, path: Path):
    """
    Take each dictionary in the glossary and dump it on it's own row as key value.
    Start each dictionary dump with the name of the dictionary on its own row.
    Export it as an ods file.

    :param glossary: The glossary structure to write into.
    :param path: The path to write the ods file to.
    """
    sheet = []

    def dump_dictionary(dictionary: dict[str, str], name: str):
        sheet.append([name])
        for key, value in dictionary.items():
            sheet.append([key, value])

    dump_dictionary(glossary.exact_terms, "Exact Terms")
    dump_dictionary(glossary.no_suffix_terms, "No Suffix Terms")
    dump_dictionary(glossary.honorific_terms, "Honorific Terms")
    dump_dictionary(glossary.title_terms, "Title Terms")
    dump_dictionary(glossary.post_terms, "Post Terms")
    dump_dictionary(glossary.regex_terms, "Regex Terms")
    print(glossary)

    pyexcel.save_as(array=sheet, dest_file_name=str(path))


def parse_cell(cell: Any, next_cell: Any, glossary: st.Glossary, comment_pattern: re.Pattern):
    """
    Format agnostic parsing of a cell.
    Pyexcel inserts comment text into cells, which we need to remove using the comment pattern.

    :param cell: The left cell with the key.
    :param next_cell: The right cell with the input pattern.
    :param glossary: The glossary structure to write into.
    :param comment_pattern: The pattern to remove comments.
    """
    if not isinstance(cell, str) or not isinstance(next_cell, str):
        return
    if not cell.strip().strip("-") or not next_cell.strip().strip("-"):
        return
    if "ignore" in cell or "ignore" in next_cell:
        return

    # Remove all inline comments.
    if isinstance(cell, str):
        cell = comment_pattern.sub("", cell)
    if isinstance(next_cell, str):
        next_cell = comment_pattern.sub("", next_cell)

    # Allow padding to protect trailing whitespace.
    if cell.startswith("/") and cell.endswith("/"):
        cell = cell[1:-1]
    if next_cell.startswith("/") and next_cell.endswith("/"):
        next_cell = next_cell[1:-1]

    # Find exact terms
    if next_cell.startswith("#"):
        glossary.exact_terms[cell] = next_cell
    # check if it's a suffix-less
    elif next_cell.startswith("|"):
        glossary.no_suffix_terms[cell] = next_cell
    # check if it's an honorific. Must be preceded by a space.
    elif next_cell.startswith("$"):
        glossary.honorific_terms[cell] = next_cell
    # check if it's a title. These only match if followed by [A-Z]
    elif next_cell.startswith("!"):
        glossary.title_terms[cell] = next_cell
    # check if it's a secondary term, to be matched last
    elif next_cell.startswith("~"):
        glossary.post_terms[cell] = next_cell
    # check if it's a regex
    elif next_cell.startswith(":"):
        glossary.regex_terms[cell] = next_cell
    else:
        pass  # Ignore the cell. Could be a comment etc.


if __name__ == "__main__":
    main()
