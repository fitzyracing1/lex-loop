# Lex loop

Lex is an 8-step robot ROM you run beside your planner/controller to catch skipped sense, missing tests, and stuck poses.

Repo: [github.com/fitzyracing1/lex-loop](https://github.com/fitzyracing1/lex-loop)

## The loop

```
READ → TRANSCRIBE → ISSUE → TEST → DRIVE → LEAN → ESCAPE → RESTART
```

| Step | Meaning |
|------|---------|
| **READ** | Sample sensors / inbound text into the register file |
| **TRANSCRIBE** | Copy the register file into a plain transcript buffer |
| **ISSUE** | Emit the next command from the transcript |
| **TEST** | Check the issued command against the expected echo |
| **DRIVE** | Apply forward actuator command |
| **LEAN** | Shift mass / heading to hold the line |
| **ESCAPE** | Break contact and clear the fault pose |
| **RESTART** | Reload BUILTIN_TASKS into the run queue; PC returns to READ |

The list lives in ROM. Restart copies ROM into the run queue. No external call, no secrets, no deps.

## Why it exists

Planners and agents often:

- skip **TEST** (issue a command and move on)
- never **ESCAPE** (stay in a fault pose)
- never **RESTART** (no clean return to sense)

Lex makes those steps first-class. It does not replace your stack. It sits beside it so the gaps are visible.

## How to try it

```bash
python robot_loop.py
```

One full cycle plus the restart that arms the next pass. You should see the ROM printed, eight step lines, then the queue reloaded at READ.

## How to use beside your work

**Humanoid / robot software**

- Map each of the eight names to a real stage in your sense → plan → act → recover path.
- Fail the cycle (or raise a flag) if TEST is skipped after ISSUE.
- Fail the cycle if ESCAPE never runs when a fault pose is held past a timeout.
- Treat RESTART as a real reload of the task table, not a soft reset of one module.

**Coding agents**

- Run Lex once per task (or once per agent turn).
- Fail the cycle if the agent never exercised TEST (no check against expected output).
- Fail the cycle if ESCAPE never fires when the agent is stuck (same error, same pose, no breakout).
- Use the printed log as a checklist, not as a claim that Lex “fixes” the agent.

Paste [CONSIDER.md](CONSIDER.md) into other project docs if you want a short, shareable version of this ask.

## Consider this

If you build robots, sims, or agents: try Lex next to your stack for a few cycles. Keep your planner. Keep your controller. Just notice whether TEST, ESCAPE, and RESTART actually fire. If something useful turns up, open an issue or point others here.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Joshua Almeida / fitzyracing1.

This is a small open pattern, not a product claim. It will not make your robot walk or your agent smarter by itself.

## Documentation

- In-repo docs: [docs/](docs/index.md)
- Wiki: [https://github.com/fitzyracing1/lex-loop/wiki](https://github.com/fitzyracing1/lex-loop/wiki)
