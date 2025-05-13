from parse_result import ParseResult
from special_modifier import SpecialModifier
from typing import Dict

S_LAYER_LEFT = "s_layer_left"
S_LAYER_RIGHT = "s_layer_right"

SP_MOD_ABBRS = ["LL", "LR"]

class BaseSettings():
  def __init__(self):
    self.description = None
    self.LL = None
    self.LR = None

  def try_consume(self, line_no: int, lhs: ParseResult, rhs: ParseResult) -> bool:
    """Returns True if the line is consumed, False otherwise."""
    if lhs.is_key_only() and lhs.key == "description" and rhs.is_key_only():
      self.description = rhs.key
      return True
    elif lhs.key.startswith("s_"):
      # lhs and rhs should not contain modifiers
      if not lhs.is_key_only() or not rhs.is_key_only():
        raise ValueError(f"Special modifier def contains modifier keys at {line_no}")

      if lhs.key == S_LAYER_LEFT:
        if self.LL is not None:
          raise ValueError(f"Duplicate def for {lhs.key} at {line_no}")
        self.LL = SpecialModifier(rhs.key, lhs.key, "LL")

      elif lhs.key == S_LAYER_RIGHT:
        if self.LR is not None:
          raise ValueError(f"Duplicate def for {lhs.key} at {line_no}")
        self.LR = SpecialModifier(rhs.key, lhs.key, "LR")

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

    return xs
      
  def get_sp_mod_abbr_to_name_mapper(self) -> Dict[str, str]:
    return {x.abbr: x.name for x in self.get_available_sp_mods()}

  def get_sp_mod_name_to_sp_mod_mapper(self) -> Dict[str, SpecialModifier]:
    return {x.name: x for x in self.get_available_sp_mods()}

  def validate(self):
    if self.description is None:
      raise ValueError("description is required")

