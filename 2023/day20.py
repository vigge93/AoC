import time
from typing import TypedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import defaultdict
from copy import deepcopy
import math

day = 20


class DataDict(TypedDict):
    pass
type Data = dict[str, "Module"] # DataDict


class State(Enum):
    LOW = auto(),
    HIGH = auto()


class ModuleType(Enum):
    BROADCASTER = auto(),
    FLIP_FLOP = auto(),
    CONJUNCTION = auto(),
    OUTPUT = auto()

module_type_map = {
    '%': ModuleType.FLIP_FLOP,
    '&': ModuleType.CONJUNCTION,
    'broadcaster': ModuleType.BROADCASTER
}


flip_state = {
    State.LOW: State.HIGH,
    State.HIGH: State.LOW    
}


@dataclass
class Module():
    name: str
    state: State
    type: ModuleType
    connection_strings: list[str]
    connections: list["Module"] = field(default_factory=list)
    incomming_connections: dict[str, State] = field(default_factory=dict)
    low_pulses_recieved: int = 0
    high_pulses_recieved: int = 0


    def add_connection(self, conn: "Module"):
        self.connections.append(conn)
        if conn.type == ModuleType.CONJUNCTION:
            conn.incomming_connections[self.name] = State.LOW

    def get_state(self, visited: set[str]) -> tuple[tuple[State | tuple[State,...] | None, ...], set[str]]:
        state: list[State | tuple[State,...] | None] = []
        visited.add(self.name)
        if self.type == ModuleType.BROADCASTER:
            state.append(None)
        elif self.type == ModuleType.FLIP_FLOP:
            state.append(self.state)
        elif self.type == ModuleType.CONJUNCTION:
            state.append(tuple(self.incomming_connections.values()))
        else:
            state.append(None)
        for mod in self.connections:
            if mod.name not in visited:
                n_state, visited = mod.get_state(visited)
                state += n_state
        return tuple(state), visited

    def send_signal(self, signal: State, sent_from: "Module") -> tuple[tuple["Module", State, "Module"], ...]:
        if signal == State.LOW:
            self.low_pulses_recieved += 1
        else:
            self.high_pulses_recieved += 1

        if self.type == ModuleType.BROADCASTER:
            self.state = signal

        elif self.type == ModuleType.FLIP_FLOP:
            if signal == State.HIGH:
                return tuple()
            self.state = flip_state[self.state]

        elif self.type == ModuleType.CONJUNCTION:
            self.incomming_connections[sent_from.name] = signal
            if any(map(lambda state: state == state.LOW, self.incomming_connections.values())):
                self.state = State.HIGH
            else:
                self.state = State.LOW

        return tuple([(module, self.state, self) for module in self.connections])
        
def part_1(data: Data):
    data = deepcopy(data)
    broadcaster = data['broadcaster']
    orig_state, _ = broadcaster.get_state(set())
    state = orig_state
    steps = 0
    while (state != orig_state or steps == 0) and steps < 1000:
        signal_queue: list[tuple[Module, State, Module]] = [(broadcaster, State.LOW, broadcaster)]
        while signal_queue:
            module, signal, parent = signal_queue.pop(0)
            signal_queue += module.send_signal(signal, parent)
        state, _ = broadcaster.get_state(set())
        steps += 1
    m = 1000//steps
    return m*m*sum([module.low_pulses_recieved for module in data.values()])*sum([module.high_pulses_recieved for module in data.values()])

def part_2(data: Data):
    broadcaster = data['broadcaster']
    steps = 0
    cycles = {}
    for cycle_start in broadcaster.connections:
        steps = 0
        cycle_found = False
        while not cycle_found:
            signal_queue: list[tuple[Module, State, Module]] = [(cycle_start, State.LOW, broadcaster)]
            while signal_queue:
                module, signal, parent = signal_queue.pop(0)
                signal_queue += module.send_signal(signal, parent)
                if (name := module.name) in ('qk', 'kf', 'kr', 'zs'):
                    if module.state == State.HIGH:
                        if name in cycles:
                            if not 'end' in cycles[name]:
                                cycles[name]['end'] = steps
                                cycle_found = True
                        else:
                            cycles[name] = {'start': steps}
            steps += 1
    cycle_lens = []
    for cycle in cycles.values():
        cycle_lens.append(cycle['end'] - cycle['start'])
    return math.lcm(*cycle_lens)


def parse_data():
    data: Data = {}
    with open(f"day{day}.txt", "r") as f:
        for line in f:
            module, connections = line.strip().split(' -> ')
            if module != 'broadcaster':
                module_type, name = module[0], module[1:]
            else:
                module_type, name = module, module
            connections = connections.split(', ')
            module = Module(name, State.LOW, module_type_map[module_type], connections)
            data[name]= module
    mod = None
    for module in data.values():
        for conn in module.connection_strings:
            if conn not in data:
                mod = Module(conn, State.LOW, ModuleType.OUTPUT, [])
                module.add_connection(mod)
                continue
            module.add_connection(data[conn])
    if mod:
        data[mod.name] = mod
    return data


if __name__ == "__main__":
    start_time = time.perf_counter_ns()
    data = parse_data()
    data_time = time.perf_counter_ns()
    p1 = part_1(data)
    p1_time = time.perf_counter_ns()
    p2 = part_2(data)
    end_time = time.perf_counter_ns()
    print(
        f"""=== Day {day:02} ===\n"""
        f"""  · Loading data\n"""
        f"""  · Elapsed: {(data_time - start_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 1: {p1}\n"""
        f"""  · Elapsed: {(p1_time - data_time)/10**6:.3f} ms\n\n"""
        f"""  · Part 2: {p2}\n"""
        f"""  · Elapsed: {(end_time - p1_time)/10**6:.3f} ms\n\n"""
        f"""  · Total elapsed: {(end_time - start_time)/10**6:.3f} ms"""
    )
