
def union(list1, list2):
    return list(set(list1 + list2))


def difference(list1, list2):
    return list(set(list1) - set(list2))


def lists_differ(list1, list2):
    return not set(list1) == set(list2)
