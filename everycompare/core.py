import itertools
from functools import lru_cache
import os

from binaryornot.check import is_binary
from pylev3 import Levenshtein

from structures import ComparisonResult

def get_filelist(path, only_text=False):
    def __filter(item_path):
        return (True if not only_text else not is_binary(item_path))
    
    return list(
        itertools.chain(*[
            [os.path.join(root, f) for f in files if __filter(os.path.join(root, f))]
            for root, _, files in os.walk(path)
        ])
    )

@lru_cache()
def read_memoized(path):
    with open(path) as f:
        return f.read()

def compare(path, only_text=False):
    paths = get_filelist(path, only_text)

    for cmp_paths in itertools.combinations(paths, 2):
        cmp_paths = sorted(cmp_paths)
        left, right = cmp_paths
        smallest_size = min(os.path.getsize(left), os.path.getsize(right))
        largest_size = max(os.path.getsize(left), os.path.getsize(right))

        if all(x == 0 for x in (smallest_size, largest_size)):
            yield ComparisonResult(difference=0, paths=cmp_paths)
        elif smallest_size == 0 or largest_size / smallest_size >= 2:
            yield ComparisonResult(difference=100, paths=cmp_paths)

        elif not any(is_binary(x) for x in (left, right)):
            left_contents = read_memoized(left)
            right_contents = read_memoized(right)

            max_len = max(len(left_contents), len(right_contents))
            yield ComparisonResult(
                difference=Levenshtein.wfi(left_contents, right_contents) * 100 / max_len,
                paths=cmp_paths
            )

        else:
            yield ComparisonResult(size_cmp, cmp_paths)
