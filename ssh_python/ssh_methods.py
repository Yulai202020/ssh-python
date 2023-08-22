import os
from os.path import isfile
from ssh_python.conn import connection
from paramiko import AutoAddPolicy, SSHClient

### Connections

def get_ssh_client(conn: connection) -> SSHClient:
    key = isfile(conn.password)

    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())

    if key:
        client.connect(conn.ip, username = conn.user, key_filename = conn.password)
    else:
        client.connect(conn.ip, username = conn.user, password = conn.password)

    return client

def check_file_exits(path: str, conn: connection):
    client = get_ssh_client(conn=conn)
    try:
        sftp = client.open_sftp()
        sftp.stat(path)
    except:
        return False
    else:
        return True
    finally:
        sftp.close()
        client.close()


### Run commands on vm/server

def run_command(command: str, conn: connection) -> dict:
    ssh = get_ssh_client(conn = conn)

    stdin, stdout, stderr = ssh.exec_command(command)

    out, err = "", ""

    for line in stdout.readlines():
        out = out + line + "\n"

    for line in stderr.readlines():
        err = err + line + "\n"
    
    stdin.close()
    ssh.close()

    return {"stdout": out, "stderr": err}

### Operations with files

def copy(path_to_file: str, path_to_copy: str, conn: connection) -> str:
    client = get_ssh_client(conn = conn)

    sftp = client.open_sftp()
    sftp.put(path_to_file, path_to_copy)

    sftp.close()
    client.close()

    return "OK"

def rm_file(path_to_file: str, conn: connection) -> str:
    ssh = get_ssh_client(conn = conn)
    sftp = ssh.open_sftp()

    sftp.remove(path_to_file)

    sftp.close()
    ssh.close()

    return "OK"

### Operations with dirs

def ls_dir(path: str, conn: connection) -> list:
    ssh = get_ssh_client(conn = conn)
    sftp = ssh.open_sftp()

    list_dirs = sftp.listdir(path)

    sftp.close()
    ssh.close()

    return list_dirs

# dev

def run_init_file(path_init_file: str, conn: connection):
    # name of file
    name = os.path.splitext(path_init_file)[0]

    # copy file
    copy(path_to_file = path_init_file, path_to_copy = f"/{name}.sh", conn = conn)
    
    # chmod copied file
    run_command(f"chmod +x {name}.sh", conn = conn)

    # run file and save logs
    logs = run_command(f"./{name}.sh", conn = conn)

    # delete file
    rm_file(f"/{name}.sh", conn = conn)

    return logs