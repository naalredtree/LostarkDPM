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

# 기본 금강선공 지속시간
DEFAULT_HYPER3_TIME_LIMIT = 0
DEFAULT_HYPER2_TIME_LIMIT = 0

# 운기조식 시간
DEFAULT_MEDITATION_TIME_LIMIT = 0

# 금강선공 강화 특화 계수
SPEC_COEF_1 = 1 / 11.6507 / 100
# 변신 시간 특화 계수
SPEC_COEF_2 = 1 / 23.3031 / 100

CLASS_BUFF_DICT = {
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 10,
    'priority': 7,
  },
  # 금강선공 2단계
    'KI Explosion_2': {
    'name':'KI Explosion_2',
    'buff_type': 'stat',
    'effect': 'KI Explosion_2',
    'duration':0,
    'priority':7,
  },
  # 금강선공 3단계 
  'KI Explosion_3': {
    'name':'KI Explosion_3',
    'buff_type': 'stat',
    'effect': 'KI Explosion_3',
    'duration':0,
    'priority':7,
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
    'priority': 6,
  },
    'flash_step_2': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'flash_step_2',
    'duration': 3,
    'priority': 7,
  },
    'flash_step_3': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'flash_step_3',
    'duration': 3,
    'priority': 8,
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
  
  
# 금강선공 3단계 확인
def modchk_if_hyper(buff_manager: BuffManager, skill_manager: SkillManager):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '페르소나 상태 진입':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)
  
# 금강선공 3단계 확인
def modchk_if_meditation(buff_manager: BuffManager, skill_manager: SkillManager):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '페르소나 상태 진입':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)
  
  
  # Actions
# 하이퍼 싱크 변신 사용 가능 전환
def grant_hyper_sync(buff_manager: BuffManager, skill_manager: SkillManager):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '하이퍼 싱크 변신':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 하이퍼 싱크 사용
def activate_hyper_sync(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Hyper_Sync'], 'class')
  if buff_manager.is_buff_exists('evolutionary_legacy_enabled_1'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Evolutionary_Legacy_1'], 'class')
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '하이퍼 싱크 변신해제':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 변신 해제
def deactivate_hyper_sync(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.unregister_buff('hyper_sync')
  buff_manager.unregister_buff('evolutionary_legacy')
  buff_manager.unregister_buff('synergy_1')
  
# 페르소나 사용
def activate_persona(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Persona'], 'class')

# 급습 사용시 페르소나 해제
def deactivate_persona(buff_manager: BuffManager, skill_manager: SkillManager):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '어둠 게이지 체크':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 금강선공 2단계 action
# 금강선공 3단계 action
# 금강선공 3단계 action
# 금강선공 3단계 해제 action




# Buff Bodies
# 회선격추 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.06)
    
# 내공방출 공격력 증가
def energy_release(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.556 * (1 + c_aap))
    
# 순보 1회 공격력 증가
def flash_step_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.148 * (1 + c_aap))
    
# 순보 2회 공격력 증가
def flash_step_2(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.296 * (1 + c_aap))
    
# 순보 3회 공격력 증가
def flash_step_3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.444 * (1 + c_aap))

# 금강선공 2단계 버프
# 금강선공 3단계 버프



# 슬래쉬 이속 버프 등록
def activate_speed_buff(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Speed_Buff_1'], 'class')

# 악마화 변신 가능 action
def grant_transform(buff_manager: BuffManager, skill_manager: SkillManager):
  def cooldown_reduction(skill: Skill):
     if skill.get_attribute('name') == '악마화 변신':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 악마화 변신 action
def demon_transform(buff_manager: BuffManager, skill_manager: SkillManager):
  s_multiplier = 1 + buff_manager.character_specialization * SPEC_COEF_2
  #transform_time_limit = DEFAULT_TRANSFORM_TIME_LIMIT * s_multiplier
  buff_manager.register_buff(CLASS_BUFF_DICT['Demon_State'], 'class')
  def set_time_limit(skill: Skill):
    if skill.get_attribute('identity_type') == 'Common':
      skill.update_attribute('remaining_cooldown', 999999)
 #   if skill.get_attribute('name') == '악마화 해제':
 #     skill.update_attribute('remaining_cooldown', seconds_to_ticks(transform_time_limit))
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('identity_type') == 'Demon':
      skill.update_attribute('remaining_cooldown', 0)  
  skill_manager.apply_function(set_time_limit)
  if buff_manager.is_buff_exists('demonic_impulse'):
    skill_manager.apply_function(cooldown_reduction)

# 악마화 해제 action
def recover_human_form(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.unregister_buff('demon_state')
  def recover_cooldown(skill: Skill):
    if skill.get_attribute('identity_type') == 'Common':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(recover_cooldown)
  

# Buff bodies
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_multiplier_2 = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == 'Demon':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_2)

# 데모닉 슬래쉬 피증 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.06)

# 데모닉 슬래쉬 공이속 버프
def speed_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('movement_speed', c_ms + 0.3)

# 악마화 버프
def demon_state(character: CharacterLayer, skill: Skill, buff: Buff):
  c_ms = character.get_attribute('movement_speed')
  character.update_attribute('movement_speed', c_ms + 0.2)

# 멈출 수 없는 충동 버프
def demonic_impulse_3(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Demon':
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('additional_crit_rate', s_acr + 0.3)