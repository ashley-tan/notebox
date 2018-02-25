from peewee import *

import datetime
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

DATABASE = SqliteDatabase("notes.db")

class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE

    def get_notes(self):
        return Note.select().where(Note.user == self)

    @classmethod
    def create_user(cls, username, password):
        try: 
            with DATABASE.transaction():
                cls.create(username=username, password=generate_password_hash(password),)
        except IntegrityError:
            raise ValueError("User already exists")

class Note(Model):
    timestamp = DateTimeField()
    user = ForeignKeyField(
        rel_model=User,
        related_name="notes"
    )
    text = TextField()

    class Meta:
        database = DATABASE
        order_by = ("-timestamp",)

    def get_notes(self):
        return Note.select().where(Note.user == self)


def initialise():
	DATABASE.connect()
	DATABASE.create_tables([User, Note], safe=True)
	DATABASE.close()

def validate_password(User, pw):
    if check_password_hash(User.password, pw):
        return True
    else:
        return False