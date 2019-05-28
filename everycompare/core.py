import itertools
from functools import lru_cache
import os

from binaryornot.check import is_binary
from pylev3 import Levenshtein

from structures import ComparisonResult, FileMeta

@lru_cache()
def read_memoized(path):
    with open(path) as f:
        return f.read()

def get_files(path, only_text=False):
    def __filter(item_path):
        return (True if not only_text else not is_binary(item_path))
    
    def __iterate():
        for root, _, files in os.walk(path):
            for f in files:
                filepath = os.path.join(root, f)
                if not __filter(filepath):
                    continue

                size = os.path.getsize(filepath)
                
                is_bin = is_binary(filepath)
                contents = None if is_bin else read_memoized(filepath)
                
                yield FileMeta(
                    path=filepath,
                    is_binary=is_bin,
                    contents=contents,
                    size=size,
                    text_length=size if is_bin else len(contents)
                )
    
    return list(__iterate())


def compare(path, only_text=False):
    files = get_files(path, only_text)

    for items in itertools.combinations(files, 2):
        left, right = sorted(items)
        paths = [os.path.relpath(x.path, path) for x in (left, right)]

        smallest_size = min(left.size, right.size)
        largest_size = max(left.size, right.size)
        size_ratio = smallest_size*100 / largest_size

        if all(x == 0 for x in (smallest_size, largest_size)):
            yield ComparisonResult(difference=0, paths=paths, method='BOTH_EMPTY')

        elif smallest_size == 0 or largest_size / smallest_size >= 2:
            yield ComparisonResult(difference=100, paths=paths, method='SIZE_DIFFERENCE')

        
        elif not any(x.is_binary for x in (left, right)):
            max_len = max(left.text_length, right.text_length)
            yield ComparisonResult(
                difference=Levenshtein.wfi(left.contents, right.contents) * 100 / max_len,
                paths=paths,
                method='STRING_COMPARISON'
            )

        else:
            yield ComparisonResult(
                difference=size_ratio,
                paths=paths,
                method='BINARY_SIZES'
            )
