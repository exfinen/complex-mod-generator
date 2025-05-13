from typing import Optional

class SpecialModifier:
  def __init__(self, src_key: str, name: str, abbr: str):
    self.src_key = src_key
    self.name = name
    self.abbr = abbr

  def get_event_name(self) -> str:
    return f"{self.name}_pressed"

  def to_obj(self) -> object:
    return {
      "from": {
        "key_code": self.src_key,
        "modifiers": { "optional": ["any"] }
      },
      "parameters": {
        "basic.to_if_alone_timeout_milliseconds": 250,
        "basic.to_if_held_down_threshold_milliseconds": 250
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
      "to_if_alone": [{ "key_code": self.src_key }],
      "type": "basic"
    }

  def __str__(self) -> str:
    return f"SpecialModifier(src_key={self.src_key}, name={self.name}, abbr={self.abbr})"

