from parse_result import ParseResult
from special_modifier import SpecialModifier
from typing import Dict

S_LAYER_LEFT = "s_layer_left"
S_LAYER_RIGHT = "s_layer_right"
S_LEFT_SHIFT = "s_left_shift"
S_RIGHT_SHIFT = "s_right_shift"

SP_MOD_ABBRS = ["LL", "LR", "SL", "SR"]

class BaseSettings():
  def __init__(self):
    self.description = None
    self.LL = None
    self.LR = None
    self.SL = None
    self.SR = None

  def try_consume(self, line_no: int, lhs: ParseResult, rhs: ParseResult) -> bool:
    """Returns True if the line is consumed, False otherwise."""
    if lhs.is_key_only() and lhs.key == "description" and rhs.is_key_only():
      self.description = rhs.key
      return True
    elif lhs.key.startswith("s_"):
      # SpecialModifiers shouldn't have modifiers on the rhs
      if not rhs.is_key_only():
        raise ValueError(f"Special modifier mapped to modifier keys at {line_no}")

      if lhs.key == S_LAYER_LEFT:
        self.LL = SpecialModifier(rhs.key, lhs.key, "LL")

      elif lhs.key == S_LAYER_RIGHT:
        self.LR = SpecialModifier(rhs.key, lhs.key, "LR")

      elif lhs.key == S_LEFT_SHIFT:
        self.SL = SpecialModifier(rhs.key, lhs.key, "SL")

      elif lhs.key == S_RIGHT_SHIFT:
        self.SR = SpecialModifier(rhs.key, lhs.key, "SR")

      else:
        raise ValueError(f"Unknown special modifier key: {lhs.key} at {line_no}")
      return True
    return False

  def get_available_sp_mods(self) -> list[SpecialModifier]:
    xs = []

    if self.LL is not None:
      xs.append(self.LL)

    if self.LR is not None:
      xs.append(self.LR)

    if self.SL is not None:
      xs.append(self.SL)

    if self.SR is not None:
      xs.append(self.SR)

    return xs
      
  def get_sp_mod_abbr_to_name_mapper(self) -> Dict[str, str]:
    return {x.abbr: x.name for x in self.get_available_sp_mods()}

  def get_sp_mod_name_to_sp_mod_mapper(self) -> Dict[str, SpecialModifier]:
    return {x.name: x for x in self.get_available_sp_mods()}

  def validate(self):
    if self.description is None:
      raise ValueError("description is required")

