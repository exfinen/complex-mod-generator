# karabiner-layered-mapper
Generates a [Karabiner-Elements](https://karabiner-elements.pqrs.org/) complex modification rule JSON from a rule definition file.

## Definition file
The definition file format supports virtual layer keys and shift keys, enabling layer-based key mapping commonly used in custom keyboards.

### Structure
The definition file consists of:

- One required description line
- Zero or more special modifier ID mappings
- Zero or more key mapping rules

### Line format

- Lines may include comments using `#`. A `#` can appear anywhere, including at the beginning of the line. Everything after it is ignored.
- Whitespace is insignificant and can be added for readability.
- Karabiner key and modifier IDs must match the internal names used by Karabiner-Elements. You can find the correct names by pressing keys in Karabiner-EventViewer, which shows the exact identifiers to use.

These rules apply to all line types described below.

For examples, see [sample.def](https://github.com/exfinen/karabiner-layered-mapper/blob/main/sample.def).

#### Description line

```
description: <description>
```

Defines a description for the configuration.

#### Special Modifier ID Mappings

The following special modifier IDs are available:

| ID             | Alias | Description |
|----------------|----|------------|
| sp_layer_left  | LL | Left Layer |
| sp_layer_right | LR | Right Layer |

Each special modifier ID can optionally be mapped to a Karabiner key ID using the following format:

```
<special_modifier_ID> : <Karabiner_key_ID>
```

You may define only the ones you use. It’s perfectly fine to omit unused special modifier IDs.

⚠️  Aliases (LL, LR, etc.) cannot be used on the left-hand side of these mappings.

#### Key mapping lines

The format is:

```
<From> : <To>
```

`<From>` is zero or more Karabiner or special modifier IDs followed by one Karabiner key ID joined by `+` character.

`<To>` is zero or more Karabiner modifier IDs followed by one Karabiner key ID.

#### Macros
The first element in the `<from>` section can be an `aggregated special modifier ID` (a comma-separated list). When that first element is comma-separated, the line will expand into one rule per listed modifier.

For example, the following mapping rule:

``` 
LL,LR + b: left_shift + equal_sign
```

will be expanded to:

```
LL + b: left_shift + equal_sign
LR + b: left_shift + equal_sign
```

Note that this expansion applies only to the first element in the `<from>` section.

## Usage
1. Create a definition file

2. Generate the key mapping JSON and copy it to the clipboard:

   ```bash
   python3 builder.py <definition-file> | pbcopy
   ```

3. Create a rule in `Complex Modifications`, and paste the JSON from your clipboard into it.

