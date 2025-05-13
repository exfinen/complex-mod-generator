def strip_split(s: str, char: str) -> list[str]:
  xs = s.split(char)
  return [x.strip() for x in xs]


