# complex-mod-rule-generator
Generates a [Karabiner-Elements](https://karabiner-elements.pqrs.org/) complex modification rule JSON from a simpler definition file.

The definition file format supports the concept of left and right layer keys.

# Usage
1. Create a definition file based on the included sample.def (shown below):

   ```python
   # Settings
   description: Sample mapping
   s_layer_left: japanese_eisuu
   s_layer_right: japanese_kana
   s_left_shift: a
   s_right_shift: semicolon

   # Layer 1
   left_control + h: delete_or_backspace
   left_control + m: return_or_enter

   # Layer 2
   LR + q: 1
   LR + w: 2
   LR + e: 3
   LR + r: 4
   LR + t: 5

   LR + SR + q: left_shift + 1 # !
   LR + SR + w: left_shift + 2 # @
   LR + SR + e: left_shift + 3 # #
   LR + SR + r: left_shift + 4 # $
   LR + SR + t: left_shift + 5 # %

   LL + y: 6
   LL + u: 7
   LL + i: 8
   LL + o: 9
   LL + p: 0

   LL + SL + y: left_shift + 6 # ^
   LL + SL + u: left_shift + 7 # &
   LL + SL + i: left_shift + 8 # *
   LL + SL + o: left_shift + 9 # (
   LL + SL + p: left_shift + 0 # )

   # Layer 3
   LL + LR + j: grave_accent_and_tilde 
   LL + LR + k: backslash 
   ```

   The special aliases `LL`, `LR`, `SL` and `SR` represent `sp_layer_left` and `sp_layer_right`, `sp_left_shift` and `sp_right_shift` respectively — these are not native to [Karabiner-Elements](https://karabiner-elements.pqrs.org/), but are logical modifier keys emulated using the event system of [Karabiner-Elements](https://karabiner-elements.pqrs.org/).

   All other key and modifier names in the definition file must match the internal names used by Karabiner-Elements. You can find the correct names by pressing keys in Karabiner-EventViewer, which displays the identifiers to use in your definition file.

2. Translate the definition file to JSON and copy to clipboard:

```bash
python3 builder.py <definition-file> | pbcopy
```

3. Create a rule in `Complex Modifications`, and paste the JSON from your clipboard into it.

