from ssh_python.ssh_methods import *
from os.path import isfile
from ssh_python.conn import connection

def check_key_dir(dir: str, n: int):
    if dir[n] == "/":
        return True
    else:
        return False

def run(ip: str, user: str, password: str, workdir_: str):

    # init
    command = [""]
    workdir_vm = "/"
    workdir_copy = workdir_

    if not check_key_dir(workdir_copy, -1):
        workdir_copy = workdir_copy + "/"

    conn = connection(ip = ip, user = user, password = password)

    # shell 
    while True:
        command = input(f"{conn.user}@{conn.ip}:{workdir_vm}$ ").lower().split(" ")

        if command[0] == "exit":
            break

        elif command[0] == "" or command[0] == "\t":
            continue

        elif command[0] == "pwd":
            # Print dir
            print(workdir_vm)

        elif command[0] == "ls":
            # Print all entity in dir
            print(ls_dir(workdir_vm, conn = conn))

        # cd 
        elif command[0] == "cd":
            if command[1] in ls_dir(workdir_vm, conn = conn):
                if check_key_dir(command[1], -1):
                    workdir_vm = workdir_vm + command[1]
                else:
                    workdir_vm = workdir_vm + command[1] + "/"

                ls_dir(workdir_vm, conn = conn)

            elif command[1] == "..":
                if workdir_vm == "/":
                    continue

                x = workdir_vm.split("/")
                x.pop(-1)

                workdir_vm = "/".join(x)

                ls_dir(workdir_vm)

            else:
                ls_dir(command[1])
                workdir_vm = command[1]

        # Copy file from pc to server
        elif command[0] == "copy":
            if isfile(workdir_copy + command[2]):
                copy(path_to_file = command[1], path_to_copy = workdir_copy + command[2], conn = conn)
            else :
                print("File not founded.")
    
        # RM file on server
        elif command[0] == "rmf":
            if check_file_exits(command[1]):
                rm_file(path_to_file = command[1], conn = conn)
            else:
                print("File not founded.")

        # else run command
        else:
            sout = run_command(command = " ".join(command), conn = conn)

            print(sout["stdout"])
            print(sout["stderr"])

        continue