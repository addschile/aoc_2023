from __future__ import annotations

import argparse
import re
import sys


def get_digit_numbers(fname: str) -> list[int]:
    numbers = []
    with open(fname) as f:
        for line in f.readlines():
            digits = list(filter(lambda x: x.isdigit(), line))
            if digits:
                numbers.append(int(digits[0] + digits[-1]))
    return numbers


NUM_STRINGS = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine"
]


def get_split_line(line: str) -> list[str]:
    """
    Split a string by whether a character is a digit, but keep the digit
    included in the split list
    """
    splits = []
    old_idx = 0
    idx = 0
    while idx < len(line):
        for char in line[old_idx:]:
            if char.isdigit():
                break
            idx += 1
        splits.append(line[old_idx:idx])
        if idx < len(line):
            splits.append(line[idx])
            idx += 1
        old_idx = idx
    return splits


def get_numbers_from_split(split: str) -> list[int]:
    """
    Given a split string, return the numbers that are in the string
    """
    matches = []
    for num in NUM_STRINGS:
        matches.extend(list(re.finditer(num, split)))
    matches = sorted(filter(None, matches), key=lambda match: match.span()[0])
    numbers = []
    for match in matches:
        numbers.append(match.group())
    return numbers


NUM_TO_DIGIT = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}


def get_number(num: str | int) -> str:
    if num.isdigit():
        return num
    else:
        return NUM_TO_DIGIT[num]


def get_number_from_line(line: str) -> int:
    line_numbers = []
    for split in get_split_line(line.strip()):
        if split.isdigit():
            line_numbers.append(split)
        else:
            line_numbers.extend(get_numbers_from_split(split))
    return int(get_number(line_numbers[0]) + get_number(line_numbers[-1]))


def get_numbers(fname: str):
    with open(fname) as f:
        return [get_number_from_line(line.strip()) for line in f.readlines()]


def main(args):

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("input", type=str)
    opt = parser.parse_args(args)

    digit_numbers = get_digit_numbers(opt.input)
    print(f"numbers using only digits: {sum(digit_numbers)}")

    numbers = get_numbers(opt.input)
    print(f"numbers using both: {sum(numbers)}")


if __name__ == '__main__':
    main(sys.argv[1:])
