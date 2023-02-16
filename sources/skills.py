from sources import models
from typing import List, Optional


async def add_skills(user: models.User, skills: List[models.Skill]):
    await user.skills.add(*skills)


async def remove_skills(user: models.User, skills: List[models.Skill]):
    await user.skills.remove(*skills)


async def create_skill(skill_name: str) -> models.Skill:
    return await models.Skill.create(name=skill_name)


async def delete_skill(skill: models.Skill):
    await skill.delete()


async def get_skills(skill_names: List[str]) -> Optional[models.Skill]:
    return await models.Skill.get(name__in=skill_names)
