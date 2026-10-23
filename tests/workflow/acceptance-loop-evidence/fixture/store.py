class SessionStore:
    def __init__(self):
        self.user = None
        self.cache = {}

    def set_user(self, user):
        if user != self.user:
            self.cache.clear()
        self.user = user

    def put(self, key, value):
        self.cache[key] = value

    def get(self, key):
        return self.cache.get(key)

    def logout(self):
        self.user = None
        self.cache.clear()
