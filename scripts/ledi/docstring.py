import itertools


def parse_docstring(docstring):
    lines = map(lambda x: x.strip(), docstring.split("\n"))
    definitions = list(itertools.dropwhile(lambda x: x, lines))
    summaries = itertools.dropwhile(lambda x: not x, definitions)
    summaries = itertools.takewhile(lambda x: x, summaries)
    summaries = list(summaries)
    summaries = summaries if summaries else list(lines)
    return definitions, summaries

