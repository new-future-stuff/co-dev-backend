from typing import List
from sources import models


async def create_project(name: str, required_skills: List[models.Skill], creator: models.User) -> models.Project:
    return await models.Project.create(
        creator=creator,
        required_skills=required_skills,
        name=name,
    )


async def remove_project(project: models.Project):
    await project.delete()
