import dataclasses
import typing

CrateStacks = typing.NewType('CrateStacks', typing.Dict[int, typing.List[str]])

@dataclasses.dataclass
class MoveCommand:
    _quantity: int
    _from: int
    _to: int

    @classmethod
    def from_string(cls, o: str) -> 'MoveCommand':
        replaced = o.replace(' ', '\n').splitlines()
        print(o)
        return MoveCommand(
            _quantity=int(replaced[1]),
            _from=int(replaced[3]),
            _to=int(replaced[5])
        )

    def move(self, d: CrateStacks):
        for _ in range(self._quantity):
            element_to_move = d[self._from].pop()
            d[self._to].append(element_to_move)


def move_crates(commands: typing.List[str], stacks: CrateStacks) -> CrateStacks:
    commands = map(MoveCommand.from_string, commands)
    for c in commands:
        c.move(stacks)

    print(stacks)
    return stacks


def build_crate_stacks(stack_lines: typing.List[str]) -> CrateStacks:
    d: typing.Dict[int, typing.List[str]] = dict()
    for i in map(int, stack_lines[0].replace(' ', '')):
        d.setdefault(i, list())

    print(d)
    for line in stack_lines[1:]:
        print(line)
        key = 1
        for i in range(0, len(line), 4):
            char = line[i]
            if char != '[':
                key += 1
                continue
            d[key].append(line[i + 1])
            key += 1

    return CrateStacks(d)


def solution(lines: typing.List[str]) -> str:
    move_commands_index = 0
    stacks = dict()
    for i, s in enumerate(lines):
        if s == '':
            stacks = build_crate_stacks(lines[i-1::-1])
            move_commands_index = i

    final_crates = move_crates(lines[move_commands_index+1:], stacks)
    return ''.join(map(lambda o: o.pop(), final_crates.values()))



if __name__ == '__main__':
    with open("input.txt") as f:
        inp = f.read()
    l = inp.splitlines()
    sol = solution(l)
    print(sol)