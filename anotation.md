mkdir caio && cd caio && mkdir nutri_lab && cd nutri_lab && code .
python3 -m venv .dev
source .dev/bin/activate

pip install django
pip install pillow
pip install django-environ
pip install psycopg2-binary

django-admin startproject nutri_lab .

python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py 
python3 manage.py runserver
python3 manage.py  startapp autenticacao
python3 manage.py runserver
python3 manage.py  migrate
python3 manage.py runserver
python3 manage.py createsuperuser
python3 manage.py runserver
 
 
Francisco_v1
fc@g.com
asdfg12Q