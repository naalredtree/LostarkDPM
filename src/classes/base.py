"""
Base buff dictionary and buff bodies
"""
from re import S
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.utils import check_chance

# Buff Dictionary
BASE_BUFF_DICT = {
  'Head_Attack': {
    'name': 'head_attack',
    'buff_type': 'stat',
    'effect': 'head_attack',
    'duration': 999999,
    'priority': 7,
  },
  'Back_Attack': {
    'name': 'back_attack',
    'buff_type': 'stat',
    'effect': 'back_attack',
    'duration': 999999,
    'priority': 7,
  },
}

RUNE_BUFF_DICT = {
  'Bleed_Legendary': {
    'name': '출혈',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 236,
    'coefficient': 2.6875,
    'damage_interval': 1,
    'duration': 6,
    'priority': 7,
  },
  'Bleed_Epic': {
    'name': '출혈',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 236,
    'coefficient': 2.6875,
    'damage_interval': 1,
    'duration': 5,
    'priority': 7,
  },
  'Rage_Legendary': {
    'name': 'rage',
    'buff_type': 'stat',
    'effect': 'rage_legendary',
    'duration': 6,
    'priority': 7,
  },
  'Rage_Epic': {
    'name': 'rage',
    'buff_type': 'stat',
    'effect': 'rage_epic',
    'duration': 6,
    'priority': 7,
  },
  'Judgement_Cooldown': {
    'name': 'judgement_cooldown',
    'buff_type': 'stat',
    'effect': 'judgement_cooldown',
    'duration': 30,
    'priority': 7,
  },
  'Judgement': {
    'name': 'judgement',
    'buff_type': 'stat',
    'effect': 'judgement',
    'duration': 6,
    'priority': 9,
  },
}

COMMON_BUFF_DICT = {
  ###### non-engraving buffs ######
  # 헤드백 시너지
  'Synergy_Head_Back': {
    'name': 'synergy_head_back',
    'buff_type': 'stat',
    'effect': 'synergy_head_back',
    'duration': 999999,
    'priority': 7,
  },
  # 사멸
  'Entropy_Set_1': {
    'name': 'entropy_set',
    'buff_type': 'stat',
    'effect': 'entropy_set_1',
    'duration': 999999,
    'priority': 7,
  },
  'Entropy_Set_2': {
    'name': 'entropy_set',
    'buff_type': 'stat',
    'effect': 'entropy_set_2',
    'duration': 999999,
    'priority': 7,
  },
  'Entropy_Set_3': {
    'name': 'entropy_set',
    'buff_type': 'stat',
    'effect': 'entropy_set_3',
    'duration': 999999,
    'priority': 7,
  },
  # 악몽
  'Nightmare_Set_1': {
    'name': 'nightmare_set',
    'buff_type': 'stat',
    'effect': 'nightmare_set_1',
    'duration': 999999,
    'priority': 7,
  },
  'Nightmare_Set_2': {
    'name': 'nightmare_set',
    'buff_type': 'stat',
    'effect': 'nightmare_set_2',
    'duration': 999999,
    'priority': 7,
  },
  'Nightmare_Set_3': {
    'name': 'nightmare_set',
    'buff_type': 'stat',
    'effect': 'nightmare_set_3',
    'duration': 999999,
    'priority': 7,
  },
  # 2악4구
  'Nig2_Sal4_Set_1': {
    'name': 'nig2_sal4_set',
    'buff_type': 'stat',
    'effect': 'nig2_sal4_set_1',
    'duration': 999999,
    'priority': 7,
  },
  'Nig2_Sal4_Set_2': {
    'name': 'nig2_sal4_set',
    'buff_type': 'stat',
    'effect': 'nig2_sal4_set_2',
    'duration': 999999,
    'priority': 7,
  },
  'Nig2_Sal4_Set_3': {
    'name': 'nig2_sal4_set',
    'buff_type': 'stat',
    'effect': 'nig2_sal4_set_3',
    'duration': 999999,
    'priority': 7,
  },
  ###### engraving buffs ######
  'Raid_Captain_3': {
    'name': 'raid_captain',
    'buff_type': 'stat',
    'effect': 'raid_captain_3',
    'duration': 999999,
    'priority': 1,
  },
  'Super_Charge_3': {
    'name': 'super_charge',
    'buff_type': 'stat',
    'effect': 'super_charge_3',
    'duration': 999999,
    'priority': 7,
  },
  'Master_Brawler_3': {
    'name': 'master_brawler',
    'buff_type': 'stat',
    'effect': 'master_brawler_3',
    'duration': 999999,
    'priority': 7,
  },
  'Master_Of_Ambush_3': {
    'name': 'master_of_ambush',
    'buff_type': 'stat',
    'effect': 'master_of_ambush_3',
    'duration': 999999,
    'priority': 7,
  },
  'Hit_Master_3': {
    'name': 'hit_master',
    'buff_type': 'stat',
    'effect': 'hit_master_3',
    'duration': 999999,
    'priority': 7,
  },
  'All_Out_Attack_3': {
    'name': 'all_out_attack',
    'buff_type': 'stat',
    'effect': 'all_out_attack_3',
    'duration': 999999,
    'priority': 7,
  },
}

"""
Buff Bodies
"""
# System-based buffs
def head_attack(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('head_attack') == True:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.2)

def back_attack(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('back_attack') == True:
      s_dm = skill.get_attribute('damage_multiplier')
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('damage_multiplier', s_dm * 1.05)
      skill.update_attribute('additional_crit_rate', s_acr + 0.10)

# Rune derived buffs


# Non-engraving buffs
# 헤드백 시너지
def synergy_head_back(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    if skill.get_attribute('back_attack') == True or skill.get_attribute('head_attack') == True:
      skill.update_attribute('damage_multiplier', s_dm * 1.12)
    else:
      skill.update_attribute('damage_multiplier', s_dm * 1.03)
# 광분
def rage_legendary(character: CharacterLayer, skill: Skill, buff: Buff):
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('attack_speed', c_as + 0.16)
    character.update_attribute('movement_speed', c_ms + 0.16)
    

def rage_epic(character: CharacterLayer, skill: Skill, buff: Buff):
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('attack_speed', c_as + 0.12)
    character.update_attribute('movement_speed', c_ms + 0.12)
    

# Artifact buffs
# 환각, 구원 -> engraving layer
# 지배
def dominion_set_1(character: CharacterLayer, skill: Skill, buff: Buff):
    pass
# 사멸
def entropy_set_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_cr = character.get_attribute('crit_rate')
    character.update_attribute('crit_rate', c_cr + 0.17)
    if skill.get_attribute('back_attack') == True or skill.get_attribute('head_attack') == True:
      c_cd = character.get_attribute('crit_damage')
      s_dm = skill.get_attribute('damage_multiplier')
      character.update_attribute('crit_damage', c_cd + 0.55)
      skill.update_attribute('damage_multiplier', s_dm * 1.21)
    else:
      c_cd = character.get_attribute('crit_damage')
      s_dm = skill.get_attribute('damage_multiplier')
      character.update_attribute('crit_damage', c_cd + 0.17)
      skill.update_attribute('damage_multiplier', s_dm * 1.07)

def entropy_set_2(character: CharacterLayer, skill: Skill, buff: Buff):
    c_cr = character.get_attribute('crit_rate')
    character.update_attribute('crit_rate', c_cr + 0.20)
    if skill.get_attribute('back_attack') == True or skill.get_attribute('head_attack') == True:
      c_cd = character.get_attribute('crit_damage')
      s_dm = skill.get_attribute('damage_multiplier')
      character.update_attribute('crit_damage', c_cd + 0.60)
      skill.update_attribute('damage_multiplier', s_dm * 1.24)
    else:
      c_cd = character.get_attribute('crit_damage')
      s_dm = skill.get_attribute('damage_multiplier')
      character.update_attribute('crit_damage', c_cd + 0.20)
      skill.update_attribute('damage_multiplier', s_dm * 1.08)

def entropy_set_3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_cr = character.get_attribute('crit_rate')
    character.update_attribute('crit_rate', c_cr + 0.22)
    if skill.get_attribute('back_attack') == True or skill.get_attribute('head_attack') == True:
      c_cd = character.get_attribute('crit_damage')
      s_dm = skill.get_attribute('damage_multiplier')
      character.update_attribute('crit_damage', c_cd + 0.65)
      skill.update_attribute('damage_multiplier', s_dm * 1.26)
    else:
      c_cd = character.get_attribute('crit_damage')
      s_dm = skill.get_attribute('damage_multiplier')
      character.update_attribute('crit_damage', c_cd + 0.22)
      skill.update_attribute('damage_multiplier', s_dm * 1.09)

# 악몽
def nightmare_set_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ad = character.get_attribute('additional_damage')
    c_dm = character.get_attribute('damage_multiplier')
    character.update_attribute('additional_damage', c_ad + 0.15)
    character.update_attribute('damage_multiplier', c_dm * 1.15)
    if skill.get_attribute('mana_cost') > 0:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.12)
      
def nightmare_set_2(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ad = character.get_attribute('additional_damage')
    c_dm = character.get_attribute('damage_multiplier')
    character.update_attribute('additional_damage', c_ad + 0.18)
    character.update_attribute('damage_multiplier', c_dm * 1.18)
    if skill.get_attribute('mana_cost') > 0:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.15)

def nightmare_set_3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ad = character.get_attribute('additional_damage')
    c_dm = character.get_attribute('damage_multiplier')
    character.update_attribute('additional_damage', c_ad + 0.20)
    character.update_attribute('damage_multiplier', c_dm * 1.20)
    if skill.get_attribute('mana_cost') > 0:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.17)

# 2악4구
def nig2_sal4_set_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ad = character.get_attribute('additional_damage')
    character.update_attribute('additional_damage', c_ad + 0.14)
    if skill.get_attribute('mana_cost') > 0:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.12)
      
def nig2_sal4_set_2(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ad = character.get_attribute('additional_damage')
    character.update_attribute('additional_damage', c_ad + 0.18)
    if skill.get_attribute('mana_cost') > 0:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.15)

def nig2_sal4_set_3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ad = character.get_attribute('additional_damage')
    character.update_attribute('additional_damage', c_ad + 0.21)
    if skill.get_attribute('mana_cost') > 0:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.17)

# Engraving buffs
def raid_captain_3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_dm = character.get_attribute('damage_multiplier')
    c_ams = character.get_attribute('actual_movement_speed')
    character.update_attribute('damage_multiplier', c_dm * (1+(c_ams-1)*0.45))

def super_charge_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('skill_type') == 'Charge':
      s_dm = skill.get_attribute('damage_multiplier')
      s_tsd = skill.get_attribute('type_specific_delay')
      skill.update_attribute('damage_multiplier', s_dm * 1.20)
      skill.update_attribute('type_specific_delay', s_tsd / 1.40)

def master_brawler_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('head_attack') == True:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.25)

def master_of_ambush_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('back_attack') == True:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.25)

def hit_master_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('head_attack') == False and skill.get_attribute('back_attack') == False:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.16)

def all_out_attack_3(character: CharacterLayer, skill: Skill, buff: Buff):
    s_t = skill.get_attribute('skill_type')
    if  s_t == 'Holding_A' or s_t == 'Holding_B' or s_t == 'Casting':
      s_dm = skill.get_attribute('damage_multiplier')
      s_tsd = skill.get_attribute('type_specific_delay')
      skill.update_attribute('damage_multiplier', s_dm * 1.20)
      skill.update_attribute('type_specific_delay', s_tsd / 1.20)


"""
Rune Actions
1: uncommon
2: rare
3: epic
4: legendary
"""
# 속행
def rune_qr_1(buff_manager: BuffManager, skill_manager: SkillManager):
    pass
def rune_qr_2(buff_manager: BuffManager, skill_manager: SkillManager):
    pass
def rune_qr_3(buff_manager: BuffManager, skill_manager: SkillManager):
    skill_manager.rune_ratio['qr'][0] += 1
    def cooldown_reduction(skill: Skill):
      it = skill.get_attribute('identity_type')
      if it == 'Awakening':
        return
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc * 0.88)
      return
    if check_chance(0.10):
      skill_manager.rune_ratio['qr'][1] += 1
      skill_manager.apply_function(cooldown_reduction)
def rune_qr_4(buff_manager: BuffManager, skill_manager: SkillManager):
    skill_manager.rune_ratio['qr'][0] += 1
    def cooldown_reduction(skill: Skill):
      it = skill.get_attribute('identity_type')
      if it == 'Awakening':
        return
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc * 0.84)
      return
    if check_chance(0.10):
      skill_manager.rune_ratio['qr'][1] += 1
      skill_manager.apply_function(cooldown_reduction)

# 광분
def rune_rg_1(buff_manager: BuffManager, skill_manager: SkillManager):
    raise NotImplementedError
def rune_rg_2(buff_manager: BuffManager, skill_manager: SkillManager):
    raise NotImplementedError
def rune_rg_3(buff_manager: BuffManager, skill_manager: SkillManager):
    skill_manager.rune_ratio['rg'][0] += 1
    if check_chance(0.15) and not buff_manager.is_buff_exists('rage'):
      skill_manager.rune_ratio['rg'][1] += 1
      buff_manager.register_buff(RUNE_BUFF_DICT['Rage_Epic'], 'base')
def rune_rg_4(buff_manager: BuffManager, skill_manager: SkillManager):
    skill_manager.rune_ratio['rg'][0] += 1
    if check_chance(0.20):
      skill_manager.rune_ratio['rg'][1] += 1
      buff_manager.unregister_buff('rage')
      buff_manager.register_buff(RUNE_BUFF_DICT['Rage_Legendary'], 'base')

# 출혈
def rune_bd_1(buff_manager: BuffManager, skill_manager: SkillManager):
    raise NotImplementedError
def rune_bd_2(buff_manager: BuffManager, skill_manager: SkillManager):
    raise NotImplementedError
def rune_bd_3(buff_manager: BuffManager, skill_manager: SkillManager):
    if not buff_manager.is_buff_exists('bleed'):
      buff_manager.register_buff(RUNE_BUFF_DICT['Bleed_Epic'], 'base')
def rune_bd_4(buff_manager: BuffManager, skill_manager: SkillManager):
    buff_manager.register_buff(RUNE_BUFF_DICT['Bleed_Legendary'], 'base')


# 심판
def rune_jm_1(buff_manager: BuffManager, skill_manager: SkillManager):
    raise NotImplementedError
def rune_jm_2(buff_manager: BuffManager, skill_manager: SkillManager):
    raise NotImplementedError
def rune_jm_3(buff_manager: BuffManager, skill_manager: SkillManager):
    raise NotImplementedError
def rune_jm_4(buff_manager: BuffManager, skill_manager: SkillManager):
    skill_manager.rune_ratio['jm'][0] += 1
    if not buff_manager.is_buff_exists('judgement_cooldown'):
      skill_manager.rune_ratio['jm'][1] += 1
      buff_manager.register_buff(RUNE_BUFF_DICT['Judgement_Cooldown'], 'base')
      buff_manager.register_buff(RUNE_BUFF_DICT['Judgement'], 'base')

# 심판 버프 및 내부쿨 표시용 더미 버프
def judgement(character: CharacterLayer, skill: Skill, buff: Buff):
    c_cr = character.get_attribute('cooldown_reduction')
    character.update_attribute('cooldown_reduction', 1 - (1 - c_cr) * (1 - 0.15))
def judgement_cooldown(character: CharacterLayer, skill: Skill, buff: Buff):
    return
