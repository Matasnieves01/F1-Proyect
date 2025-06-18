import subprocess
from watchfiles import run_process

def run():
    cmd = ['daphne', '-b', '0.0.0.0', '-p', '8010', 'config.asgi:application']
    run_process('.', cmd)

if __name__ == '__main__':
    run()
