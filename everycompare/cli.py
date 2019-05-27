import argparse
import sys

from core import compare

parser = argparse.ArgumentParser()
parser.add_argument('dir_path', help='Directory to analyze')

if __name__ == "__main__":
    params = vars(parser.parse_args(sys.argv[1:]))
    
    out = sorted(compare(params['dir_path'], True))
    [print(x) for x in out]