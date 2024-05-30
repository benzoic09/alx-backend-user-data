#!/usr/bin/env python3
"""
A script to obfuscate specific fields in a log message using regex.
"""
import re
from typing import List
import logging
import os
import mysql.connector
from mysql.connector import connection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_logger() -> logging.Logger:
    """Creates a logger for user data with obfuscation for PII fields."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create a StreamHandler
    stream_handler = logging.StreamHandler()
    # Set the RedactingFormatter with PII_FIELDS
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    # Add the handler to the logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """
    Connects to the MySQL database using credentials
    from environment variables.

    Returns:
        MySQLConnection: A MySQLConnection object to the database.
    """
    # Retrieve database credentials from environment variables
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Create a connection to the database
    conn = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return conn


def main():
    """ Main function to retrieve and log user data """
    logger = get_logger()
    db_conn = get_db()
    cursor = db_conn.cursor(dictionary=True)

    query = "SELECT * FROM users"
    cursor.execute(query)

    for row in cursor:
        row_str = "; ".join(f"{key}={value}" for key, value in row.items())
        logger.info(row_str)

    cursor.close()
    db_conn.close()
