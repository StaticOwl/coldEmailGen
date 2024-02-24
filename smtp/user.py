import inquirer

from utils.query import GET_USERS


class User:
    users = {}
    relation = {}

    def __init__(self, data=None):
        if data:
            self.id = data['id']
            self.name = data['username']
            self.email = data['email']
            self.password = data['password']
            self.status = data['status']
            self.sender = None
            self.message_type = None
            if self.status:
                self.sender = data['sender']
                self.message_type = data['message_type']
            self.add_user()
        else:
            raise ValueError("User data not provided")

    def add_user(self):
        if self.sender:
            User.users[f"{self.email} -> {self.sender}"] = self
        else:
            User.users[f"Sender({self.email})"] = self

    @classmethod
    def get_user(cls):
        answer = inquirer.prompt([inquirer.List('user', message="Select User: ",
                                                choices=[f"{id}. {user.name} -> {user.email}" for (id, user) in
                                                         (cls.users.keys(), cls.users.values())], default=0)])
        if answer:
            return cls.users.get(answer['user'].split('.')[0])

    def get_email(self):
        return self.email

    def get_pswd(self):
        if self.password:
            return self.password
        else:
            raise Exception("Not a Sender Type")

    @classmethod
    def clear_user_data(cls):
        cls.users.clear()


def get_users_from_db(db, query_str=GET_USERS):
    for data in db.query_to_get_data(query_str):
        User(data)


def insert_user(db):
    query_str = ""
    questions = [
        inquirer.Text('username', message="Enter username"),
        inquirer.Text('email', message="Enter email", validate=lambda _, x: '@' in x),
        inquirer.List('user_type', message="Select User Type", choices=['sender', 'receiver'], default='receiver'),
    ]

    answers = inquirer.prompt(questions)

    if answers['user_type'] == 'sender':
        sender_questions = [inquirer.Password('password', message="Enter password")]
        sender_answers = inquirer.prompt(sender_questions)
        answers.update(sender_answers)
        query_str = ("INSERT INTO users "
                     "(username, email, password, status) "
                     "VALUES "
                     f"('{answers['username']}', '{answers['email']}','{answers['password']}', false);")
    elif answers['user_type'] == 'receiver':
        message_types = [entry.get('type') for entry in db.query_to_get_data('select distinct type from template')]
        receiver_questions = [
            inquirer.Text('sender', message="Enter sender email"),
            inquirer.List('message_type', message="Enter Message Type", choices=message_types,
                          default=message_types[0])
        ]
        receiver_answers = inquirer.prompt(receiver_questions)
        answers.update(receiver_answers)
        query_str = ("INSERT INTO users "
                     "(username, email) "
                     "VALUES "
                     f"('{answers['username']}', '{answers['email']}');"
                     f"INSERT INTO relation "
                     "(sender, receiver, message_type)"
                     "VALUES "
                     f"('{answers['sender']}', '{answers['email']}', '{answers['message_type']}');")

    db.query_to_commit(query_str)
    print(f"Inserted User: {answers['username']}")


def clear_data():
    User.clear()
