from mapping_rule import MappingRule

def strip_split(s: str, char: str) -> list[str]:
  xs = s.split(char)
  return [x.strip() for x in xs]

def remove_duplicates(xs: list[MappingRule]) -> list[MappingRule]:
  seen = set()
  return [x for x in xs if x not in seen and not seen.add(x)]


