from account.models import User


def run():
    User.objects.filter(is_superuser=False).delete()
    