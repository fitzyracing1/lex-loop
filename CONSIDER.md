# Consider testing with the Lex loop

Lex is an 8-step robot ROM you run **beside** your planner, controller, or coding agent — not instead of it. It makes sense, test, escape, and restart first-class so those steps are harder to skip.

## The 8 steps

| Step | Meaning |
|------|---------|
| **READ** | Sample sensors / inbound text into the register file |
| **TRANSCRIBE** | Copy the register file into a plain transcript buffer |
| **ISSUE** | Emit the next command from the transcript |
| **TEST** | Check the issued command against the expected echo |
| **DRIVE** | Apply forward actuator command |
| **LEAN** | Shift mass / heading to hold the line |
| **ESCAPE** | Break contact and clear the fault pose |
| **RESTART** | Reload the built-in task list; PC returns to READ |

## How to try it

```bash
python robot_loop.py
```

One cycle plus restart. No deps, no network, MIT.

## How to report results

If you run Lex next to your stack, a short note helps everyone:

1. What you ran it beside (humanoid stack, sim, coding agent, etc.)
2. Whether TEST was skipped or ESCAPE never fired in your normal path
3. What you changed (or didn’t) after seeing the gap
4. Link or paste: https://github.com/fitzyracing1/lex-loop

Open an issue or PR on that repo, or mention Lex in your own docs with a pointer back. No signup, no telemetry — just the pattern.
