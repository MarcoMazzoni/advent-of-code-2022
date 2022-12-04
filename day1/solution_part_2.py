import dataclasses
import typing


@dataclasses.dataclass
class ElfCalories:
    index: int
    calories: int

    def __lt__(self, other: 'ElfCalories'):
        return self.calories <= other.calories


def get_elf_calories(s: str) -> typing.Iterator[ElfCalories]:
    curr_elf_num: int = 0
    prev_new_line_index: int = -1
    curr_calories: int = 0
    for curr_char_index, curr_char in enumerate(s):
        if curr_char == '\n':
            if curr_char_index - prev_new_line_index == 1:
                elf_calories = ElfCalories(curr_elf_num, curr_calories)
                curr_elf_num += 1
                prev_new_line_index = curr_char_index
                curr_calories = 0
                yield elf_calories
            else:
                curr_calories += int(s[(prev_new_line_index + 1):curr_char_index])
                prev_new_line_index = curr_char_index


def get_top_three_elves(s: str) -> typing.List[ElfCalories]:
    sorted_list = sorted(get_elf_calories(s), reverse=True)
    return sorted_list[:3]


if __name__ == '__main__':
    with open("input.txt") as f:
        inp = f.read()
    top_three = get_top_three_elves(inp)
    print(top_three)
    print(sum(map(lambda o: o.calories, top_three)))