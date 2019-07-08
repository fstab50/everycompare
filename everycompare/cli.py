import argparse
import re
import sys
from multiprocessing import Pool
from libtools import export_json_object

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(result, *args, **kwargs):
        return sorted(result)

from everycompare.core import compare
from everycompare.formatters import available_formatters

parser = argparse.ArgumentParser()
parser.add_argument('dir_path', help='Directory to analyze')
parser.add_argument('-c', '--count', type=int, default=1, help='How many comparisons to execute in parallel (default 1)')
parser.add_argument('-f', '--format', choices=sorted(available_formatters), default='raw', help='Output format')
parser.add_argument('-e', '--exclude', help='Regular expression indicating which files/folders to exclude from comparison')


def main(args=None):
    args = args or sys.argv[1:]
    params = vars(parser.parse_args(args))

    kwargs = {
        'path': params['dir_path'],
        'only_text': True
    }
    if params.get('exclude'):
        kwargs['exclusion_pattern'] = re.compile(params['exclude'])

    formatter = available_formatters[params['format']]

    with Pool(params['count']) as p:
        kwargs['mapping_function'] = p.imap_unordered

        result, count = compare(**kwargs)
        processed = [i for i in tqdm(result, total=count)]

    out = formatter(processed)
    export_json_object(out)

if __name__ == "__main__":
    main()
