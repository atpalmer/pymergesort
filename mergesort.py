'''
An "Pythonic" object-oriented merge-sorter
'''


class MergeIterator(object):
    def __init__(self, items):
        self._items = items
        self._index = 0

    def __bool__(self):
        return self._index < len(self._items)

    @property
    def current(self):
        try:
            return self._items[self._index]
        except IndexError:
            raise StopIteration

    def next(self):
        result = self.current
        self._index += 1
        return result

    def compare(self, other):
        return self and ((not other) or self.current < other.current)

    def yield_merged(self, other):
        while True:
            obj = self if self.compare(other) else other
            yield obj.next()

    @classmethod
    def merge(cls, left, right):
        iterl, iterr = cls(left), cls(right)
        return list(cls.yield_merged(iterl, iterr))


class MergeSorter(object):
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return len(self) > 1

    @property
    def midpoint(self):
        return len(self) // 2

    @property
    def left(self):
        return self._items[0: self.midpoint]

    @property
    def right(self):
        return self._items[self.midpoint: len(self)]

    def result(self):
        if not self:
            return self.items
        return MergeIterator.merge(
            self.sort(self.left),
            self.sort(self.right))

    @classmethod
    def sort(cls, items):
        sorter = cls(items)
        return sorter.result()


def main():
    result = MergeSorter.sort([2, 3, 1])
    print(result)
    assert result == [1, 2, 3]

    result = MergeSorter.sort([9, 2, 7, 4, 0, 5, 1, 3, 6, 8])
    print(result)
    assert result == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


if __name__ == '__main__':
    main()

