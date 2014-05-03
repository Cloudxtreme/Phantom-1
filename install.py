#!/usr/bin/env python
'''
Phantom install script (No dependency)
'''
import sys
import os

PYTHON_VERSION = sys.version_info
def check_env():
    env = { 'version': False, 'tarball': False, 'ionice': False, 'pip': False }

    print '- Checking python version'
    if PYTHON_VERSION < (2, 7) or PYTHON_VERSION >= (3, 0):
        print '-- ERROR: This python version is not supported. Please use version 2.7'
        exit(1)
    else:
        env['version'] = True
        print '-- OK'

    print '- Checking tarball'
    if not which('tar'):
        print '-- ERROR: cannot find tarball(tar) binary'
        exit(1)
    else:
        env['tarball'] = True
        print '-- OK'

    print '- Checking ionice'
    if not which('ionice'):
        print '-- WARNING: cannot find ionice binary, Phantom have no affect on this situation, but IO limit feature is not supported'
    else:
        env['ionice'] = True
        print '-- OK'

    print '- Checking pip'
    if not which('pip'):
        print '-- ERROR: cannot find pip installer. Please install pip'
    else:
        env['pip'] = True
        print '-- OK'

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

if __name__ == "__main__":
    check_env()