class ParseResult:
  def __init__(
    self,
    sp_mods: list[str],
    mods: list[str],
    key: str,
  ):
    self.sp_mods = sp_mods
    self.mods = mods
    self.key = key

  def is_key_only(self) -> bool:
    return len(self.sp_mods) == 0 and len(self.mods) == 0

  def __str__(self) -> str:
    return f"ParseResult(sp_mods={self.sp_mods}, mods={self.mods}, key={self.key})"

  def __eq__(self, other):
    if not isinstance(other, ParseResult):
      return NotImplemented
    return (
      tuple(self.sp_mods) == tuple(other.sp_mods) and
      tuple(self.mods) == tuple(other.mods) and
      self.key == other.key
    )

  def __hash__(self):
    return hash((
      self.key,
      tuple(self.sp_mods),
      tuple(self.mods),
    ))
