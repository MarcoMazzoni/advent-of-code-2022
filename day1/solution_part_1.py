import dataclasses
import typing


@dataclasses.dataclass
class BestElfCalories:
    index: int
    calories: int


def get_best_elf(s: str) -> BestElfCalories:
    curr_elf_num = 0
    prev_new_line_index = -1
    curr_calories = 0
    best_elf_calories = BestElfCalories(0, 0)
    for curr_char_index, curr_char in enumerate(s):
        if curr_char == '\n':
            if curr_char_index - prev_new_line_index == 1:
                if curr_calories > best_elf_calories.calories:
                    best_elf_calories.index = curr_elf_num
                    best_elf_calories.calories = curr_calories
                curr_elf_num += 1
                prev_new_line_index = curr_char_index
                curr_calories = 0
                continue
            curr_calories += int(s[(prev_new_line_index + 1):curr_char_index])
            prev_new_line_index = curr_char_index

    return best_elf_calories


if __name__ == '__main__':
    with open("input.txt") as f:
        inp = f.read()
    best = get_best_elf(inp)
    print(best)
