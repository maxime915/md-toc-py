# Headers rule

**underline header** (`===` / `---`):
- max 3 blank space before
- min 1 `=` or `-` (no max)

**diese header** (#):
- max 3 blank space before the first `#`
- min 1 and max 6 `#`

**quote block**:
- starting with `>` (may be nested undefinitely, max 4 spaces between each `>`)
- can contain header only if `#` if the first non white nor `>` character
- *not to include in a table of content* (because it is quoted)

**code block**:
- start with at least 4 spaces or at least 1 tab or ` ``` ` or ``` ` ```
- ignore the header in them
- max 3 spaces before ` ``` `
- -> no need to check inline code (``` ` ```) since then the `#` char could not be the firs
- -> no need to prevent 4 space / 1 tab before there should be max 3 space before the first `#`

**invalid text for header**:
- quoted
- list
- code block
- header line (`#...`)
- line full of `=` or `-`
