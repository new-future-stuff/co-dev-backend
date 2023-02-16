import tortoise
from tortoise.models import Model
from tortoise import fields
import asyncio


class Skill(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    skills = fields.ManyToManyField("models.Skill", related_name="users")
    join_date = fields.DatetimeField()


class WebsiteUserData(Model):
    user = fields.ForeignKeyRelation("models.User", related_name="website_profile")
    hashed_password = fields.BinaryField()
    password_hash_salt = fields.BinaryField()
    email = fields.TextField(unique=True)


class TelegramUserData(Model):
    user = fields.ForeignKeyRelation("models.User", related_name="telegram_profile")
    telegram_id = fields.IntField(unique=True)


class Project(Model):
    id = fields.IntField(pk=True)
    creator = fields.ForeignKeyField("models.User", related_name="created_projects")
    name = fields.TextField()
    required_skills = fields.ManyToManyField("models.Skill")


class UserLike(Model):
    sender = fields.ForeignKeyField("models.User", related_name="sent_likes")
    receiver = fields.ForeignKeyField("models.Project", related_name="received_likes")


class ProjectLike(Model):
    sender = fields.ForeignKeyField("models.Project", related_name="sent_likes")
    receiver = fields.ForeignKeyField("models.User", related_name="received_likes")


class Token(Model):
    contents = fields.TextField()
    owner = fields.ForeignKeyField("models.User")
    expiration_time = fields.DatetimeField()


async def init():
    await tortoise.Tortoise.init(
        {
            "connections": {
                "default": {
                    "engine": "tortoise.backends.sqlite",
                    "credentials": {"file_path": "db.sqlite3"},
                }
            },
            "apps": {
                "events": {"models": ["__main__"], "default_connection": "default"}
            },
        }
    )


asyncio.run(init())
