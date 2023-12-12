from payment.models import Purchase

def down():
    Purchase.objects.all().delete()
