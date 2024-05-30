#!/usr/bin/env python3
"""
A script to obfuscate specific fields in a log message using regex.
"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """
    fields (List[str]): The list of fields to obfuscate.
    redaction (str): The string to replace the field values with.
    message (str): The log message to be obfuscated.
    separator (str): The separator used in the log message.
    """
    pattern = '|'.join("{0}=[^{1}]*".format(
        field, separator)for field in fields)

    return re.sub(
            pattern, lambda m: "{0}={1}".format(
                m.group().split('=')[0], redaction), message)
