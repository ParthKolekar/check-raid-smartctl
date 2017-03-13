check_raid (OLD)
================

This is a backport to `python2`. Please do not use this. Use the `master` branch.

Checks RAID array via `smartctl` from package `smartmontools` to give a nagios format output.

Usage
-----

- Edit the DEVICES inside the script to match your smartctl parameters, and make a nagios command
for it. Recommended name: `check_raid_smartctl`.

- Allow NOPASSWD sudo for the nagios / nrpe user for the command smartctl. (Being specific about 
the commands is nice and recommended. Quick and easy hack for smartctl * is minimally required).

- Party Hard! (Is a Must!)


