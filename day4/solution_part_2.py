from __future__ import annotations
import dataclasses
import time
import typing


@dataclasses.dataclass
class Range:
    lower: int
    upper: int

    @classmethod
    def from_string(cls, o: str) -> Range:
        lower, upper = o.split('-')
        return Range(lower=int(lower), upper=int(upper))

    def fully_contains_other_range(self, other_range: Range) -> bool:
        if self.lower <= other_range.lower and self.upper >= other_range.upper:
            return True

    def overlaps_with_other_range(self, other_range: Range) -> bool:
        if other_range.lower <= self.lower <= other_range.upper or other_range.lower <= self.upper <= other_range.upper:
            return True


def does_one_range_fully_contain_the_other(range_pair: str) -> bool:
    range_1, range_2 = tuple(map(lambda x: Range.from_string(x), range_pair.split(',')))
    if range_1.overlaps_with_other_range(range_2) or range_2.overlaps_with_other_range(range_1):
        return True
    return False


def get_overlaps(list_of_pairs: typing.List[str]) -> int:
    return sum(1 for _ in filter(does_one_range_fully_contain_the_other, list_of_pairs))


if __name__ == '__main__':
    with open("input.txt") as f:
        inp = f.read()
    start = time.time_ns()
    score = get_overlaps(inp.splitlines())
    print(f'Overlaps computation took: {(time.time_ns() - start) // 1_000_000} ms')
    print('Result:', score)