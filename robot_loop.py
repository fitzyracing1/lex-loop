#!/usr/bin/env python3
"""Lex loop — an 8-step robot ROM you run beside your planner or controller.

Goals (sense/issue): Read, Transcribe, Issue, Test
Motion/recovery:     Drive, Lean, Escape, Restart

Restart does not call out. It reloads the built-in task table
into the run queue and returns the program counter to Read.

MIT License — see LICENSE. No secrets, no network, no external deps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


# Built into the CPU. Order is the restart image.
BUILTIN_TASKS = (
    "READ",
    "TRANSCRIBE",
    "ISSUE",
    "TEST",
    "DRIVE",
    "LEAN",
    "ESCAPE",
    "RESTART",
)


@dataclass
class Task:
    name: str
    pc: int
    ticks: int = 1
    done: bool = False
    note: str = ""


@dataclass
class CPU:
    """Tiny task CPU. The list lives in ROM. Restart copies ROM into the queue."""

    rom: tuple = BUILTIN_TASKS
    queue: List[Task] = field(default_factory=list)
    log: List[str] = field(default_factory=list)
    cycle: int = 0
    restarts: int = 0

    def restart(self) -> None:
        """Built-in. Wipe the queue and reload the list from ROM."""
        self.restarts += 1
        self.queue = [
            Task(name=name, pc=i, ticks=1) for i, name in enumerate(self.rom)
        ]
        self.log.append(f"RESTART #{self.restarts}: loaded {len(self.queue)} built-in tasks")

    def step(self) -> str:
        if not self.queue:
            self.restart()
        task = self.queue[0]
        self.cycle += 1
        task.ticks -= 1
        line = f"c{self.cycle:03d} pc={task.pc} {task.name}"
        self.log.append(line)
        if task.name == "RESTART":
            # Restart consumes itself, then reloads the whole list.
            self.queue.pop(0)
            self.restart()
            return line
        if task.ticks <= 0:
            task.done = True
            self.queue.pop(0)
        return line


HANDLERS: dict[str, str] = {
    "READ": "sample sensors / inbound text into the register file",
    "TRANSCRIBE": "copy the register file into a plain transcript buffer",
    "ISSUE": "emit the next command from the transcript",
    "TEST": "check the issued command against the expected echo",
    "DRIVE": "apply forward actuator command",
    "LEAN": "shift mass / heading to hold the line",
    "ESCAPE": "break contact and clear the fault pose",
    "RESTART": "reload BUILTIN_TASKS into the run queue; PC returns to READ",
}


def main() -> None:
    cpu = CPU()
    cpu.restart()
    # One full pass plus the restart that arms the next pass.
    for _ in range(len(BUILTIN_TASKS)):
        cpu.step()
    print("ROM (built into the CPU)")
    for i, name in enumerate(BUILTIN_TASKS):
        print(f"  {i}  {name:<12} {HANDLERS[name]}")
    print()
    print("Run")
    for line in cpu.log:
        print(" ", line)
    print()
    print("Queue after restart")
    for t in cpu.queue:
        print(f"  pc={t.pc} {t.name}")


if __name__ == "__main__":
    main()
