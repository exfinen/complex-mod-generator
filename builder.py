import argparse
import json
from base_settings import BaseSettings
from json_obj import JsonObj
from line_parser import LineParser
from macro import expand
from mapping_rule import MappingRule
from util import remove_duplicates

def parse_args():
  parser = argparse.ArgumentParser(description="Karabiner layered mapper")
  parser.add_argument(
      'file',
      type=str,
      help='Definition file',
  )
  return parser.parse_args()

args = parse_args();

base_settings = BaseSettings()
mapping_rules = []

with open(args.file, 'r', encoding='utf-8') as f:
  line_no = 0

  for s in f:
    line_no += 1
    res = LineParser.parse(line_no, s)
    if res is None:
      continue
    lhs, rhs = res

    # first try to parse a line as base setting line.
    # if the line is not for base setting,
    # parse the line as a mapping rule line
    if not base_settings.try_consume(line_no, lhs, rhs):
      src_mr = MappingRule(line_no, lhs, rhs)
      for mr in expand(base_settings, src_mr):
        mapping_rules.append(mr)

base_settings.validate()
mapping_rules = remove_duplicates(mapping_rules)

json_obj = JsonObj(base_settings, mapping_rules)

print(json.dumps(json_obj.get(), indent=2))

