from os import system


def run():
    system(
        """ 
        python -m flush;
        python manage.py makemigrations;
        python manage.py migrate;
        python manage.py runscript seed;
        python manage.py createsuperuser;
        """
    )
