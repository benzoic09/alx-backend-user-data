#!/usr/bin/env python3
"""
A script to obfuscate specific fields in a log message using regex.
"""
import re
from typing import List
import logging


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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize the formatter with the given fields."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record by obfuscating specified fields."""
        original_message = super(RedactingFormatter, self).format(record)
        return filter_datum(
                self.fields, self.REDACTION, original_message, self.SEPARATOR)
