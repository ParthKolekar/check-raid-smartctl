#!/usr/bin/env python

import subprocess
import sys

DEVICES = [
    '-H /dev/sda',
    '-H /dev/sdb',
    '-H /dev/sdc',
    '-H /dev/sdd'
]

EXIT_STATUS = {
    'CRITICAL': 2,
    'WARNING': 1,
    'OK': 0,
    'UNKNOWN': 3
}


def check_device(device_node_string):
    running_process = subprocess.Popen(
            ("sudo smartctl %s" % (device_node_string)).split(),
            stdout=subprocess.PIPE
    )
    try:
        output, _ = running_process.communicate()
        return_code = running_process.poll()
    except Exception, e:
        running_process.kill()
        running_process.wait()
        print(str(e))
        sys.exit(EXIT_STATUS.get('CRITICAL'))

    if (return_code):
        print(output)
        if (return_code & 8):
            exit_code = EXIT_STATUS.get('CRITICAL')
            exit_output = "DISK %s: FAILING\n" % (device_node_string)
        else:
            exit_code = EXIT_STATUS.get('OK')
            exit_output = "DISK %s: UNKNOWN\n" % (device_node_string)
    else:
        exit_code = EXIT_STATUS.get('OK')
        exit_output = ""

    return exit_code, exit_output


def main():
    device_status = tuple(map(check_device, DEVICES))

    combined_output = "".join(map(lambda x: x[1], device_status))
    combined_exit_code = tuple(map(lambda x: x[0] != EXIT_STATUS.get('OK'), device_status))

    for i in combined_exit_code:
        if i:
            print("CRITICAL\n%s" % (combined_output))
            sys.exit(EXIT_STATUS.get('CRITICAL'))
    else:
        print("OK\n%s" % (combined_output))
        sys.exit(EXIT_STATUS.get('OK'))


if __name__ == '__main__':
    main()
