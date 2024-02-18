from enum import Enum
from dataclasses import dataclass, field
from sre_constants import MAGIC
from typing import List, DefaultDict
from collections import defaultdict, deque
import math
import copy


# I implemented all of the hashing for memoization
# but ended up going with a different method


class Pulse(Enum):
    HIGH = "HIGH"
    LOW = "LOW"


@dataclass
class OutputModule:
    module_type: str = "output"
    sending_pulse: Pulse = Pulse.LOW
    destination: List[str] = field(default_factory=list)
    will_send: bool = False

    def receive(self, source: str, pulse: Pulse):
        pass

    def __hash__(self):
        return hash(
            (
                self.module_type,
                self.sending_pulse,
                tuple(self.destination),
                self.will_send,
            )
        )


@dataclass
class FlipFlop:
    module_type: str = "%"
    sending_pulse: Pulse = Pulse.LOW
    destination: List[str] = field(default_factory=list)
    state: str = "OFF"
    will_send: bool = False

    def receive(self, source: str, pulse: Pulse):
        if pulse == Pulse.LOW:
            if self.state == "OFF":
                self.sending_pulse = Pulse.HIGH
                self.state = "ON"
                self.will_send = True
            else:
                self.sending_pulse = Pulse.LOW
                self.state = "OFF"
                self.will_send = True
        else:
            self.will_send = False

    def __hash__(self):
        return hash(
            (
                self.module_type,
                self.sending_pulse,
                tuple(self.destination),
                self.state,
                self.will_send,
            )
        )


@dataclass
class Conjunction:
    module_type: str = "&"
    sending_pulse: Pulse = Pulse.LOW
    memory: DefaultDict[str, Pulse] = field(
        default_factory=lambda: defaultdict(lambda: Pulse.LOW)
    )
    destination: List[str] = field(default_factory=list)
    will_send: bool = True

    def receive(self, source: str, pulse: Pulse):
        self.memory[source] = pulse
        if set(self.memory.values()) == {Pulse.HIGH}:
            self.sending_pulse = Pulse.LOW
        else:
            self.sending_pulse = Pulse.HIGH

    def __hash__(self):
        return hash(
            (
                self.module_type,
                self.sending_pulse,
                tuple(sorted(self.memory.items())),
                tuple(self.destination),
                self.will_send,
            )
        )


@dataclass
class Broadcaster:
    module_type: str = "broadcaster"
    sending_pulse: Pulse = Pulse.LOW
    destination: List[str] = field(default_factory=list)
    will_send: bool = True

    def receive(self, source: str, pulse: Pulse):
        self.sending_pulse = pulse

    def __hash__(self):
        return hash(
            (
                self.module_type,
                self.sending_pulse,
                tuple(self.destination),
                self.will_send,
            )
        )


def send_pulse(pulse_queue, modules, pulse_types):
    module_name = pulse_queue.popleft()
    for dest in modules[module_name].destination:
        modules[dest].receive(
            source=module_name, pulse=modules[module_name].sending_pulse
        )
        if modules[dest].will_send:
            pulse_queue.append(dest)
        pulse_types[modules[module_name].sending_pulse] += 1
    return pulse_queue, modules, pulse_types


def send_magic_pulse(pulse_queue, modules, magic_inputs, presses):
    module_name = pulse_queue.popleft()
    for dest in modules[module_name].destination:
        modules[dest].receive(
            source=module_name, pulse=modules[module_name].sending_pulse
        )
        if modules[dest].will_send:
            pulse_queue.append(dest)
        if (
            dest in magic_inputs
            and modules[dest].sending_pulse == Pulse.HIGH
            and magic_inputs[dest] == 0
        ):
            magic_inputs[dest] = presses
    return pulse_queue, modules, magic_inputs, presses


def run_magic_cycle(modules, magic_inputs, presses):
    presses += 1
    pulse_queue = deque(["broadcaster"])
    while pulse_queue:
        pulse_queue, modules, magic_inputs, presses = send_magic_pulse(
            pulse_queue, modules, magic_inputs, presses
        )
    return modules, magic_inputs, presses


def run_cycle(modules):
    pulse_queue = deque(["broadcaster"])
    pulse_types = {Pulse.LOW: 1, Pulse.HIGH: 0}
    while pulse_queue:
        pulse_queue, modules, pulse_types = send_pulse(
            pulse_queue, modules, pulse_types
        )

    return modules, pulse_types


if __name__ == "__main__":
    fpath = r"path_to_file.txt"
    modules = {}
    for line in open(fpath, "r"):
        l, r = line.strip().split(" -> ")
        outputs = r.split(", ")
        if l == "broadcaster":
            modules["broadcaster"] = Broadcaster(destination=outputs)
        elif l[0] == "%":
            modules[l[1:]] = FlipFlop(destination=outputs)
        else:
            modules[l[1:]] = Conjunction(destination=outputs)

    output_modules = []
    for module in modules.values():
        for dest_module in module.destination:
            if dest_module not in modules:
                output_modules.append(dest_module)
    for module in output_modules:
        modules[module] = OutputModule()

    for source, module in modules.items():
        if module.module_type != "output":
            for dest_module in module.destination:
                if modules[dest_module].module_type == "&":
                    modules[dest_module].memory[source] = Pulse.LOW

    modules_copy = copy.deepcopy(modules)
    l, h = 0, 0
    NUM_PRESSES = 1000
    PULSE_TYPES = {Pulse.LOW: 0, Pulse.HIGH: 0}
    for _ in range(NUM_PRESSES):
        modules, pulse_types = run_cycle(modules)
        PULSE_TYPES[Pulse.LOW] += pulse_types[Pulse.LOW]
        PULSE_TYPES[Pulse.HIGH] += pulse_types[Pulse.HIGH]

    print(f"Part 1 Solution: {PULSE_TYPES[Pulse.HIGH]*PULSE_TYPES[Pulse.LOW]}")

    # This is some magic where I inspected the input and saw that we had
    # &Y_i -> &cl -> rx for i = 1,2,3,4 which implies that
    # we simply need to find an instance when &Y_i are all outputting T
    magic_inputs = {"js": 0, "qs": 0, "dt": 0, "ts": 0}
    presses = 0

    while True:
        modules_copy, magic_inputs, presses = run_magic_cycle(
            modules_copy, magic_inputs, presses
        )
        if math.lcm(*magic_inputs.values()) != 0:
            print(magic_inputs)
            print(f"Part 2 Solution: {math.lcm(*magic_inputs.values())}")
            break
