"""
Actions & Buff bodies of soulfist

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

# 0.25초당 내공 회복량
DEFAULT_MEDITATION_ENERGY_RECOVERY = 30
DEFAULT_HYPER1_ENERGY_RECOVERY = 51
DEFAULT_HYPER2_ENERGY_RECOVERY = 81
DEFAULT_HYPER3_ENERGY_RECOVERY = 120


# 금강선공 강화 특화 계수
SPEC_COEF_1 = 1 / 46.5983 / 100

# 운기조식 시간 감소 특화 계수
SPEC_COEF_2 = 1 / 23.3013 / 100

CLASS_BUFF_DICT = {
  # 회선격추 공증
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 10,
    'priority': 7,
  },
  # 역천지체 더미 버프
    'Robust_Spirit': {
    'name': 'robust_spirit',
    'buff_type': 'stat',
    'effect': 'robust_spirit',
    'duration': 999999,
    'priority': 7,
  },
  # 금강선공 1단계
    'Hyper1': {
    'name':'hyper1',
    'buff_type': 'stat',
    'effect': 'hyper1',
    'duration': 90,
    'priority': 3,
  },  
  # 금강선공 2단계
    'Hyper2': {
    'name':'hyper2',
    'buff_type': 'stat',
    'effect': 'hyper2',
    'duration': 40,
    'priority': 3,
  },
  # 금강선공 3단계
    'Hyper3': {
    'name':'hyper3',
    'buff_type': 'stat',
    'effect': 'hyper3',
    'duration': 20,
    'priority': 3,
  },
  # 내공방출
  'energy_release': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'energy_release',
    'duration': 6,
    'priority': 9,
  },
  # 순보
  'flash_step_1': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'flash_step_1',
    'duration': 3,
    'priority': 3,
  },
    'flash_step_2': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'flash_step_2',
    'duration': 3,
    'priority': 5,
  },
    'flash_step_3': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'flash_step_3',
    'duration': 3,
    'priority': 7,
  },
}

# Actions
# 회선격추 시너지
def activate_synergy_1(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')
    
# 내공방출 공격력 증가
def activate_energy_release(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['energy_release'], 'class')
    
# 순보 1타 공격력 증가
def activate_flash_step_1(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['flash_step_1'], 'class')    
      
# 순보 2타 공격력 증가
def activate_flash_step_2(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['flash_step_2'], 'class')   

# 순보 3타 공격력 증가
def activate_flash_step_3(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['flash_step_3'], 'class')   
      
# 역천지체 등록
def actiavte_robust_spirit(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['Robust_Spirit'], 'class')
    
# 금강선공 1단계 action
def activate_hyper1(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['Hyper1'], 'class')
    def cooldown_reduction(skill: Skill):
      if skill.get_attribute('name') == 'Hyper2':
        skill.update_attribute('remaining_cooldown', 0)
      return
    skill_manager.apply_function(cooldown_reduction)
    
# 금강선공 1단계 해제 action
def deactivate_hyper1(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.unregister_buff('Hyper1')
    def cooldown_reduction(skill: Skill):
      if skill.get_attribute('name') == 'Hyper1':
        skill.update_attribute('remaining_cooldown', 10)
      return
    skill_manager.apply_function(cooldown_reduction)

# 금강선공 2단계 action
def activate_hyper2(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.unregister_buff('Hyper1')
    buff_manager.register_buff(CLASS_BUFF_DICT['Hyper2'], 'class')
    def cooldown_reduction(skill: Skill):
      if skill.get_attribute('name') == 'Hyper3':
        skill.update_attribute('remaining_cooldown', 0)
      return
    skill_manager.apply_function(cooldown_reduction)
    
# 금강선공 2단계 해제 action
def deactivate_hyper2(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.unregister_buff('Hyper2')
    def cooldown_reduction(skill: Skill):
      if skill.get_attribute('name') == 'Hyper1':
        skill.update_attribute('remaining_cooldown', 25)
      return
    skill_manager.apply_function(cooldown_reduction)
    
# 금강선공 3단계 action
def activate_hyper3(buff_manager: BuffManager, skill_manager: SkillManager):
    if buff_manager.is_buff_exists('Robust_Spirit'):
      buff_manager.register_buff(CLASS_BUFF_DICT['Hyper3'], 'class')
    else:
      buff_manager.unregister_buff('Hyper2')
      buff_manager.register_buff(CLASS_BUFF_DICT['Hyper3'], 'class')
    
# 금강선공 3단계 해제 action
def deactivate_hyper3(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.unregister_buff('Hyper3') 
    def cooldown_reduction_h1(skill: Skill):
      if skill.get_attribute('name') == 'Hyper1':
        skill.update_attribute('remaining_cooldown', 50)
      return
    def cooldown_reduction_h3(skill: Skill):
      if skill.get_attribute('name') == 'Hyper3':
        skill.update_attribute('remaining_cooldown', 50)
      return
    if buff_manager.is_buff_exists('Robust_Spirit'):
      skill_manager.apply_function(cooldown_reduction_h3)
    else:
      skill_manager.apply_function(cooldown_reduction_h1)

# Buff Bodies
# 회선격추 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.06)
  
# 내공방출 공격력 증가
def energy_release(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.556 * (1 + c_aap))
  
# 순보 1타 공격력 증가
def flash_step_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.148 * (1 + c_aap))
  
# 순보 2타 공격력 증가
def flash_step_2(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.296 * (1 + c_aap))
  
# 순보 3타 공격력 증가
def flash_step_3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.444 * (1 + c_aap))

# 금강선공 1단계 버프
def hyper1(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    c_ad = character.get_attribute('additional_damage')
    c_cr = character.get_attribute('cooldown_reduction')
    c_as = character.get_attribute('attack_speed')
    
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_multiplier_2 = (1 + s * SPEC_COEF_1)

    h_cr = 0.05 * s_multiplier_2
    h_as = 0.05 * s_multiplier_2
    h_ce = 0.1 * s_multiplier_2
    
    h_ad = 1 + ((c_ad - 1)*(1 + h_ce)) + h_ce
    
    character.update_attribute('cooldown_reduction', 1 - (1 - c_cr - h_cr))
    character.update_attribute('movement_speed', c_as + h_as) 
    character.update_attribute('additional_damage', h_ad)
    
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
      
# 금강선공 2단계 버프
def hyper2(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    c_ad = character.get_attribute('additional_damage')
    c_cr = character.get_attribute('cooldown_reduction')
    c_as = character.get_attribute('attack_speed')
    
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_multiplier_2 = (1 + s * SPEC_COEF_1)
    
    h_cr = 0.1 * s_multiplier_2
    h_as = 0.1 * s_multiplier_2
    h_ce = 0.25 * s_multiplier_2
    
    h_ad = 1 + ((c_ad - 1)*(1 + h_ce)) + h_ce
    
    character.update_attribute('cooldown_reduction', 1 - (1 - c_cr - h_cr))
    character.update_attribute('movement_speed', c_as + h_as) 
    character.update_attribute('additional_damage', h_ad)
    
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)

# 금강선공 3단계 버프
def hyper3(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    c_ad = character.get_attribute('additional_damage')
    c_cr = character.get_attribute('cooldown_reduction')
    c_as = character.get_attribute('attack_speed')
    
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_multiplier_2 = (1 + s * SPEC_COEF_1)
    
    def robust_spirit_COEF(buff_manager: BuffManager, skill_manager: SkillManager):
      if buff_manager.is_buff_exists('Robust_Spirit'):
        return 0.3
      else:
        return 0;
    
    h_cr = 0.25 * s_multiplier_2
    h_as = 0.15 * s_multiplier_2
    h_ce = (0.6 + robust_spirit_COEF) * s_multiplier_2  
  
    h_ad = 1 + ((c_ad - 1)*(1 + h_ce)) + h_ce
    
    character.update_attribute('cooldown_reduction', 1 - (1 - c_cr - h_cr))
    character.update_attribute('movement_speed', c_as + h_as) 
    character.update_attribute('additional_damage', h_ad)
    
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
      
# 세맥타통 버프
