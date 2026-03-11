import secrets

from boto3.dynamodb.conditions import Key
from django.contrib.auth.hashers import check_password
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from dynamo import table, to_native

from .serializers import LoginSerializer, UserSerializer


def _no_store_headers():
    return {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0, private",
        "Pragma": "no-cache",
        "Expires": "0",
        "Vary": "Authorization",
    }


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        identifier = serializer.validated_data["identifier"]
        password = serializer.validated_data["password"]

        user_table = table("accounts_user")
        candidates = []
        for index_name, attr in (
            ("mssv-index", "mssv"),
            ("email-index", "email"),
            ("username-index", "username"),
        ):
            response = user_table.query(
                IndexName=index_name,
                KeyConditionExpression=Key(attr).eq(identifier),
                Limit=1,
            )
            candidates.extend(response.get("Items", []))

        if not candidates:
            scan_resp = user_table.scan(
                ProjectionExpression="id, username, first_name, last_name, email, mssv, is_staff, is_superuser, is_active, password"
            )
            for item in scan_resp.get("Items", []):
                norm = to_native(item)
                if str(norm.get("mssv", "")).lower() == identifier.lower() or str(
                    norm.get("email", "")
                ).lower() == identifier.lower() or str(norm.get("username", "")).lower() == identifier.lower():
                    candidates.append(item)

        if not candidates:
            return Response({"detail": "Sai thông tin đăng nhập."}, status=status.HTTP_400_BAD_REQUEST)

        user = to_native(candidates[0])
        if not check_password(password, user.get("password", "")):
            return Response({"detail": "Sai thông tin đăng nhập."}, status=status.HTTP_400_BAD_REQUEST)

        token_table = table("authtoken_token")
        token_q = token_table.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key("user_id").eq(int(user["id"])),
            Limit=1,
        )
        token_item = token_q.get("Items", [])
        if token_item:
            token_key = token_item[0]["key"]
        else:
            token_key = secrets.token_hex(20)
            token_table.put_item(
                Item={
                    "key": token_key,
                    "user_id": int(user["id"]),
                }
            )

        return Response(
            {
                "token": token_key,
                "user": UserSerializer(user).data,
            },
            headers=_no_store_headers(),
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token_table = table("authtoken_token")
        response = token_table.query(
            IndexName="user_id-index",
            KeyConditionExpression=Key("user_id").eq(int(request.user.id)),
        )
        for item in response.get("Items", []):
            token_table.delete_item(Key={"key": item["key"]})
        return Response(status=status.HTTP_204_NO_CONTENT, headers=_no_store_headers())


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, headers=_no_store_headers())
