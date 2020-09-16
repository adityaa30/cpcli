# Competitive Programming CLI

![Commit](https://github.com/adityaa30/cp-cli/workflows/Check%20Commit/badge.svg)
![Test](https://github.com/adityaa30/cp-cli/workflows/Test/badge.svg)

### Download Guide

```bash
# Clone the repository
git clone https://github.com/adityaa30/cp-cli

# Change directory to the cloned directory
cd cp-cli

# Install
pip install -e .
``` 

### Requirements

- Python 3.6+
- [lxml](https://pypi.org/project/lxml/)
- [zope.interface](https://pypi.org/project/zope.interface/)

### Docs

```bash
cpcli --help
```

```text
usage: cpcli [-h] [-t TEMPLATE] [-p PATH] -c CONTEST {download,run,show} ...

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
                        Codechef: cc::JUNE20A
```


For example to download **Codeforces Round #661 (Div. 3)** sample test cases, create a URI using the contest id.
For the above contest - Link is **https://codeforces.com/contest/1399/**
Contest ID is 1399 -> URI would become `cf::1399`

### `download`

```bash
cpcli -c cf::1339 download
```

```text
Found: Codeforces Round #633 (Div. 2) ✅
Scraping problems:
Question 1: A-Filling-Diamonds [⏰ 1 sec] [1 Samples]
Question 2: B-Sorted-Adjacent-Differences [⏰ 1 sec] [1 Samples]
Question 3: C-Powered-Addition [⏰ 1 sec] [1 Samples]
Question 4: D-Edge-Weight-Assignment [⏰ 1 sec] [3 Samples]
Question 5: E-Perfect-Triples [⏰ 2 sec] [1 Samples]
Saved in ./ContestFiles/Codeforces-1339
```

All the problems will be saved in a tree like structure as below::

```text
ContestFiles
└── Codeforces-1339
    ├── A-Filling-Diamonds.cpp
    ├── B-Sorted-Adjacent-Differences.cpp
    ├── C-Powered-Addition.cpp
    ├── D-Edge-Weight-Assignment.cpp
    ├── E-Perfect-Triples.cpp
    └── metadata.json
```

Here, `*.cpp` is a copy of Template file (by default taken from `./Template.cpp`). To specify a custom template use `-t` or `--template` flag.

```bash
cpcli -t <path-to-template> -c cf::1339 download
```

### `run`

```bash
cpcli -c cf::1339 run -h
```

```text
usage: cpcli run [-h] [-s SOLUTION_FILE] question

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
cpcli -c cf::1339 run 3
# OR
cpcli -c cf::1339 run powered
# OR
cpcli -c cf::1339 run add
```

```text
[#] Checking question: C-Powered-Addition
[#] Sample Test Case 1: ✅
```

OR

```text
[#] Checking question: C-Powered-Addition
[#] Sample Test Case 1: ❌ (WA)
Sample Input:
 ...

Sample Output:
 ...

Your Output:
 ...
```

OR

```text
[#] Checking question: C-Powered-Addition
[#] Sample Test Case 1: ❌ (TLE) [>1 sec]
```

### `show`

```bash
cpcli -c cf::1339 show -h
```

```text
usage: cpcli show [-h] [-v] [-q QUESTION]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         If True show all test cases (default=False)
  -q QUESTION, --question QUESTION
                        Shows only test cases of the provided question
```

Example:

```bash
cpcli -c cf::1339 show
```

```text
Question 1: A-Filling-Diamonds [⏰ 1 sec] [1 Samples]
Question 2: B-Sorted-Adjacent-Differences [⏰ 1 sec] [1 Samples]
Question 3: C-Powered-Addition [⏰ 1 sec] [1 Samples]
Question 4: D-Edge-Weight-Assignment [⏰ 1 sec] [3 Samples]
Question 5: E-Perfect-Triples [⏰ 2 sec] [1 Samples]
```
