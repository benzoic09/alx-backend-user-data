#!/usr/bin/env python3
""" Auth module"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """ Auth class template for all authentication systems"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that returns False - path and excluded_paths"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # ensure path ends with a slash
        if not path.endswith('/'):
            path += '/'

        excluded_paths = [
                p if p.endswith('/') else p + '/' for p in excluded_paths]
        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Method that returns None -
        request will be the Flask request object"""
        if request is None:
            return None

        auth_header = request.headers.get("Authorization")
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that returns None -
        request will be the Flask request object"""
        return None

    def session_cookie(self, request=None):
        """Retrieves the session cookie from the request"""
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        if session_name is None:
            return None
        return request.cookies.get(session_name)
