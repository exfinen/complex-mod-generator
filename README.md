# complex-mod-rule-generator
Generates a [Karabiner-Elements](https://karabiner-elements.pqrs.org/) complex modification rule JSON from a simpler definition file.

The definition file format supports the concept of left and right layer keys.

# Usage
1. Create a definition file based on the included sample.def (shown below):

   ```python
   # Settings
   description: Sample mapping
   layer_left: japanese_eisuu
   layer_right: japanese_kana

   # Layer 1
   left_control + h: delete_or_backspace
   left_control + m: return_or_enter

   # Layer 2
   LR + q: 1
   LR + w: 2
   LR + e: 3
   LR + r: 4
   LR + t: 5

   LL + y: 6
   LL + u: 7
   LL + i: 8
   LL + o: 9
   LL + p: 0

   # Layer 3
   LL + LR + j: grave_accent_and_tilde 
   LL + LR + k: backslash
   ```

   The special aliases `LL` and `LR` represent `layer_left` and `layer_right`, respectively — these are not native to [Karabiner-Elements](https://karabiner-elements.pqrs.org/), but are logical layer keys emulated using the event system of [Karabiner-Elements](https://karabiner-elements.pqrs.org/). All other key names must exactly match the symbols shown in `Karabiner-EventViewer` when the corresponding physical key is pressed.

2. Translate the definition file to JSON and copy to clipboard:

```bash
python3 builder.py <definition-file> | pbcopy
```

3. Create a rule in `Complex Modifications`, and paste the JSON from your clipboard into it.

