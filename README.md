# TA-Tools
Small personal repo meant to house some tools I write to grade student code easier.

# Usage
```
usage: autoGrader.py [-h] [-v] src template tester output

positional arguments:
  src            path to the directory with all students' code
  template       path to template text file for reports; should be a YAML file with each line as '<string name>:<int max score>'
  tester         path to python file to pass individual repo to
  output         path to dir for report outputs and progress record

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  more print statements
```
