echo "from django.contrib.auth.models import User; User.objects.create_superuser('deepak', 'admin@example.com', 'cooladmins@3')" | python manage.py shell;
echo  "python manage.py migrate && python manage.py makemigrations" | python manage.py shell;
echo  "python manage.py migrate && python manage.py migrate" | python manage.py shell;
echo  "python manage.py collectstatic" | python manage.py shell


