"""
Actions & Buff bodies of devilhunter
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 핸드건 치명타 피해량 특화 계수
SPEC_COEF_1 = 1 / 9.3206 / 100
# 샷건 스킬 피해량 특화 계수
SPEC_COEF_2 = 1 / 27.9663 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  'Pistoleer_3': {
    'name': 'pistoleer',
    'buff_type': 'stat',
    'effect': 'pistoleer_3',
    'duration': 999999,
    'priority': 7,
  },
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 8,
    'priority': 7,
  }
}

# Actions
# 유탄 출혈 시간 갱신 action
def extend_bleed(buff_manager: BuffManager, skill_manager: SkillManager):
  def duration_increase(buff: Buff):
    if buff.name == 'bleed':
      buff.duration += seconds_to_ticks(3)
  buff_manager.apply_function(duration_increase)

# 치적 시너지 등록
def activate_synergy_1(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# Buff bodies
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_handgun_additional_crit_damage = s * SPEC_COEF_1
    s_shotgun_multiplier = (1 + s * SPEC_COEF_2)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == "Handgun":
      s_acd = skill.get_attribute('additional_crit_damage')
      skill.update_attribute('additional_crit_damage', s_acd + s_handgun_additional_crit_damage)
    elif skill.get_attribute('identity_type') == 'Shotgun':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_shotgun_multiplier)

# 핸드거너 각인
def pistoleer_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.3)
    elif skill.get_attribute('identity_type') == "Handgun":
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.7)

# 치적 시너지 (8초)
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_acr = skill.get_attribute('additional_crit_rate')
    skill.update_attribute('additional_crit_rate', s_acr + 0.10)
