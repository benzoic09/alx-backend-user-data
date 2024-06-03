#!/usr/bin/env python3
""" Auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class template for all authentication systems"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that returns False - path and excluded_paths"""
        return False

    def authorization_header(self, request=None) -> str:
        """ Method that returns None -
        request will be the Flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that returns None -
        request will be the Flask request object"""
        return None
