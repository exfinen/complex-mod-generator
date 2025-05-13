from base_settings import BaseSettings
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
      m = base_settings.get_sp_mod_name_to_sp_mod_mapper()
      sp_mods = [m[x] for x in self.lhs.sp_mods]

      obj["conditions"] = [
        {
          "name": sp_mod.get_event_name(),
          "type": "variable_if",
          "value": int(sp_mod.name in self.lhs.sp_mods),
        }
        for sp_mod in sp_mods
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

