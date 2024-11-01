def split_by_none(array):
    if not None in array:
        return [array]
    index_first_none = array.index(None)
    return [array[:index_first_none]] + split_by_none(array[index_first_none+1:])


def split_by_none_iteratively(array):
    ans = []
    curr = []
    for val in array:
        if val is None:
            ans.append(curr)
            curr = []
        else:
            curr.append(val)
    ans.append(curr)
    return ans

L = [1, 2, None, 3, None, 0, None, None, 4, None]
print(split_by_none(L))
print(split_by_none_iteratively(L))
