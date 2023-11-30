from typing import List, TypeVar, Callable

from django.db.models import QuerySet


T = TypeVar("T")

def group(models: QuerySet[T], split: int):
    size = len(models)
    groups = [[] for _ in range((size + split + 1) // split)]

    for index, item in enumerate(models):
        groups[index % len(groups)].append(item)
    
    return groups


def find_group(groups: List[T], element: T, predicate: Callable[[T, T], bool]):
    for group in groups:
        last_item = group[-1]

        if predicate(last_item, element):
            return group
        else:
            continue


# l = [1,2,3,4,5,6,7,8,9,10,11,12,13]
# a = group(l, 5)
# print(find_group(a, 2, lambda b, o: ))