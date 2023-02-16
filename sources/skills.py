from sources import models
from typing import List, Optional


async def add_skills(user: models.User, skills: List[models.Skill]):
    await user.skills.add(*skills)


async def remove_skills(user: models.User, skills: List[models.Skill]):
    await user.skills.remove(*skills)


async def create_skill(skill_name: str) -> models.Skill:
    return await models.Skill.create(name=skill_name)


async def get_skill(skill_name: str) -> Optional[models.Skill]:
    return await models.Skill.get(name=skill_name)
