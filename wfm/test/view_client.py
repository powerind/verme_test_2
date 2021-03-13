import json
import random
import string

from django.contrib.auth import get_user_model
from django.test import Client

from wfm.test import mixer


class ViewClient(Client):
    def __init__(self, god_mode=True, anon=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not anon:
            self._create_user(god_mode)
            self._auth()

    def _auth(self):
        self.login(username=self.user.username, password=self.password)

    def _create_user(self, god_mode=True):
        user_opts = {"is_staff": True, "is_superuser": True} if god_mode else {}
        self.user = mixer.blend(get_user_model(), **user_opts)
        self.password = "".join([random.choice(string.hexdigits) for _ in range(0, 6)])
        self.user.set_password(self.password)
        self.user.save()

    def get(self, *args, **kwargs):
        return self._api_call(
            "get", kwargs.get("expected_status_code", 200), *args, **kwargs,
        )

    def post(self, *args, **kwargs):
        return self._api_call(
            "post", kwargs.get("expected_status_code", 201), *args, **kwargs,
        )

    def put(self, *args, **kwargs):
        return self._api_call(
            "put", kwargs.get("expected_status_code", 200), *args, **kwargs,
        )

    def patch(self, *args, **kwargs):
        return self._api_call(
            "patch", kwargs.get("expected_status_code", 200), *args, **kwargs,
        )

    def delete(self, *args, **kwargs):
        return self._api_call(
            "delete", kwargs.get("expected_status_code", 204), *args, **kwargs,
        )

    def _api_call(self, method, expected, *args, **kwargs):
        # by default submit all data in JSON
        kwargs["format"] = kwargs.get("format", "json")
        kwargs["content_type"] = kwargs.get("content_type", "application/json")
        as_response = kwargs.pop("as_response", False)

        method = getattr(super(), method)
        response = method(*args, **kwargs)

        if as_response:
            return response

        content = self._decode(response)

        assert response.status_code == expected, content

        return content

    def _decode(self, response):
        if not len(response.content):
            return

        content = response.content.decode("utf-8", errors="ignore")
        if "application/json" in response._headers["content-type"][1]:
            return json.loads(content)
        else:
            return content
