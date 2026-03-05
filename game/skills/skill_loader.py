from game.skills.warrior_skills import WARRIOR_SKILLS
from game.skills.wizard_skills import WIZARD_SKILLS
from game.skills.ranger_skills import RANGER_SKILLS
from game.skills.cleric_skills import CLERIC_SKILLS

ALL_SKILLS = {
    **WARRIOR_SKILLS,
    **WIZARD_SKILLS,
    **RANGER_SKILLS,
    **CLERIC_SKILLS
}
