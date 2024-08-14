# Simple Multi-Threaded Port Scanner (feat. Masscan)

![made-with-python][made-with-python]
![Python Versions][pyversion-button]
![Hits][hits-button]

[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg
[made-with-python]: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
[hits-button]: https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpassword123456%2Fsimple-multi-threaded-port-scanner%2F&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false

This tool is a highly efficient, multi-threaded port scanner built using Python and integrated with [Masscan](https://github.com/robertdavidgraham/masscan) - the fastest Internet port scanner.

By leveraging the power of Python's `ThreadPoolExecutor` and Masscan's unparalleled scanning capabilities, this tool can quickly scan a large number of IP addresses and ports, providing you with fast and reliable results.
***

## Table of Contents
  * [1. Features](#1-features)
  * [2. Installation](#2-installation)
  * [3. Usage](#3-usage)
    + [3.1. Configuration](#31-configuration)
    + [3.2. Running the Scanner](#32-running-the-scanner)
    + [3.3. Output](#33-output)
  * [4. Customization](#4-customization)
    + [4.1. Adjusting the Scan Rate](#41-adjusting-the-scan-rate)
    + [4.2. Changing Ports](#42-changing-ports)
  * [5. Notes](#5-notes)
***

## 1. Features

- **Multi-threading:** Scans multiple IPs concurrently, utilizing all available CPU cores for maximum efficiency.
- **Masscan Integration:** Combines the speed and power of Masscan with Python's flexibility.
- **IP Management:** Easily handle large CIDR blocks and exclude specific IP addresses from the scan.
- **Real-time Progress Monitoring:** Track the progress of your scan in real-time, complete with elapsed time and percentage completion.
- **Custom Output:** Save scan results to individual files, with each IP's results neatly organized.

## 2. Installation

Before you begin, ensure you have met the following requirements:

- **Python 3.6+**: Make sure you have Python installed on your machine.
- **Masscan**: Install Masscan on your system.

You can install Masscan via your package manager:

```bash
# On Ubuntu/Debian
$ sudo apt-get install masscan

# On CentOS/RHEL
$ sudo yum install masscan
```

## 3. Usage
### 3.1. Configuration
- Target List: Place your list of target IP addresses or CIDR blocks in `conf/list.txt`.
- Exclusion List: Specify any IP addresses or ranges to exclude in `conf/exclude.txt`.

### 3.2. Running the Scanner
Execute the scanner using the following command:
```bash
$ python3 main.py
```

As the scan runs, you'll see real-time output like this:
```python

▌║█║▌│║▌│║▌║▌█║ Simple Multi-Threaded Port Scanner (feat. Masscan) v1.0.1 ▌│║▌║▌│║║▌█║▌║█

=== Scan Summary ===
- Total IPs to scan        : 255
- IPs excluded from scan   : 4
- Final Target IPs to scan : 251
- Excluded IPs:
	10.210.0.2, 10.210.0.3, 10.210.0.5, 172.16.33.233

>>> O.K Here We go.!

[00:00:00.000126] ( 1 scanned of 251 ) (0.40%) [ (ok) 10.210.0.8, -p80,443 ]
[00:00:00.000146] ( 2 scanned of 251 ) (0.80%) [ (ok) 10.210.0.9, -p80,443 ]
[00:00:00.000154] ( 3 scanned of 251 ) (1.20%) [ (ok) 10.210.0.4, -p80,443 ]
[00:00:00.000160] ( 4 scanned of 251 ) (1.59%) [ (ok) 10.210.0.7, -p80,443 ]
[00:00:00.000166] ( 5 scanned of 251 ) (1.99%) [ (ok) 10.210.0.1, -p80,443 ]
[00:00:00.000172] ( 6 scanned of 251 ) (2.39%) [ (ok) 10.210.0.6, -p80,443 ]
[00:00:00.001225] ( 7 scanned of 251 ) (2.79%) [ (ok) 10.210.0.10, -p80,443 ]
[00:00:00.001241] ( 8 scanned of 251 ) (3.19%) [ (ok) 10.210.0.11, -p80,443 ]
[00:00:00.001249] ( 9 scanned of 251 ) (3.59%) [ (ok) 10.210.0.12, -p80,443 ]

...

>> scan complete!
>> elapsed time: 00:10:43.649449
```
### 3.3. Output
- Each IP scan result is saved in the `logs/` directory, with filenames formatted as `YYYYMMDD-jobid-ip.txt`.
- The progress of the scan is displayed in real-time, showing elapsed time, completed scan count, and percentage progress.
```python
$ cat logs/20240814-rgA-X2EbN9CNxZ47-10.210.0.8.txt
#masscan
open tcp 80 10.210.0.8 1723618805
open tcp 443 10.210.0.8 1723618805
# end

...

$ cat logs/20240814-rgA-X2EbN9CNxZ47-10.210.0.12.txt
#masscan
open tcp 80 10.210.0.12 1723618805
open tcp 443 10.210.0.12 1723618805
# end
```

## 4. Customization
### 4.1. Adjusting the Scan Rate
You can adjust the scan rate by modifying the `--rate` parameter in the `run_masscan` function:
```python
cmd = ['sudo', 'masscan', target, '-p80,443', '--rate', '10000', '-oL', output_file]
```

### 4.2. Changing Ports
To scan different ports, simply update the `-p80,443` parameter to your desired port range or list:
```python
cmd = ['sudo', 'masscan', target, '-p22,80,443', '--rate', '10000', '-oL', output_file]
```

## 5. Notes
- I hope it is helpful to those who need it.
- If you find this helpful, please the **"star"**:star2: to support further improvements.
