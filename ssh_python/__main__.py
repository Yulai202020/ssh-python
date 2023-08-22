from sys import argv
from ssh_python.shell import run

def main():
    ip = argv[1]
    username = argv[2]
    password = argv[3]
    workdir = argv[4]

    run(ip, username, password, workdir)

if __name__ == "__main__":
    main()