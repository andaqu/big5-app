web: gunicorn "app:create_app()"
worker: python manager.py get_tweets -n 400 -b 200
worker: python manager.py hotfix -b 2500