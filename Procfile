worker: python DiscordBot.py
web: gunicorn -w 4 -b 0.0.0.0:$PORT -k gevent keep_alive:app
