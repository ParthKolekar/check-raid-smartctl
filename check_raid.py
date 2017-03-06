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


def run_function_wrapper(*popenargs, input=None, timeout=None, check=False, **kwargs):
    """
        Shamelessly copied from python3.5 source.
    """
    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    with subprocess.Popen(*popenargs, **kwargs) as process:
        try:
            stdout, stderr = process.communicate(input, timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            raise subprocess.TimeoutExpired(
                process.args,
                timeout,
                output=stdout,
                stderr=stderr
            )
        except:
            process.kill()
            process.wait()
            raise
        retcode = process.poll()
        if check and retcode:
            raise subprocess.CalledProcessError(
                retcode,
                process.args,
                output=stdout,
                stderr=stderr
            )
    return subprocess.CompletedProcess(process.args, retcode, stdout, stderr)


def check_device(device_node_string):
    try:
        completed_process = run_function_wrapper(
            ("sudo smartctl %s" % (device_node_string)).split(),
            stdout=subprocess.PIPE
        )
        return_code = completed_process.returncode
    except Exception as e:
        print(str(e), file=sys.stderr)
        sys.exit(EXIT_STATUS.get('CRITICAL'))

    if (return_code):
        print(completed_process.stdout.decode(), file=sys.stderr)
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
