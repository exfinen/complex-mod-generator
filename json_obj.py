from base_settings import BaseSettings
from mapping_rule import MappingRule

class JsonObj:
  def __init__(
    self,
    base_settings: BaseSettings,
    mapping_rules: list[MappingRule]
  ):
    sp_mods = base_settings.get_available_sp_mods()
    rule_objs = [x.to_obj(base_settings) for x in mapping_rules]

    self.obj = {
      "description": base_settings.description,
      "manipulators": [sp_mod.to_obj() for sp_mod in sp_mods] + rule_objs,
    }

  def __str__(self) -> str: 
    return "not implemented"

  def get(self) -> object:
    return self.obj

