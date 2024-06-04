#!/usr/bin/env python3
""" Auth module"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Auth class template for all authentication systems"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that returns False - path and excluded_paths"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        
        #ensure path ends with a slash
        if not excluded_paths:
            path += '/'

        excluded_paths = [p if p.endswitch('/') else p + '/' for p in excluded_paths]
        if path in excluded_paths:
            return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """ Method that returns None -
        request will be the Flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Method that returns None -
        request will be the Flask request object"""
        return None
