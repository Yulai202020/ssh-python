class connection():
    def __init__(self, ip, user, password) -> None:
        self.ip = ip
        self.user = user
        self.password = password

    def get_ip(self):
        return self.ip

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password