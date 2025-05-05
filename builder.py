import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(description="Karabiner Elements key mapping rule JSON generator")
    parser.add_argument(
        'file',
        type=str,
        help='Mappingw rule definition file',
    )
    return parser.parse_args()

def parse_line(line: str) -> list[str]:
  toks = line.split(":", 1)
  if len(toks) != 2:
    raise ValueError(f"Malformed line found: {line}")
  return [tok.strip() for tok in toks]

def gen_sp_key_def(sp_key: str, sp_key_name: str) -> object:
  sp_key_pressed = f"{sp_key_name}_pressed"
  obj = {
    "from": {
      "key_code": sp_key,
      "modifiers": { "optional": ["any"] }
    },
    "parameters": {
      "basic.to_if_alone_timeout_milliseconds": 250,
      "basic.to_if_held_down_threshold_milliseconds": 250
    },
    "to": [
      {
        "set_variable": {
          "name": sp_key_pressed,
          "value": 1
        }
      }
    ],
    "to_after_key_up": [
      {
        "set_variable": {
          "name": sp_key_pressed,
          "value": 0
        }
      }
    ],
    "to_if_alone": [{ "key_code": sp_key }],
    "type": "basic"
  }
  return sp_key_pressed, obj

def gen_key_def(
  from_key: str,
  from_mods: list[str],
  from_sp_key_events: list[str],
  to_key: str,
  to_mods: list[str],
) -> object:
  obj = {
    "from": {
      "key_code": from_key,
      "modifiers": {
        "mandatory": from_mods,
        "optional": ["any"]
      }
    },
    "to": [
      {
        "key_code": to_key,
        "modifiers": to_mods,
      }
    ],
    "type": "basic"
  }

  if len(from_sp_key_events) > 0:
    obj["conditions"] = [
      {
        "name": sp_key_event,
        "type": "variable_if",
        "value": int(sp_key_event in from_sp_key_events),
      }
      for sp_key_event in SP_KEY_EVENTS
      if sp_key_event is not None
    ]

  return obj

LL = None
LR = None
SL = None
SR = None
 
# values will be set in translate_base_settings
SP_KEY_EVENTS = (LL, LR, SL, SR)

def unalias(key: str) -> str:
  if key == "LL":
    return LL
  elif key == "LR":
    return LR
  elif key == "SL":
    return SL
  elif key == "SR":
    return SR
  else:
    return key

def translate_base_settings(obj, lines) -> (object, list[str]):
  global LL, LR, SL, SR, SP_KEY_EVENTS

  remaining_lines = []
  for line in lines:
    key = line[0]
    val = line[1]

    if key == "description":
      obj["description"] = val
    elif key.startswith("s_"):
      sp_key_pressed, child_obj = gen_sp_key_def(val, key)
      obj["manipulators"].append(child_obj)
      if key == "s_layer_left":
        LL = sp_key_pressed
      elif key == "s_layer_right":
        LR = sp_key_pressed
      elif key == "s_left_shift":
        SL = sp_key_pressed
      elif key == "s_right_shift":
        SR = sp_key_pressed
      else:
        raise ValueError(f"Unhandled special key: {key}")
    else:
      remaining_lines.append(line)

  SP_KEY_EVENTS = (LL, LR, SL, SR)

  return obj, remaining_lines

def translate_key_defs(ms: list[object], lines) -> object:
  for line in lines:
    # lhs
    lhs = [x.strip() for x in line[0].split("+")]

    from_key = lhs[-1]
    from_others = [unalias(x) for x in lhs[:-1]]

    from_sp_key_events = [x for x in from_others if x in SP_KEY_EVENTS]
    from_mods = [x for x in from_others if x not in SP_KEY_EVENTS]

    # rhs
    rhs = [x.strip() for x in line[1].split("+")]
    to_key = rhs[-1]
    to_mods = [x for x in rhs[:-1]]

    obj = gen_key_def(from_key, from_mods, from_sp_key_events, to_key, to_mods) 
    ms.append(obj)

  return ms

args = parse_args();

lines = []
with open(args.file, 'r', encoding='utf-8') as f:
  for line in f:
    line = line.strip()

    # skip empty lines and comments
    if line.startswith('#') or len(line) == 0:
      continue

    # remove inline comment if exists
    if "#" in line:
      line = line.split("#", 1)[0].strip()

    lines.append(line)

lines = [parse_line(line) for line in lines]

obj = {
  "manipulators": [],
}
obj, ms = translate_base_settings(obj, lines)

obj["manipurators"] = translate_key_defs(obj["manipulators"], ms)

print(json.dumps(obj, indent=2))

