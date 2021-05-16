from typing import List
import random


def generate_random_number(to: int, exclusive_nums: List[int]) -> int:
    random_number = random.randint(0, to)
    exclusive_nums_has_gen_num = list(
        filter(lambda x: x == random_number, exclusive_nums)
    )
    return (
        generate_random_number(to, exclusive_nums)
        if len(exclusive_nums_has_gen_num) > 0
        else random_number
    )
