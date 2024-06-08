#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)

    if user_id == 'me':
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())

    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    rj = request.get_json()
    if rj is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in rj:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in rj:
        return jsonify({"error": "Missing password"}), 400
    user = User()
    user.email = rj['email']
    user.password = rj['password']
    if 'last_name' in rj:
        user.last_name = rj['last_name']
    if 'first_name' in rj:
        user.first_name = rj['first_name']
    user.save()
    return jsonify(user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id: str) -> str:
    """ PUT /api/v1/users/<user_id>
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    user = User.get(user_id)
    if user is None:
        abort(404)

    rj = request.get_json()
    if rj is None:
        return jsonify({"error": "Not a JSON"}), 400

    if 'last_name' in rj:
        user.last_name = rj['last_name']
    if 'first_name' in rj:
        user.first_name = rj['first_name']
    user.save()
    return jsonify(user.to_json()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200
