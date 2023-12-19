import time
from dataclasses import dataclass, field
from typing import Callable, TypedDict

day = 19


@dataclass
class Rule:
    label: str
    op: Callable[[int, int], bool]
    op_sym: str
    value: int
    target: str
    default: bool

    @property
    def final(self):
        return self.target in ("A", "R")

    def match(self, part: dict[str, int]):
        if self.default:
            return True
        return self.op(part[self.label], self.value)


@dataclass
class State:
    label: str
    rules: list[Rule] = field(default_factory=list)

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def apply_rules(self, part: dict[str, int]):
        rule = self.rules[0]
        for rule in self.rules:
            if rule.match(part):
                break
        return rule


class Data(TypedDict):
    parts: list[dict[str, int]]
    states: dict[str, State]


def part_1(data: Data):
    states = data["states"]
    parts = data["parts"]
    accepted: list[dict[str, int]] = []
    for part in parts:
        state = states["in"]
        while not (results := state.apply_rules(part)).final:
            state = states[results.target]
        if results.target == "A":
            accepted.append(part)
    return sum([sum(x.values()) for x in accepted])


def get_new_range(part, rule):
    if rule.op_sym == "<":
        if part[rule.label][0] >= rule.value:  # Part outside of rule
            return None
        else:
            return part | {
                rule.label: [
                    part[rule.label][0],
                    min(rule.value - 1, part[rule.label][1]),
                ]
            }
    else:  # rule.op_sum == '>'
        if part[rule.label][1] <= rule.value:  # Part outside of rule
            return None
        else:
            return part | {
                rule.label: [
                    max(rule.value + 1, part[rule.label][0]),
                    part[rule.label][1],
                ]
            }


def get_new_neg_range(part, rule):
    if rule.op_sym == "<":
        if part[rule.label][1] < rule.value:  # Part inside of rule
            return None
        else:
            return part | {
                rule.label: [max(rule.value, part[rule.label][0]), part[rule.label][1]]
            }
    else:  # rule.op_sum == '>'
        if part[rule.label][0] > rule.value:  # Part inside of rule
            return None
        else:
            return part | {
                rule.label: [part[rule.label][0], min(rule.value, part[rule.label][1])]
            }


def get_new_parts(parts: list[dict[str, list[int]]], state: State, label: str):
    new_parts: list[dict[str, list[int]]] = []
    target_rules = filter(lambda rule: rule.target == label, state.rules)
    for rule in target_rules:
        for part in parts:
            new_part = part
            for other_rule in state.rules:
                if rule == other_rule:
                    if not rule.default:
                        new_part = get_new_range(new_part, rule)
                    break
                else:
                    new_part = get_new_neg_range(new_part, other_rule)
                    if not new_part:
                        break
            if new_part:
                new_parts.append(new_part)
    return new_parts


def part_2_recurse(
    state: State, parts: list[dict[str, list[int]]], states: dict[str, State]
):
    if state.label == "in":
        return parts
    parent_states = filter(
        lambda t_state: any(
            map(lambda rule: rule.target == state.label, t_state.rules)
        ),
        states.values(),
    )
    res_parts: list[dict[str, list[int]]] = []
    for parent_state in parent_states:
        new_parts = get_new_parts(parts, parent_state, state.label)
        res_parts += part_2_recurse(parent_state, new_parts, states)
    return res_parts


def part_2(data: Data):
    states = data["states"]
    accepted_states = filter(
        lambda state: any(map(lambda rule: rule.target == "A", state.rules)),
        states.values(),
    )
    part_ranges: list[dict[str, list[int]]] = []
    for state in accepted_states:
        parts = [{"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}]
        new_parts = get_new_parts(parts, state, "A")
        part_ranges += part_2_recurse(state, new_parts, states)
    s = 0
    for part_range in part_ranges:
        v = 1
        for item in part_range.values():
            v *= item[1] - item[0] + 1
        s += v
    return s


def parse_data() -> Data:
    data: Data = {"states": {}, "parts": []}
    states = True
    with open(f"day{day}.txt", "r") as f:
        for line in f:
            if not line.strip():
                states = False
                continue
            if states:
                label, rule_s = line.strip().split("{")
                rules = rule_s[:-1].split(",")
                state = State(label)
                for rule_s in rules[:-1]:
                    rule_s, target = rule_s.split(":")
                    r_label, op_s, *value = rule_s
                    value = int("".join(value))
                    if op_s == "<":
                        op: Callable[[int, int], bool] = lambda part, val: part < val
                    else:
                        op: Callable[[int, int], bool] = lambda part, val: part > val
                    rule = Rule(r_label, op, op_s, value, target, False)
                    state.add_rule(rule)
                state.add_rule(Rule("", lambda x, y: True, "", -1, rules[-1], True))
                data["states"][label] = state
            else:
                part = {}
                parts = line.strip()[1:-1].split(",")
                for part_s in parts:
                    label, value = part_s.split("=")
                    part[label] = int(value)
                data["parts"].append(part)
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
