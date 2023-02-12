from tortoise.models import Model
from tortoise import fields


class Skill(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class User(Model):
    id = fields.IntField(pk=True)
    hashed_password = fields.TextField()
    password_hash_salt = fields.TextField()
    textual_id = fields.TextField(unique=True)
    name = fields.TextField()
    skills = fields.ManyToManyField("models.Skill", related_name="users")


class Project(Model):
    id = fields.IntField(pk=True)
    creator = fields.ForeignKeyField("models.User", related_name="created_projects")
    name = fields.TextField()


class UserLike(Model):
    sender = fields.ForeignKeyField("models.User", related_name="sent_likes")
    receiver = fields.ForeignKeyField("models.Project", related_name="received_likes")


class ProjectLike(Model):
    sender = fields.ForeignKeyField("models.Project", related_name="sent_likes")
    receiver = fields.ForeignKeyField("models.User", related_name="received_likes")


class TokenType(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class Token(Model):
    access_token = fields.TextField()
    type = fields.ForeignKeyField("models.TokenType", related_name="tokens")
