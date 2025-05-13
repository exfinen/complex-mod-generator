from base_settings import BaseSettings
from mapping_rule import MappingRule
from parse_result import ParseResult
from util import strip_split
import copy

def expand_aggr_sp_mods(src_mr: MappingRule) -> list[MappingRule]:
  """
  expands MappingRule if it contains aggregated special modifie in lhs[0]
  """
  if len(src_mr.lhs.sp_mods) > 0 and "," in src_mr.lhs.sp_mods[0]:
    sp_mods_0_str = src_mr.lhs.sp_mods[0]
    sp_mods_0s = strip_split(sp_mods_0_str, ",")
    mrs = []
    for sp_mods_0 in sp_mods_0s:
      mr = copy.deepcopy(src_mr)
      mr.lhs.sp_mods[0] = sp_mods_0
      mrs.append(mr)
    return mrs
  else:
    return [src_mr]

def expand_sp_mods(
  base_settings: BaseSettings,
  mrs: list[MappingRule],
) -> list[MappingRule]:
  """Expands special modifiers in lhs"""
  sp_mod_map = base_settings.get_sp_mod_abbr_to_name_mapper()
  for mr in mrs:
    for i in range(len(mr.lhs.sp_mods)):
      if mr.lhs.sp_mods[i] in sp_mod_map:
        mr.lhs.sp_mods[i] = sp_mod_map[mr.lhs.sp_mods[i]]
  return mrs

def expand(
  base_settings: BaseSettings,
  src_mr: MappingRule,
) -> list[MappingRule]:
  """
  Expands LL, LR, SL, SR into special modifier abbrs.
  Also expands aggregated special modifiers in sp_mods[0] into multiple lines.
  """
  mrs = expand_aggr_sp_mods(src_mr)
  mrs = expand_sp_mods(base_settings, mrs)
  
  return mrs

