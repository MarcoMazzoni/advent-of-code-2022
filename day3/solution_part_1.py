from __future__ import annotations
import dataclasses
import time


@dataclasses.dataclass
class Item:
    _item: str

    @classmethod
    def from_string(cls, o: str) -> Item:
        half = len(o) // 2
        item = set(o[:half]).intersection(set(o[half:]))
        return Item(_item=item.pop())

    def get_priority(self) -> int:
        res = self._get_priority_of_lower_case() if self._item.islower() else self._get_priority_of_upper_case()
        print(self._item, res)
        return res

    def _get_priority_of_lower_case(self) -> int:
        return ord(self._item) - 96

    def _get_priority_of_upper_case(self) -> int:
        return ord(self._item) - 38


def get_score(s: str) -> int:
    res = 0
    prev_new_line_index = -1
    for i, curr_char in enumerate(s):
        if curr_char == '\n':
            res += Item.from_string(s[(prev_new_line_index + 1):i]).get_priority()
            prev_new_line_index = i

    return res


if __name__ == '__main__':
    with open("input.txt") as f:
        inp = f.read()

    # inp = 'vJrwpWtwJgWrhcsFMMfFFhFp\njqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\nPmmdzqPrVvPwwTWBwg\nwMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\nttgJtRGJQctTZtZT\nCrZsJsPPZsGzwwsLwLmpwMDw\n'
    start = time.time_ns()
    score = get_score(inp)
    print(f'Score computation took: {(time.time_ns() - start) // 1_000_000} ms')
    print('Result:', score)
