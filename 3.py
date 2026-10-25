import os
import functools
from datetime import datetime


def logger(path):
    def __logger(old_function):
        @functools.wraps(old_function)
        def new_function(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            try:
                result = old_function(*args, **kwargs)
            except StopIteration:
                with open(path, 'a', encoding='utf-8') as log_file:
                    log_file.write(
                        f"{datetime.now()} | "
                        f"function: {old_function.__name__} | "
                        f"args: ({signature}) | "
                        f"returned: StopIteration\n"
                    )
                raise
            except Exception as exc:
                with open(path, 'a', encoding='utf-8') as log_file:
                    log_file.write(
                        f"{datetime.now()} | "
                        f"function: {old_function.__name__} | "
                        f"args: ({signature}) | "
                        f"raised: {type(exc).__name__}: {exc}\n"
                    )
                raise

            with open(path, 'a', encoding='utf-8') as log_file:
                log_file.write(
                    f"{datetime.now()} | "
                    f"function: {old_function.__name__} | "
                    f"args: ({signature}) | "
                    f"returned: {result!r}\n"
                )
            return result

        return new_function

    return __logger



class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.outer_index = 0
        self.inner_index = 0

    def __iter__(self):
        return self

    @logger('iterator.log')
    def __next__(self):
        while self.outer_index < len(self.list_of_list):
            inner_list = self.list_of_list[self.outer_index]
            if self.inner_index < len(inner_list):
                item = inner_list[self.inner_index]
                self.inner_index += 1
                return item
            self.outer_index += 1
            self.inner_index = 0
        raise StopIteration



def test_iterator():
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    expected = ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    for flat_iterator_item, check_item in zip(FlatIterator(list_of_lists_1), expected):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == expected
    print('test_iterator: OK')


if __name__ == '__main__':
    for log in ('iterator.log',):
        if os.path.exists(log):
            os.remove(log)

    test_iterator()

    print('\n--- iterator.log ---')
    with open('iterator.log') as f:
        print(f.read())
