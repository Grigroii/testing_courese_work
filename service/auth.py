import calendar
import datetime
from flask import abort
import jwt

from constants import JWT_SECRET, JWT_ALGO
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise abort(404)

        # TODO расскоментировать 
        # if not is_refresh:
        #     if not self.user_service.compare_passwords(user.password, password):
        #         abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        return {
            "access_token": access_token.decode("utf-8"),
            "refresh_token": refresh_token.decode("utf-8")
        }

    def approve_refresh_token(self, refresh_token):
        data = jwt.encode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGO])
        username = data.get("username")

        return self.generate_tokens(username, None, is_refresh=True)
