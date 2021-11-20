from flask_login import UserMixin
import mongoengine as db

# Class model that will create a table in the DB
class Users(db.Document, UserMixin):

    username = db.StringField(max_length=200, required=True)
    password = db.StringField(max_length=200, required=True)

    def __str__(self):
        return (
            f'Username: {self.username}, '
            f'Password: {self.password}'
        )

class Messages(db.Document):

    username = db.StringField(max_length=200, required=True)
    content = db.StringField(max_length=200, required=True)

    def __str__(self):
        return (
            f'Username: {self.username}, '
            f'Content: {self.content}'
        )

class Rooms(db.Document):

    room_name = db.StringField(max_length=50, required=True)

    def __str__(self):
        return (
            f'Room name: {self.room_name}'
        )
