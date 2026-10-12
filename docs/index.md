# Lex loop

Lex is an 8-step robot "ROM" that runs beside your planner, controller or coding agent. Its job is to make skipped sense, missing tests and stuck poses visible. It is a single dependency-free Python script (`robot_loop.py`).

```
READ → TRANSCRIBE → ISSUE → TEST → DRIVE → LEAN → ESCAPE → RESTART
```

| Step | Meaning |
|---|---|
| READ | sample sensors or inbound text into the register file |
| TRANSCRIBE | copy the register file into a transcript buffer |
| ISSUE | emit the next command from the transcript |
| TEST | check the issued command against the expected echo |
| DRIVE | apply the forward actuator command |
| LEAN | shift mass or heading to hold the line |
| ESCAPE | break contact and clear the fault pose |
| RESTART | reload `BUILTIN_TASKS` into the run queue, and the PC returns to READ |

## Getting started

```bash
python robot_loop.py
```

It prints the ROM, eight step lines, and then the queue reloaded at READ.

## Using it beside your work

Map each step to a real stage of your pipeline. Fail the cycle if TEST is skipped after ISSUE, or if ESCAPE never runs while a fault persists. [CONSIDER.md](../CONSIDER.md) is a shareable short version.

The README says plainly that Lex is a small open pattern, not a product. It will not make a robot walk or an agent smarter by itself.

## License

MIT (see LICENSE). Copyright (c) 2026 Joshua Almeida
