# Programs

![Commit](https://github.com/adityaa30/programs/workflows/Check%20Commit/badge.svg)
![Test](https://github.com/adityaa30/programs/workflows/Test/badge.svg)

## Competitive Programming CLI

```bash
./cli.py --help
```

```text
usage: cli.py [-h] [-t TEMPLATE] [-p PATH] -c CONTEST {download,run,show} ...

Competitive Programming Helper

positional arguments:
  {download,run,show}

optional arguments:
  -h, --help            show this help message and exit
  -t TEMPLATE, --template TEMPLATE
                        Competitive programming template file
  -p PATH, --path PATH  Path of the dir where all input/output files are saved
  -c CONTEST, --contest CONTEST
                        Uri format should be: <platform-prefix>::<contest-name> 
                        Contest Prefixes Supported: {'cc': 'Codechef', 'cf': 'Codeforces'}
                        Eg: 
                        Codeforces: cf::1382 
                        Codechef: cc::JUNE20A (Coming Soon)
```


For example to download **Codeforces Round #661 (Div. 3)** sample test cases, create a URI using the contest id. 
For the above contest - Link is **https://codeforces.com/contest/1399/**
Contest ID is 1399 -> URI would become `cf::1399`

### `download`

```bash
./cli.py -c cf::1339 download
```

```text
Found: Codeforces Round #633 (Div. 2) ✅
Scraping problems:
[#]  A. Filling Diamonds -- 1 Samples
[#]  B. Sorted Adjacent Differences -- 1 Samples
[#]  C. Powered Addition -- 1 Samples
[#]  D. Edge Weight Assignment -- 3 Samples
[#]  E. Perfect Triples -- 1 Samples
Saved in ./ContestFiles/Codeforces-1339
```

All the problems will be saved in a tree like structure as below::

```text
ContestFiles/
└── Codeforces-1339
    ├── A-Filling-Diamonds
    │   ├── Input
    │   │   └── 0.txt
    │   ├── Output
    │   │   └── 0.txt
    │   └── Solve.cpp
    ├── B-Sorted-Adjacent-Differences
    │   ├── Input
    │   │   └── 0.txt
    │   ├── Output
    │   │   └── 0.txt
    │   └── Solve.cpp
    ├── C-Powered-Addition
    │   ├── Input
    │   │   └── 0.txt
    │   ├── Output
    │   │   └── 0.txt
    │   └── Solve.cpp
    ├── D-Edge-Weight-Assignment
    │   ├── Input
    │   │   ├── 0.txt
    │   │   ├── 1.txt
    │   │   └── 2.txt
    │   ├── Output
    │   │   ├── 0.txt
    │   │   ├── 1.txt
    │   │   └── 2.txt
    │   └── Solve.cpp
    └── E-Perfect-Triples
        ├── Input
        │   └── 0.txt
        ├── Output
        │   └── 0.txt
        └── Solve.cpp
```

Here, `Solve.cpp` is a Template file (default copied from `./Template.cpp`). To specify a custom template use `-t` or `--template` flag

```bash
./cli.py -t <path-to-template> -c cf::1339 download
```

### `run`

```bash
./cli.py -c cf::1339 run -h
```

```text
usage: cli.py run [-h] [-s SOLUTION_FILE] question

positional arguments:
  question              Path to the C++ program file or Question Name or 1 based index

optional arguments:
  -h, --help            show this help message and exit
  -s SOLUTION_FILE, --solution-file SOLUTION_FILE
                        Path of the program file (different from default file)
```

By default, `run` will take the default `Solve.cpp` file inside the question directory. To specify another solution file, use the `-s` flag.

Example:

```bash
./cli.PY -c cf::1339 run 3
# OR
./cli.PY -c cf::1339 run powered
# OR
./cli.PY -c cf::1339 run add
```

```text
[#] Checking question: C-Powered-Addition
[#] Sample Test Case 1: ✅
```

### `show`

```bash
./cli.py -c cf::1339 show -h
```

```text
usage: cli.py show [-h] [-v] [-q QUESTION]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         If True show all test cases (default=False)
  -q QUESTION, --question QUESTION
                        Shows only test cases of the provided question
```

Example:

```bash
./cli.py -c cf::1339 show
```

```text
Question 1: A-Filling-Diamonds
Question 2: B-Sorted-Adjacent-Differences
Question 3: C-Powered-Addition
Question 4: D-Edge-Weight-Assignment
Question 5: E-Perfect-Triples
```

### Download Guide

Only two files are required:

1. [**`autocpp.sh`**](https://raw.githubusercontent.com/adityaa30/programs/master/autocpp.sh)
2. [**`cli.py`**](https://raw.githubusercontent.com/adityaa30/programs/master/cli.py)

However, one file named [**`Template.cpp`**](https://raw.githubusercontent.com/adityaa30/programs/master/Template.cpp) is also required. This file will be used as default template for each question.
