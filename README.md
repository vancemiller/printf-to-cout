= Printf to cout =

This simple python script converts printf statements to cout statements.

It ignores format specifiers (except for %x). If you want to add that functionality please submit a pull request.

== Use ==

python3 converter.py <path/to/file>

Converted output is printed to standard out
Please check the result for correctness. If you find a scenario where the script fails, please add it to the test cases and submit a pull request.

== Testing ==
python3 tester.py
