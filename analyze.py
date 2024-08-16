__author__ = 'password123456'
__date__ = '2024.08.16'
__version__ = '1.0.1'
__status__ = 'Production'

import os
import sys
import requests
import json
from datetime import datetime


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



def analyze_logs(scan_id, scan_log_dir, scan_logfiles):
    output_file = os.path.join(scan_log_dir, f'{datetime.now().strftime("%Y%m%d")}_{scan_id}_result.log')
    content_result = ''
    contents = ''
    no_open_ports_ips = []
    open_ports_ips = {}
    for logfile in scan_logfiles:
        if os.path.getsize(logfile) == 0:
            no_open_ports_ips.append(os.path.splitext(logfile.split('_')[2])[0])
            continue

        with open(logfile, 'r', encoding='utf-8') as f:
            file_content = f.readlines()

        for i, line in enumerate(file_content):
            if line.startswith('#') or len(line.strip()) == 0:
                continue

            if os.path.exists(output_file):
                mode = 'a'
            else:
                mode = 'w'

            with open(output_file, mode, encoding='utf-8') as output:
                parts = line.strip().split()
                if len(parts) == 5:
                    status = parts[0]
                    protocol = parts[1]
                    port = parts[2]
                    ip = parts[3]
                    discovery_time = parts[4]

                    output.write(f'datetime="{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",'
                                 f'scan_id="{scan_id}",ip="{ip}",port="{port}",proto="{protocol}",'
                                 f'status="{status},reason="syn-ack",'
                                 f'discovery_ime="{datetime.fromtimestamp(int(discovery_time)).strftime("%Y-%m-%d %H:%M:%S")}"\n')

                    if ip not in open_ports_ips:
                        open_ports_ips[ip] = []  
                    open_ports_ips[ip].append(port)

        if open_ports_ips:
            for ip in open_ports_ips:
                open_ports_ips[ip] = ', '.join(open_ports_ips[ip])  

            for ip, ports in open_ports_ips.items():
                contents = f'\t- {ip} = [ {ports} ]\n'
            content_result += contents

    return scan_id, len(scan_logfiles), output_file, content_result, no_open_ports_ips


def print_results(ret_scan_id, ret_count_logfiles, ret_output_filename, ret_open_ports_list, ret_no_open_ports_list):
    header = (f'------------------------------------------------\n'
              f'Scanning result for `{ret_scan_id}`\n'
              f'------------------------------------------------\n')

    bottom = (f'Outputs:\n\t{ret_output_filename}\n\n'
              f'>> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
              f'>> Total: {ret_count_logfiles}')

    body = f'Open Ports:\n{ret_open_ports_list}'

    if isinstance(ret_no_open_ports_list, list):
        message = f'No Open Ports:\n\t- ' + '\n\t- '.join(ret_no_open_ports_list) + '\n\n'
    else:
        message = f'No Open Ports:\n\t- {ret_no_open_ports_list}\n\n'

    message = f'{header}\n{message}{body}\n{bottom}'

    # send_to_your_WEBHOOK(message)
    print(message)

    """
    ------------------------------------------------
    Scanning result for `rgA-X2EbN9CNxZ47`
    ------------------------------------------------
    
    No Open Ports:
            - 10.210.0.9
            - 10.210.0.10
            - 10.210.0.11
    
    Open Ports:
            - 10.210.0.12 = [ 80, 443 ]
            - 10.210.0.13 = [ 80, 443, 22, 3306 ]
    
    Outputs:
            /data/portscan/logs/20240816_rgA-X2EbN9CNxZ47_result.log
    
    >> 2024-08-16 07:53:33
    >> Total: 5
    """


def main():
    scan_id = '{PORT-SCAN-JOB_ID}'
    home_path = os.path.dirname(os.path.realpath(__file__))
    scan_log_dir = os.path.join(home_path, 'logs')
    scan_logfiles = []

    if os.path.isdir(scan_log_dir):
        for root, _, files in os.walk(scan_log_dir):
            for file in files:
                if file.split('_')[1] == scan_id and file.endswith('.txt'):
                    scan_logfiles.append(os.path.join(root, file))

    ret_scan_id, ret_count_logfiles, ret_output_filename, ret_open_ports_list, ret_no_open_ports_list \
        = analyze_logs(scan_id, scan_log_dir, scan_logfiles)

    if len(ret_no_open_ports_list) == 0:
        ret_no_open_ports_list = 'Not Found'

    if all([ret_scan_id, ret_count_logfiles, ret_output_filename, ret_open_ports_list, ret_no_open_ports_list]):
        print_result(ret_scan_id, ret_count_logfiles, ret_output_filename,
                     ret_open_ports_list, ret_no_open_ports_list)
        

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'{Bcolors.Yellow}- ::Exception:: Func:[{__name__}] '
              f'Line:[{sys.exc_info()[-1].tb_lineno}] [{type(e).__name__}] {e}{Bcolors.Endc}')
