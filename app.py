from utils.database import DatabaseObject
from smtp import user as user_object, smtp
from utils import configLoader
import inquirer

if __name__ == '__main__':
    db_config = configLoader.load_config('assets/database.ini', 'postgresql')
    db = DatabaseObject(db_config)
    db.connect_postgres()
    while True:
        answers = inquirer.prompt([inquirer.List('action', message="Select Action: ", choices=['insert user', 'send mail', 'insert template', 'help', 'quit'], default='m')])
        action = answers['action']
        match action:
            case 'insert user':
                user_object.insert_user(db)
            case 'send mail':
                user_object.get_users_from_db(db)
                users = user_object.User.users
                for user in users.values():
                    if user.status:
                        mail_server = smtp.SMTP(user, users)
                        mail_server.gmail()
                        mail_server.send_email(db)
                user_object.User.clear_user_data()
            case 'insert template':
                print("You can't right now!")
            case 'quit':
                db.close_postgress()
                break
            case 'help':
                print("""
                Available Actions:
                1. insert user : Let's you insert a user on your own, even not taking a look into the database. Prompts are self explanatory.
                2. send mail : 
                3. insert template
                """)
