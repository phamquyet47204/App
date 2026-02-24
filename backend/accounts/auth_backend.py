from django.contrib.auth import get_user_model

User = get_user_model()


class MSSVOrEmailBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = kwargs.get("identifier") or username
        if not identifier or not password:
            return None

        user = (
            User.objects.filter(mssv__iexact=identifier).first()
            or User.objects.filter(email__iexact=identifier).first()
            or User.objects.filter(username__iexact=identifier).first()
        )

        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
