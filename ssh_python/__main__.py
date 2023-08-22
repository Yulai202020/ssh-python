from ssh_python.shell import run
from sys import argv

# python3 shell.py [ip address] [username] [password/path to key file] [workdir on pc (files to copy)]

def main():
    ip = argv[1]
    username = argv[2]
    password = argv[3]
    workdir = argv[4]

    run(ip, username, password, workdir)

if __name__ == "__main__":
    main()