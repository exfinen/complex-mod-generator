from typing import Callable
from parse_result import ParseResult
from typing import Optional, Tuple
from util import strip_split
from base_settings import SP_MOD_ABBRS

class LineParser:
  @staticmethod
  def partition(xs: list[str], p: Callable[[str], bool]) -> Tuple[list[str], list[str]]:
    ts = []
    fs = []
    for x in xs:
      if p(x):
        ts.append(x)
      else:
        fs.append(x)
    return ts, fs

  @staticmethod
  def parse(line_no: int, s: str) -> Optional[Tuple[ParseResult, ParseResult]]:
    """
    Returns (lhs, ths) if the line is valid, None otherwise.
    Does not expand macros.

    Line format:

    lhs : rhs
    lhs: (mod_key (+ mod_key)* +)* key
    rhs: (mod_key (+ mod_key)*)* +) key
    mod_key: sp_mod_keys | norm_mod_key
    sp_mod_keys: sp_mod_key (, sp_mod_key)*
    """
    # remove inline comment
    if "#" in s:
      s = s.split("#", 1)[0].strip()

    # return no reuslt if the line is comment only
    if s == "":
      return None

    # split lhs and rhs by ':'
    toks = s.split(":", 1)
    if len(toks) != 2:
      return None

    lhs = toks[0].strip()
    rhs = toks[1].strip()
    if lhs == "" or rhs == "":
      return None

    # parse lhs
    lhs_toks = strip_split(lhs, "+")

    lhs_key = lhs_toks[-1]
    lhs_others = lhs_toks[:-1]

    is_sp_mod_abbr = lambda x: x in SP_MOD_ABBRS or "," in x

    # classify modifiers into sp and normal ones
    lhs_sp_mods, lhs_mods = LineParser.partition(
      lhs_others, is_sp_mod_abbr
    )

    # parse rhs
    rhs_toks = strip_split(rhs, "+")

    rhs_key = rhs_toks[-1]
    rhs_others = rhs_toks[:-1]

    # classify modifiers into sp and normal ones
    rhs_sp_mods, rhs_mods = LineParser.partition(
      rhs_others, is_sp_mod_abbr
    )

    # rhs should not have sp_mods
    if len(rhs_sp_mods) != 0:
      raise ValueError(f"found mapping to special modifier keys at {line_no}: {s}")

    lhs_result = ParseResult(
      sp_mods=lhs_sp_mods,
      mods=lhs_mods,
      key=lhs_key,
    )
    rhs_result = ParseResult(
      sp_mods=[],
      mods=rhs_mods,
      key=rhs_key,
    )
    return lhs_result, rhs_result

