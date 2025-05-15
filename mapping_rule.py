from base_settings import BaseSettings, ALL_SP_MOD_ABBRS
from parse_result import ParseResult

class MappingRule():
  def __init__(self, line_no: int, lhs: ParseResult, rhs: ParseResult):
    self.line_no = line_no
    self.lhs = lhs
    self.rhs = rhs

  def __str__(self) -> str:
    return f"MappingRule(line_no={self.line_no}, lhs={self.lhs}, rhs={self.rhs})"

  def to_obj(self, base_settings: BaseSettings) -> object:
    obj = {
      "from": {
        "key_code": self.lhs.key,
        "modifiers": {
          "mandatory": self.lhs.mods,
          "optional": ["any"]
        }
      },
      "to": [
        {
          "key_code": self.rhs.key,
          "modifiers": self.rhs.mods,
        }
      ],
      "type": "basic"
    }

    if len(self.lhs.sp_mods) > 0:
      # get SpecialModifier objects from names
      abbr_to_sp_mod = base_settings.get_sp_mod_name_to_obj_mapper()

      obj["conditions"] = [
        {
          "name": abbr_to_sp_mod[abbr].get_event_name(),
          "type": "variable_if",
          "value": int(abbr_to_sp_mod[abbr].name in self.lhs.sp_mods),
        }
        for abbr in ALL_SP_MOD_ABBRS
      ]

    return obj

  def __eq__(self, other):
    if not isinstance(other, MappingRule):
      return NotImplemented
    return (
      self.line_no == other.line_no and
      self.lhs == other.lhs and
      self.rhs == other.rhs
    )

  def __hash__(self):
    return hash((self.line_no, self.lhs, self.rhs))

