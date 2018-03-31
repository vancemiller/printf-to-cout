#!/usr/bin/python

import re
import sys

class converter:

  # Line contains printf, return a string containing the entire printf without newlines
  # Will read additional lines from f until reaching the end of the printf statement
  @staticmethod
  def _coalesce_printf(line, f):
    match = re.match(r'(.*)printf\((.*?)\);(.*)', line);
    if match is None:
      match = re.match(r'(.*)printf\((.*)', line);
      assert(match is not None)
      before = match.group(1)
      print_statement = match.group(2)
      for line in f:
        match = re.match(r'(.*?)\);(.*)', line)
        if match is None:
          match = re.match(r'(.*)', line)
          assert(match is not None)
          print_statement += match.group(1)
        else:
          print_statement += match.group(1)
          after = match.group(2)
          break
    else:
      before = match.group(1)
      print_statement = match.group(2)
      after = match.group(3)

    return (print_statement, before, after)

  @staticmethod
  def _process_printf(line, f, prefix):
    (printf, before, after) = converter._coalesce_printf(line, f)
    return before + converter._printf_to_cout(prefix, printf) + after

  @staticmethod
  def _process_fprintf(line, f):
    if 'stdout' in line:
      line = re.sub(r'fprintf\((\s*)stdout(\s*),\s*', 'printf(', line)
      prefix = 'std::cout'
    elif 'stderr' in line:
      line = re.sub(r'fprintf\((\s*)stderr(\s*),\s*', 'printf(', line)
      prefix = 'std::cerr'
    else:
      prefix = re.search(r'fprintf\((.*?),', line).group(1)
      line = re.sub(r'fprintf\(' + prefix + ',', 'printf(', line)
    return converter._process_printf(line, f, prefix)

  format_string = re.compile(r'(%\d*\.?\d*[hlLzjt]*[diufFeEgGxXoscpaAn])')
  @staticmethod
  def _printf_to_cout(prefix, line):
    result = prefix
    split = line.strip().split('",')
    string = split[0][1:] # remove first quotation mark with [1:]
    if len(split) > 1:
      args = split[1].split(',')
    else:
      args = []
      string = string[:-1] # remove last quotation mark
    split = converter.format_string.split(string)
    n_args = len(re.findall(converter.format_string, string))
    if n_args != len(args):
      print("\n\nERROR: mismatched arguments for line: " + line)
      print("Expected " + str(n_args) + " but provided " + str(len(args)))
      print(args)
      assert(False)
    current_arg = 0
    for string in split:
      if re.match(converter.format_string, string):
        if 'x' in string:
          result += ' << std::hex'
        result += " << " + args[current_arg].strip()
        if 'x' in string:
          result += ' << std::dec'
        current_arg += 1
      else:
        result += ' << "' + string + '"'
    result += ';'
    result = re.sub(r'\\n', '" << std::endl << "', result)
    result = re.sub(r' << ""', '', result)
    return result

  @staticmethod
  def _process_line(line, f):
    if re.search(r'(\s|^)fprintf\(', line):
      return converter._process_fprintf(line, f)
    elif re.search(r'(\s|^)printf\(', line):
      return converter._process_printf(line, f, 'std::cout')
    else:
      return line

  @staticmethod
  def process_file(f):
    output = ''
    for line in f:
      output += converter._process_line(line, f)
    return output


if __name__ == '__main__':
  with open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin as f:
    print(converter.process_file(f), end='')

