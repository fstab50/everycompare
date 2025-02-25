import argparse
import sys

from multiprocessing import Pool

from core import compare

parser = argparse.ArgumentParser()
parser.add_argument('dir_path', help='Directory to analyze')
parser.add_argument('-c', '--count', type=int, default=1, help='How many comparisons to execute in parallel (default 1)')

if __name__ == "__main__":
    params = vars(parser.parse_args(sys.argv[1:]))

    kwargs = {
        'path': params['dir_path'],
        'only_text': True
    }

    if params['count'] > 1:
        p = Pool(params['count'])
        kwargs['mapping_function'] = p.map

    out = sorted(compare(**kwargs))
    [print(x) for x in out]