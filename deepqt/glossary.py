import re
from pathlib import Path
from typing import Any

import pandas as pd
import pyexcel_odsr as ods
from logzero import logger

import deepqt.structures as st


def process_text(text: str, glossary: st.Glossary) -> str:
    """
    Process a text string with the glossary.

    :param text: The text to process.
    :param glossary: The glossary to use.
    :return: The processed text.
    """
    lines_in = text.splitlines()
    lines_out = ["\n"] * len(lines_in)

    process_lines(lines_in, lines_out, glossary)

    return "\n".join(lines_out)


"""
Internal functions
"""


def parse_glossary(path: Path) -> st.Glossary:
    """
    Parse a glossary file into a glossary.
    Apply the appropriate parser.
    The file type should already have been verified to match the appropriate parser.

    :param path: The glossary file to parse.
    :return: The glossary structure.
    """

    glossary = st.Glossary()
    glossary.set_hash(path)

    if path.suffix == ".ods":
        logger.debug("Started ods parser.")
        parse_ods(path, glossary)
    elif path.suffix == ".xlsx":
        logger.debug("Started xlsx parser.")
        parse_xlsx(path, glossary)

    glossary.generate_patterns()
    return glossary


def parse_xlsx(path: Path, glossary: st.Glossary):
    """
    Parse an excel file into a glossary.
    Exceptions need to be handled by the caller.

    :param path: The excel file to parse.
    :param glossary: The glossary structure to write into.
    """

    workbook = pd.read_excel(path, sheet_name=None)

    for sheet in workbook.values():
        height, width = sheet.shape

        for y in range(0, height):
            for x in range(1, width):
                # Start one from the left, since the keyed term will be the right one from among two.
                # This way we cannot have an out-of-bounds error.
                cell = sheet.iat[y, x]
                prev_cell = sheet.iat[y, x - 1]
                parse_cell(cell, prev_cell, glossary)


def parse_ods(path: Path, glossary: st.Glossary):
    """
    Parse an ods file into a glossary.
    Exceptions need to be handled by the caller.

    :param path: The ods file to parse.
    :param glossary: The glossary structure to write into.
    """

    workbook = ods.get_data(str(path))
    # TODO, this ain't how it works

    for sheet in workbook.values():
        height, width = sheet.shape

        for y in range(0, height):
            for x in range(1, width):
                # Start one from the left, since the keyed term will be the right one from among two.
                # This way we cannot have an out-of-bounds error.
                cell = sheet.iat[y, x]
                prev_cell = sheet.iat[y, x - 1]
                parse_cell(cell, prev_cell, glossary)


def parse_term(
    cell: str,
    prev_cell: str,
    target_dict: dict[str, str],
    prefix: str = "",
    suffix: str = " ",
):
    replacement_term = cell[1:] + suffix
    original_term = prev_cell.replace(r"\+", "+")  # Spreadsheets trigger formula stuff with a +

    # Allow splitting an input term into multiple with &.
    original_terms = original_term.split("&")
    for original_term in original_terms:
        target_dict[prefix + original_term] = replacement_term


def parse_cell(cell: Any, prev_cell: Any, glossary: st.Glossary):
    """
    Format agnostic parsing of a cell.

    :param cell: The right cell with the key.
    :param prev_cell: The left cell with the input pattern.
    :param glossary: The glossary structure to write into.
    """
    if not isinstance(cell, str) or not isinstance(prev_cell, str):
        return
    if not cell.strip() or not prev_cell.strip():
        return
    if "ignore" in cell or "ignore" in prev_cell:
        return

    # Allow padding to protect trailing whitespace.
    if cell.startswith("/") and cell.endswith("/"):
        cell = cell[1:-1]
    if prev_cell.startswith("/") and prev_cell.endswith("/"):
        prev_cell = prev_cell[1:-1]

    # Find exact terms
    if cell.startswith("#"):
        parse_term(cell, prev_cell, glossary.exact_terms)
    # check if it's a suffix-less
    elif cell.startswith("|"):
        parse_term(cell, prev_cell, glossary.no_suffix_terms, suffix="")
    # check if it's an honorific. Must be preceded by a space.
    elif cell.startswith("$"):
        parse_term(cell, prev_cell, glossary.honorific_terms)
    # check if it's a title. These only match if followed by [A-Z]
    elif cell.startswith("!"):
        parse_term(cell, prev_cell, glossary.title_terms)
    # check if it's a secondary term, to be matched last
    elif cell.startswith("~"):
        parse_term(cell, prev_cell, glossary.post_terms)
    # check if it's a regex
    elif cell.startswith(":"):
        parse_term(cell, prev_cell, glossary.regex_terms, suffix="")
    else:
        pass  # Ignore the cell. Could be a comment etc.


def process_lines(
    lines_in: list[str],
    lines_out: list[str],
    glossary: st.Glossary,
    start_index: int = 0,
    count: int = -1,
):
    """
    Perform substitutions on a list of lines, given a start index and count.
    Use the glossary to do the substitutions.

    :param lines_in: The list of lines to process.
    :param lines_out: The list of lines to write into.
    :param start_index: The index to start at.
    :param count: The number of lines to process.
    :param glossary: The glossary to use for substitutions.
    """
    if count == -1:
        count = len(lines_in) - start_index

    for i in range(start_index, start_index + count):
        line = lines_in[i]

        if line == "\n":
            continue

        if glossary.exact_terms:
            line = glossary.exact_pattern.sub(lambda match: glossary.exact_terms[match.group()], line)

        if glossary.honorific_terms:
            line = glossary.honorific_pattern.sub(
                lambda match: match.group(1) + glossary.honorific_terms[match.group(2)],
                line,
            )

        for instance in glossary.title_pattern.findall(line):  # only match if followed by A-Z

            line = line.replace(instance, glossary.title_terms[instance[:-1]] + instance[-1])

        if glossary.no_suffix_terms:
            line = glossary.no_suffix_pattern.sub(lambda match: glossary.no_suffix_terms[match.group()], line)

        # Run unoptimized regex to prevent individual regex from interfering with each other.
        if glossary.regex_terms:
            for term, pattern in glossary.regex_terms.items():
                line = re.sub(term, glossary.regex_terms[term], line)

        if glossary.post_terms:
            line = glossary.post_pattern.sub(lambda match: glossary.post_terms[match.group()], line)

        lines_out[i] = line
