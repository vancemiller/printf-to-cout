#!/usr/bin/python3

import unittest
from converter import converter

class TestConvert(unittest.TestCase):

  test_printf_cases = [
      ('"hi"', 'std::cout << "hi";'),
      ('"hi\\n"', 'std::cout << "hi" << std::endl;'),
      ('"\\nh\\ni\\n\\n"',  'std::cout << std::endl << "h" << std::endl << "i" << std::endl << std::endl;'),
      ('"%d %d", a, b', 'std::cout << a << " " << b;'),
      ('"%d%d", a, b', 'std::cout << a << b;'),
      ('"%x", a', 'std::cout << std::hex << a << std::dec;'),
      ]

  test_coalesce_cases = [
      (('printf("hi', [' world!\\n");']), ('"hi world!\\n"', '', '')),
      (('printf("hi', [' world! %d\\n",', 'abc);']), ('"hi world! %d\\n",abc','','')),
      (('printf("%d', [' world! %d\\n', '%d %x %l', '%b\\n",', 'a, b, c,d,', 'e,   f);']),
        ('"%d world! %d\\n%d %x %l%b\\n",a, b, c,d,e,   f','','')),
      (('printf(', [');']), ('', '', ''))
      ]

  def test_printf(self):
    for case in TestConvert.test_printf_cases:
      self.assertEqual(converter._printf_to_cout('std::cout', case[0]), case[1]);

  def test_coalesce(self):
    for case in TestConvert.test_coalesce_cases:
      self.assertEqual(converter._coalesce_printf(case[0][0], case[0][1]), case[1]);


if __name__ == '__main__':
  unittest.main()

