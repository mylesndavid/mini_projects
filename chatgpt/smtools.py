class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.following = []
        self.feed = []

    def follow(self, user):
        self.following.append(user)

    def unfollow(self, user):
        self.following.remove(user)

    def post(self, message):
        self.feed.append(message)
        for user in self.following:
            user.feed.append(message)

    def view_feed(self):
        for message in self.feed:
            print(message)

class SocialMedia:
    def __init__(self):
        self.users = {}

    def create_account(self, username, password):
        if username not in self.users:
            self.users[username] = User(username, password)
            print("Account created successfully!")
        else:
            print("Username is already taken. Please choose a different one.")

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            return self.users[username]
        else:
            print("Incorrect username or password.")

sm = SocialMedia()

# create accounts
sm.create_account("user1", "password1")
sm.create_account("user2", "password2")

# login
user1 = sm.login("user1", "password1")
user2 = sm.login("user2", "password2")

# follow and post
user1.follow(user2)
user2.post("Hello world!")

# view feed
user1.view_feed()
# prints: "Hello world!"
