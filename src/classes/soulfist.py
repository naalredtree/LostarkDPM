"""
Actions & Buff bodies of soulfist

# writer: naalredtree
# update date: 220814

"""
from asyncio.proactor_events import _ProactorBasePipeTransport
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
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
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
  'Energy_Release': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'energy_Release',
    'duration': 6,
    'priority': 7,
  },
  # 순보
  'Flash_Step_1': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'flash_step_1',
    'duration': 3,
    'priority': 7,
  },
    'Flash_Step_2': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'flash_step_2',
    'duration': 3,
    'priority': 7,
  },
    'Flash_Step_3': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'flash_step_3',
    'duration': 3,
    'priority': 7,
  }
}

# Actions
# 회선격추 시너지
def activate_synergy_1(buff_manager: BuffManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')
    
# 내공방출 공격력 증가
def activate_energy_release(buff_manager: BuffManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['Energy_Release'], 'class')
     
# 역천지체 각인 활성화
def actiavte_robust_spirit(buff_manager: BuffManager):
    buff_manager.register_buff(CLASS_BUFF_DICT['Robust_Spirit'], 'class')
    
# 순보 공격력 증가
def activate_flash_step(buff_manager: BuffManager):  
    if buff_manager.is_buff_exists('flesh_step_2'):     
      buff_manager.unregister_buff(CLASS_BUFF_DICT['Flash_Step_2'],'class')
      buff_manager.register_buff(CLASS_BUFF_DICT['Flash_Step_3'], 'class')   
    
    else:
      if buff_manager.is_buff_exists('flesh_step_1'): 
        buff_manager.unregister_buff(CLASS_BUFF_DICT['Flash_Step_1'],'class')
        buff_manager.register_buff(CLASS_BUFF_DICT['Flash_Step_2'], 'class')   
        
      else:
        buff_manager.register_buff(CLASS_BUFF_DICT['Flash_Step_1'], 'class')   
  
# 순보 쿨타임 갱신
def step_cooldown_calc(character: CharacterLayer):
    c_cr = character.get_attribute('cooldown_reduction')    
    
    def chk_step_stage(buff_manager: BuffManager, skill_manager: SkillManager):
      step_rc = 8
      def cooldown_reduction_step_1(skill:Skill):
        if skill.get_attribute('name') == '순보_1타':
          skill.update_attribute('remaining_cooldown', step_rc * (1 - c_cr))
        return    
      def cooldown_reduction_step_2(skill:Skill):
        if skill.get_attribute('name') == '순보_2타':
          skill.update_attribute('remaining_cooldown', step_rc * (1 - c_cr))
        return   
      def cooldown_reduction_step_3(skill:Skill):
        if skill.get_attribute('name') == '순보_3타':
          skill.update_attribute('remaining_cooldown', step_rc * (1 - c_cr))
        return   
      
      if buff_manager.is_buff_exists('flash_step_1'):
        step_rc = 8
        skill_manager.apply_function(cooldown_reduction_step_1)
        
      elif buff_manager.is_buff_exists('flash_step_2'):
        step_rc = 12
        skill_manager.apply_function(cooldown_reduction_step_1)
        skill_manager.apply_function(cooldown_reduction_step_2)
            
      elif buff_manager.is_buff_exists('flash_step_3'):
        step_rc = 16
        skill_manager.apply_function(cooldown_reduction_step_1)
        skill_manager.apply_function(cooldown_reduction_step_2)
        skill_manager.apply_function(cooldown_reduction_step_3)
    return

# 금강선공 1단계 action
def activate_hyper_1(character:CharacterLayer, buff_manager: BuffManager, skill_manager: SkillManager):
    s = character.get_attribute('specialization')
    h1_meditation_time = 10 * (1 - s * SPEC_COEF_2)
      
    def h1_meditation(skill:Skill):
      if skill.get_attribute('name') == '금강선공_1단계':
        skill.update_attribute('remaining_cooldown', h1_meditation_time) 
      return
    
    def grant_hyper2(skill:Skill):
      if skill.get_attribute('name') == '금강선공_2단계':
        skill.update_attribute('remaining_cooldown', 0) 
      return

    buff_manager.register_buff(CLASS_BUFF_DICT['Hyper1'], 'class')
    skill_manager.apply_function(h1_meditation)
    skill_manager.apply_function(grant_hyper2)

# 금강선공 2단계 action
def activate_hyper_2(character:CharacterLayer, buff_manager: BuffManager, skill_manager: SkillManager):
    s = character.get_attribute('specialization')
    h2_meditation_time = 25 * (1 - s * SPEC_COEF_2)
      
    def h2_meditation(skill:Skill):
      if skill.get_attribute('name') == '금강선공_1단계':
        skill.update_attribute('remaining_cooldown', h2_meditation_time) 
      return
    
    def grant_hyper3(skill:Skill):
      if skill.get_attribute('name') == '금강선공_3단계':
        skill.update_attribute('remaining_cooldown', 0) 
      return
    
    buff_manager.unregister_buff('Hyper1')
    buff_manager.register_buff(CLASS_BUFF_DICT['Hyper1'], 'class')
    skill_manager.apply_function(h2_meditation)
    skill_manager.apply_function(grant_hyper3)

# 금강선공 3단계 action
def activate_hyper_3(character:CharacterLayer, buff_manager: BuffManager, skill_manager: SkillManager):
    s = character.get_attribute('specialization')
    h3_meditation_time = 50 * (1 - s * SPEC_COEF_2)
    
    def h3_meditation(skill:Skill):
      if skill.get_attribute('name') == '금강선공_1단계' or '금강선공':
        skill.update_attribute('remaining_cooldown', h3_meditation_time) 
      return
    
    if buff_manager.is_buff_exists('Robust_Spirit'):
      buff_manager.register_buff(CLASS_BUFF_DICT['Hyper3'], 'class')
      skill_manager.apply_function(h3_meditation)
        
    else:
      buff_manager.unregister_buff('Hyper2')
      buff_manager.register_buff(CLASS_BUFF_DICT['Hyper3'], 'class')
      skill_manager.apply_function(h3_meditation)

# Buff Bodies
# 특화 버프
def specialization(character: CharacterLayer, skill: Skill, buff:Buff):
    s = character.get_attribute('specialization')
    s_multiplier = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier)
      
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
    
    s_multiplier = (1 + s * SPEC_COEF_1)

    h_cr = 0.05 * s_multiplier
    h_as = 0.05 * s_multiplier
    h_ce = 0.1 * s_multiplier
    
    h_ad = 1 + ((c_ad - 1)*(1 + h_ce)) + h_ce
    
    character.update_attribute('cooldown_reduction', 1 - (1 - c_cr - h_cr))
    character.update_attribute('movement_speed', c_as + h_as) 
    character.update_attribute('additional_damage', h_ad)

# 금강선공 2단계 버프
def hyper2(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    c_ad = character.get_attribute('additional_damage')
    c_cr = character.get_attribute('cooldown_reduction')
    c_as = character.get_attribute('attack_speed')
    
    s_multiplier = (1 + s * SPEC_COEF_1)
    
    h_cr = 0.1 * s_multiplier
    h_as = 0.1 * s_multiplier
    h_ce = 0.25 * s_multiplier
    
    h_ad = 1 + ((c_ad - 1)*(1 + h_ce)) + h_ce
    
    character.update_attribute('cooldown_reduction', 1 - (1 - c_cr - h_cr))
    character.update_attribute('movement_speed', c_as + h_as) 
    character.update_attribute('additional_damage', h_ad)
    
# 금강선공 3단계 버프
def hyper3(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    c_ad = character.get_attribute('additional_damage')
    c_cr = character.get_attribute('cooldown_reduction')
    c_as = character.get_attribute('attack_speed')
    
    s_multiplier = (1 + s * SPEC_COEF_1)
    
    def robust_spirit_COEF(buff_manager: BuffManager, skill_manager: SkillManager):
      if buff_manager.is_buff_exists('Robust_Spirit'):
        return 0.3
      else:
        return 0;
    
    h_cr = 0.25 * s_multiplier
    h_as = 0.15 * s_multiplier
    h_ce = (0.6 + robust_spirit_COEF) * s_multiplier
  
    h_ad = 1 + ((c_ad - 1)*(1 + h_ce)) + h_ce
    
    character.update_attribute('cooldown_reduction', 1 - (1 - c_cr - h_cr))
    character.update_attribute('movement_speed', c_as + h_as) 
    character.update_attribute('additional_damage', h_ad)
      
# 세맥타통 버프
