from __future__ import annotations
from typing import Optional
from util import strip_split

class SpecialModifier:
  def __init__(
    self,
    src_key: str,
    name: str,
    abbr: str,
    tap_key: Optional[str],
    threshold: int,
  ):
    self.src_key = src_key
    self.name = name
    self.abbr = abbr
    self.tap_key = tap_key
    self.threshold = threshold

  @staticmethod
  def of(src_key: str, name: str, abbr: str) -> Optional[SpecialModifier]:
    # src_key can contain tap key definition
    tap_key = None
    threshold = 250
    if "," in src_key:
      toks = strip_split(src_key, ",")
      match len(toks):
        case 2:
          tap_key = toks[1]
        case 3:
          tap_key = toks[1]
          threshold = int(toks[2])
        case _:
          return None
      src_key = toks[0]

    return SpecialModifier(src_key, name, abbr, tap_key, threshold)

  def get_event_name(self) -> str:
    return f"{self.name}_pressed"

  def to_obj(self) -> object:
    tap_key = self.src_key if self.tap_key is None else self.tap_key
    return {
      "from": {
        "key_code": self.src_key,
        "modifiers": { "optional": ["any"] }
      },
      "parameters": {
        "basic.to_if_alone_timeout_milliseconds": self.threshold,
        "basic.to_if_held_down_threshold_milliseconds": self.threshold,
      },
      "to": [
        {
          "set_variable": {
            "name": self.get_event_name(),
            "value": 1
          }
        }
      ],
      "to_after_key_up": [
        {
          "set_variable": {
            "name": self.get_event_name(),
            "value": 0
          }
        }
      ],
      "to_if_alone": [{ "key_code": tap_key }],
      "type": "basic"
    }

  def __str__(self) -> str:
    return f"SpecialModifier(src_key={self.src_key}, name={self.name}, abbr={self.abbr})"

