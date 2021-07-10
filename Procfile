release: python manage.py migrate
web: daphne test_chat.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=test_chat.settings -v2