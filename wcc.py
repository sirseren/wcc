#!/usr/bin/env python

import click
import sys

from collections import OrderedDict

def utf8len(s):
   return len(s.encode('utf-8'))


def get_metrics(metric, input):

    if type(input) is not str:
    #if stdin is empty
        if sys.stdin.isatty():
            return {}
        input_file = input
    else:
        input_file = open(input)

    temp_dict = {"a_lines": 0, "b_words": 0, "c_chars": 0, "d_bytes": 0}
    metric_cnt = OrderedDict(sorted(temp_dict.items()))

    for line in input_file:
        if any("lines" in s for s in metric):
            metric_cnt["a_lines"] += 1

        if any("words" in s for s in metric):
            metric_cnt["b_words"] += len(line.split())

        if any("count" in s for s in metric):
            metric_cnt["c_chars"] += len(line)

        if any("bytes" in s for s in metric):
            metric_cnt["d_bytes"] += utf8len(line)

    return metric_cnt


@click.command()
@click.argument('input_file', required=False)
@click.option('-c', '--bytes', 'metric', multiple=True, flag_value='bytes', help='print the byte counts')
@click.option('-m', '--count', 'metric', multiple=True, flag_value='count', help='print the character counts')
@click.option('-l', '--lines', 'metric', multiple=True, flag_value='lines', help='print the newline counts')
@click.option('-w', '--words', 'metric', multiple=True, flag_value='words', help='print the word counts')
def main(metric, input_file):
    #print(metric)
    metric_ordered_list = ("lines", "words", "chars" "bytes")
    if not metric:
        metric = metric_ordered_list

    if input_file is None:
        input_file = sys.stdin

    metric_values = get_metrics(metric, input_file)
    output_result = ''

    if type(input_file) is str:
        str_input_file = str(input_file)
        tab1 = ' '    #tabs and indents
        tab2 = ' '   # to match the output format of the original utility
    else:
        str_input_file = ''
        tab1 = tab2 = '      '

    for k, v in metric_values.items():
        if str(v) != str(0):
            output_result = tab1 + output_result.strip() + tab2 + str(v)

    print(output_result, str_input_file)


if __name__ == "__main__":
    main()