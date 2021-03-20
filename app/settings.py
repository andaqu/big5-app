from models import personality, twitter

DOCUMENT = {"personality": personality.Document, "twitter": twitter.Document}
USER = {"personality": personality.User, "twitter": twitter.User}
CONFIG = {"development" : "config.debug", "production": "config.prod", None : "config.debug"}