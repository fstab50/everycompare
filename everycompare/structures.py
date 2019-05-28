from collections import namedtuple

ComparisonResult = namedtuple('ComparisonResult', ('difference', 'paths', 'method'))
FileMeta = namedtuple('FileMeta', ('path', 'is_binary', 'contents', 'size', 'text_length'))