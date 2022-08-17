"""
Actions & Buff bodies of gunslinger

# writer: naalredtree
# update date: 220814

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
SPEC_COEF_2 = 1 / 15.38146 / 100
# 라이플 스킬 피해량 특화 계수
SPEC_COEF_3 = 1 / 27.9663 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
    'Peace_Maker_1': {
    'name': 'peace_maker_1',
    'buff_type': 'stat',
    'effect': 'peace_maker_1',
    'duration': 999999,
    'priority': 7,
  },
    'Time_To_Hunt_3': {
    'name': 'time_to_hunt_3',
    'buff_type': 'stat',
    'effect': 'time_to_hunt_3',
    'duration': 999999,
    'priority': 7,
  },
  'Speed_Buff_1': {
    'name': 'speed_buff',
    'buff_type': 'stat',
    'effect': 'speed_buff_1',
    'duration': 5,
    'priority': 7,
  },
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 8,
    'priority': 7,
  },
  'Synergy_2': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_2',
    'duration': 12,
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
  
def activate_synergy_2(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_2'], 'class')
  
# 퀵스텝 이속 버프 등록
def activate_speed_buff(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Speed_Buff_1'], 'class')
  
# Buff bodies
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_handgun_additional_crit_damage = s * SPEC_COEF_1
    s_shotgun_multiplier = (1 + s * SPEC_COEF_2)
    s_marksman_multiplier = (1 + s * SPEC_COEF_2 * 0.5)
    s_rifle_multiplier = (1 + s * SPEC_COEF_3)
    
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == 'Handgun':
      s_acd = skill.get_attribute('additional_crit_damage')
      skill.update_attribute('additional_crit_damage', s_acd + s_handgun_additional_crit_damage)
    elif skill.get_attribute('identity_type') == 'Rifle':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_rifle_multiplier)
    elif skill.get_attribute('identity_type') == 'Shotgun':
      s_dm = skill.get_attribute('damage_multiplier')
      if skill.get_attribute('name') == '마탄의 사수':
        # 마탄의 사수 특화 50% 적용
        s_dm = skill.get_attribute('damage_multiplier')
        skill.update_attribute('damage_multiplier', s_dm * s_marksman_multiplier)
      else:
        skill.update_attribute('damage_multiplier', s_dm * s_shotgun_multiplier)
      
# 피스메이커 각인
def peace_maker_1(character: CharacterLayer, skill: Skill, buff: Buff):  
    if skill.get_attribute('identity_type') == 'Awakening':
      # 각성기 피스메이커-샷건 효과 적용
      s_dm = skill.get_attribute('damage_multiplier') 
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('damage_multiplier', s_dm * 1.05)
      skill.update_attribute('additional_crit_rate', s_acr + 0.10)
    elif skill.get_attribute('identity_type') == "Handgun":
      c_as = character.get_attribute('attack_speed')         
      character.update_attribute('attack_speed', c_as + 0.138)
    elif skill.get_attribute('identity_type') == "Shotgun":
      s_dm = skill.get_attribute('damage_multiplier') 
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('damage_multiplier', s_dm * 1.05)
      skill.update_attribute('additional_crit_rate', s_acr + 0.10)
    elif skill.get_attribute('identity_type') == "Rifle":
      s_dm = skill.get_attribute('damage_multiplier') 
      skill.update_attribute('damage_multiplier', s_dm * 1.1478)      
      
# 사냥의시간 각인
def time_to_hunt_3(character: CharacterLayer, skill: Skill, buff: Buff):  
    if skill.get_attribute('identity_type') == "Handgun":
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('additional_crit_rate', s_acr + 0.45)
    elif skill.get_attribute('identity_type') == "Rifle":
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('additional_crit_rate', s_acr + 0.45)
     
# 치적 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_acr = skill.get_attribute('additional_crit_rate')
    skill.update_attribute('additional_crit_rate', s_acr + 0.10)
    
def synergy_2(character: CharacterLayer, skill: Skill, buff: Buff):
    s_acr = skill.get_attribute('additional_crit_rate')
    skill.update_attribute('additional_crit_rate', s_acr + 0.10)
    
# 퀵 스텝 공이속 버프
def speed_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ms = character.get_attribute('movement_speed')
    c_as = character.get_attribute('attack_speed')
    character.update_attribute('movement_speed', c_ms + 0.138)
    character.update_attribute('attack_speed', c_as + 0.138)