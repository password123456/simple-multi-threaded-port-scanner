__author__ = 'password123456'
__date__ = '2024.08.14'
__version__ = '1.0.1'
__status__ = 'Production'

import os
import sys
import subprocess
import secrets
import ipaddress
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class Bcolors:
    Black = '\033[30m'
    Red = '\033[31m'
    Green = '\033[32m'
    Yellow = '\033[33m'
    Blue = '\033[34m'
    Magenta = '\033[35m'
    Cyan = '\033[36m'
    White = '\033[37m'
    Orange = '\033[38;5;208m'
    Endc = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def create_job_id():
    return secrets.token_urlsafe(12)


def subprocess_cmd_execute(cmd):
    try:
        result = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        return '(ok)', result
    except subprocess.CalledProcessError as error:
        return '(error)', error.output
    except FileNotFoundError:
        return '(error)', f'-bash: {cmd[0]}: command not found'


def read_list_from_file(file_path):
    result = []
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.readlines()

        for line in file_content:
            if line.startswith('#') or len(line.strip()) == 0:
                continue
            result.append(line.strip())
    return result


def cidr_to_ipaddress(cidrs):
    result = []
    for cidr in cidrs:
        network = ipaddress.ip_network(cidr)
        for ip in network.hosts():
            result.append(ip)
    return result


def run_masscan(target, output_file):
    # sudo masscan 127.0.0.1 -p1-65535 --rate 10000
    # sudo masscan 10.10.10.10 -p1-65535 --rate 10000 -oL result.txt
    cmd = ['sudo', 'masscan', target,
           '-p80,443', '--rate', '10000', '-oL', output_file]

    ret_cmd_status, ret_cmd_result = subprocess_cmd_execute(cmd)
    if ret_cmd_status == '(ok)':
        result = f'(ok)|{target}|{cmd[3]}'
    else:
        result = f'(error)|{target}|{ret_cmd_result}'
    return result


def main():
    home_path = os.path.dirname(os.path.realpath(__file__))
    scan_file = os.path.join(home_path, 'conf/list.txt')
    scan_exclude_file = os.path.join(home_path, 'conf/exclude.txt')
    scan_id = create_job_id()

    if os.path.exists(scan_file):
        scan_lists = read_list_from_file(scan_file)
        scan_ips = cidr_to_ipaddress(scan_lists)
    else:
        print(f'{Bcolors.Yellow}- Not exists target list: {scan_file} {Bcolors.Endc}')
        sys.exit(1)

    if scan_ips:
        exclude_lists = read_list_from_file(scan_exclude_file)
        _count_scan_ips = len(set(scan_ips))
        _count_completed_scan_ips = 0
        print('')
        print(f'{Bcolors.Green}▌║█║▌│║▌│║▌║▌█║ {Bcolors.Red}Simple Multi-Threaded Port Scanner (feat. Masscan) {Bcolors.White}v{__version__}{Bcolors.Green} ▌│║▌║▌│║║▌█║▌║█{Bcolors.Endc}')
        print('')
        print(f'{Bcolors.BOLD}{Bcolors.Cyan}=== Scan Summary ==={Bcolors.Endc}')
        print(f'{Bcolors.Green}- Total IPs to scan        : {Bcolors.White}{_count_scan_ips}{Bcolors.Endc}')

        excluded_scan_ips = []
        futures = []
        with ThreadPoolExecutor(max_workers=3) as executor:
            for scan_ip in scan_ips:
                output_file = os.path.join(home_path, f'logs/{datetime.now().strftime("%Y%m%d")}-{scan_id}-{scan_ip}.txt')
                if str(scan_ip) in exclude_lists:
                    excluded_scan_ips.append(str(scan_ip))
                else:
                    futures.append(executor.submit(run_masscan, str(scan_ip), output_file))
            _count_scan_targets = int(_count_scan_ips - len(excluded_scan_ips))
            print(f'{Bcolors.Green}- IPs excluded from scan   : {Bcolors.White}{len(excluded_scan_ips)}{Bcolors.Endc}')
            print(f'{Bcolors.Green}- Final Target IPs to scan : {Bcolors.White}{_count_scan_targets}{Bcolors.Endc}')
            print(f'- Excluded IPs:\n\t{", ".join(excluded_scan_ips) if excluded_scan_ips else "None"}')
            print('')
            print(f'>>> {Bcolors.Green}O.K Here We go.!{Bcolors.Endc}')
            print('')
            _scan_start_time = datetime.now()
            for future in as_completed(futures):
                result = future.result()
                _count_completed_scan_ips += 1
                scan_elapsed_time = datetime.now() - _scan_start_time
                scan_elapsed_time_formatted = (datetime.min + scan_elapsed_time).strftime("%H:%M:%S.%f")
                if result:
                    _progress_status = (_count_completed_scan_ips / _count_scan_targets) * 100
                    print(f'[{scan_elapsed_time_formatted}] '
                          f'( {_count_completed_scan_ips} scanned of {_count_scan_targets} ) ({_progress_status:.2f}%) '
                          f'[ {result.split("|")[0].strip()} {result.split("|")[1].strip()}, {result.split("|")[2].strip()} ]')
            print('')
            print('>> scan complete!')
            print(f'>> elapsed time: {scan_elapsed_time_formatted}')
    else:
        print(f'{Bcolors.Yellow}- Not exists target list: {scan_file} {Bcolors.Endc}')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'{Bcolors.Yellow}- ::Exception:: Func:[{__name__}] '
              f'Line:[{sys.exc_info()[-1].tb_lineno}] [{type(e).__name__}] {e}{Bcolors.Endc}')
