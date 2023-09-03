from os import system


def run():
    system(
        """ 
        python -m flush;
        python manage.py makemigrations;
        python manage.py migrate;
        python manage.py createsuperuser;
        python manage.py runscript create_test_questions; 
        python manage.py runscript create_rewards
        """
    )
