#!/usr/bin/env python3

import subprocess
import sys

DEVICES = [
    '/dev/sda -a',
    '/dev/sdb -a'
]

EXIT_STATUS = {
    'CRITICAL': 2,
    'WARNING': 1,
    'OK': 0,
    'UNKNOWN': 3
}


def check_device(device_node_string):
    with subprocess.Popen(
            ("sudo smartctl %s" % (device_node_string)).split(),
            stdout=subprocess.PIPE,
    ) as running_process:
        try:
            output, _ = running_process.communicate()
            return_code = running_process.poll()
        except Exception as e:
            running_process.kill()
            running_process.wait()
            print(str(e), file=sys.stderr)
            sys.exit(EXIT_STATUS.get('CRITICAL'))

    if (return_code):
        print(output, file=sys.stderr)
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

    if any(combined_exit_code):
        print("CRITICAL\n%s" % (combined_output))
        sys.exit(EXIT_STATUS.get('CRITICAL'))
    else:
        print("OK\n%s" % (combined_output))
        sys.exit(EXIT_STATUS.get('OK'))


if __name__ == '__main__':
    main()
