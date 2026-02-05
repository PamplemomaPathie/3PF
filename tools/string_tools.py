#!/usr/bin/python3


def compute_difference(first: str, second: str):
    prev_row = []
    for i in range(len(second) + 1):
        prev_row.append(i)

    for i, cfirst in enumerate(first, 1):
        curr_row = [i]
        for j, csecond in enumerate(second, 1):
            insert = curr_row[j - 1] + 1
            delete = prev_row[j] + 1
            replace = prev_row[j - 1]
            if cfirst != csecond:
                replace += 1
            curr_row.append(min(min(insert, delete), replace))
        prev_row = curr_row

    return prev_row[-1]


def compute_similarity(first: str, second: str):
    if first == second:
        return 0
    if len(first) == 0 or len(second) == 0:
        return len(second if len(first) == 0 else first)
    diff = compute_difference(first, second) / max(len(first), len(second))
    return float(1.0 - diff)


def get_similar(name: str, objs, cutoff: float = 0.5):
    name = name.lower()

    result = None
    maximum = 0.0

    for obj in objs:
        score = compute_similarity(name, obj.lower())
        if score > maximum:
            maximum = score
            result = obj

    return result if maximum >= cutoff else None
