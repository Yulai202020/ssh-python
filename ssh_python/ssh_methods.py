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

def check_file_exits(path: str, ssh: SSHClient):
    try:
        sftp = ssh.open_sftp()
        sftp.stat(path)
    except:
        return False
    else:
        return True
    finally:
        sftp.close()

### Run commands on vm/server

def run_command(command: str, ssh: SSHClient) -> dict:

    stdin, stdout, stderr = ssh.exec_command(command)

    out, err = "", ""

    for line in stdout.readlines():
        out = out + line + "\n"

    for line in stderr.readlines():
        err = err + line + "\n"
    
    stdin.close()
    
    return {"stdout": out, "stderr": err}

### Operations with files

def copy(path_to_file: str, path_to_copy: str, ssh: SSHClient) -> str:
    sftp = ssh.open_sftp()
    sftp.put(path_to_file, path_to_copy)
    sftp.close()

    return "OK"

def rm_file(path_to_file: str, ssh: SSHClient) -> str:
    sftp = ssh.open_sftp()
    sftp.remove(path_to_file)
    sftp.close()

    return "OK"

### Operations with dirs

def ls_dir(path: str, ssh: SSHClient) -> list:
    sftp = ssh.open_sftp()
    list_dirs = sftp.listdir(path)
    sftp.close()

    return list_dirs

# dev

def run_init_file(path_init_file: str, ssh: SSHClient):
    # name of file
    name = os.path.splitext(path_init_file)[0]

    # copy file
    copy(path_to_file = path_init_file, path_to_copy = f"/{name}.sh", ssh = ssh)
    
    # chmod copied file
    run_command(f"chmod +x {name}.sh", ssh = ssh)

    # run file and save logs
    logs = run_command(f"./{name}.sh", ssh = ssh)

    # delete file
    rm_file(f"/{name}.sh", ssh = ssh)

    return logs

def close(ssh: SSHClient):
    ssh.close()