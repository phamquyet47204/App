from dataclasses import dataclass

from rest_framework import authentication
from rest_framework import exceptions

from dynamo import table, to_native


@dataclass
class DynamoUser:
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    mssv: str
    is_staff: bool
    is_superuser: bool
    is_active: bool

    @property
    def is_authenticated(self):
        return True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


def build_user_from_item(user_item):
    user_item = to_native(user_item)
    return DynamoUser(
        id=int(user_item["id"]),
        username=user_item.get("username", ""),
        first_name=user_item.get("first_name", ""),
        last_name=user_item.get("last_name", ""),
        email=user_item.get("email", ""),
        mssv=user_item.get("mssv", ""),
        is_staff=bool(user_item.get("is_staff", False)),
        is_superuser=bool(user_item.get("is_superuser", False)),
        is_active=bool(user_item.get("is_active", True)),
    )


class DynamoTokenAuthentication(authentication.BaseAuthentication):
    keyword = "Token"

    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) != 2:
            raise exceptions.AuthenticationFailed("Invalid token header.")

        token_key = auth[1].decode("utf-8", errors="ignore")
        token_item = table("authtoken_token").get_item(Key={"key": token_key}).get("Item")
        if not token_item:
            raise exceptions.AuthenticationFailed("Invalid token.")

        user_id = int(to_native(token_item["user_id"]))
        user_item = table("accounts_user").get_item(Key={"id": user_id}).get("Item")
        if not user_item:
            raise exceptions.AuthenticationFailed("User not found.")

        return (build_user_from_item(user_item), token_key)

    def authenticate_header(self, request):
        return self.keyword
