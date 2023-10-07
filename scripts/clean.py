from account.models import Notification, Profile
from payment.models import Purchase
from .clear_rewards import run as run_clear_rewards 
from .reset_courses import run as run_reset_courses 

def run():
    run_clear_rewards()
    run_reset_courses()

    profiles = []

    for profile in Profile.objects.all():
        profile.xp = 0
        profile.bits = 0
        profiles.append(profile)

    Profile.objects.bulk_update(profiles, ["xp", "bits"])
    Notification.objects.all().delete()
    Purchase.objects.all().delete()