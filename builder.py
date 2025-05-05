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

def gen_layer_key_def(layer_key: str, layer_name: str) -> object:
  event = f"{layer_name}_pressed"
  obj = {
    "from": {
      "key_code": layer_key,
      "modifiers": { "optional": ["any"] }
    },
    "parameters": {
      "basic.to_if_alone_timeout_milliseconds": 250,
      "basic.to_if_held_down_threshold_milliseconds": 250
    },
    "to": [
      {
        "set_variable": {
          "name": f"{layer_name}_pressed",
          "value": 1
        }
      }
    ],
    "to_after_key_up": [
      {
        "set_variable": {
          "name": f"{layer_name}_pressed",
          "value": 0
        }
      }
    ],
    "to_if_alone": [{ "key_code": layer_key }],
    "type": "basic"
  }
  return event, obj

def gen_key_def(from_key: str, from_mods: list[str], from_layers: list[str], to_key: str) -> object:
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
        "modifiers": []
      }
    ],
    "type": "basic"
  }

  if len(from_layers) > 0:
    obj["conditions"] = [
      {
        "name": target,
        "type": "variable_if",
        "value": int(target in from_layers),
      }
      for target in (LL, LR)
      if target is not None
    ]

  return obj

LL = None
LR = None

def unalias(key: str) -> str:
  if key == "LL":
    return LL
  elif key == "LR":
    return LR
  else:
    return key

def translate_base_settings(res, lines) -> (object, list[str]):
  global LL, LR

  remaining_lines = []
  for line in lines:
    key = line[0]
    val = line[1]

    if key == "description":
      res["description"] = val
      pass
    elif key in ["layer_left", "layer_right"]:
      event, obj = gen_layer_key_def(val, key)
      res["manipulators"].append(obj)
      if key == "layer_left":
        LL = event
      else:
        LR = event
    else:
      remaining_lines.append(line)
  return res, remaining_lines

def translate_key_defs(ms: list[object], lines) -> object:
  global LL, LR

  for line in lines:
    lhs = [x.strip() for x in line[0].split("+")]
    to_key = line[1]

    from_key = lhs[-1]
    from_non_keys = [unalias(x) for x in lhs[:-1]]

    from_layers = [x for x in from_non_keys if x in (LL, LR)]
    from_mods = [x for x in from_non_keys if x not in (LL, LR)]

    obj = gen_key_def(from_key, from_mods, from_layers, to_key) 
    ms.append(obj)

  return ms

args = parse_args();

lines = []
with open(args.file, 'r', encoding='utf-8') as f:
  for line in f:
    line = line.strip()
    if line.startswith('#') or len(line) == 0:
      continue
    lines.append(line)

lines = [parse_line(line) for line in lines]

obj = {
  "manipulators": [],
}
obj, ms = translate_base_settings(obj, lines)
obj["manipurators"] = translate_key_defs(obj["manipulators"], ms)

print(json.dumps(obj, indent=2))

