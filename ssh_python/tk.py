import os
from sys import argv
from tkinter import ttk
from tkinter import *
from ssh_methods import *

def update_remote_dir(cwd: str, new_dir: StringVar, list_dir: Listbox, cd_option: OptionMenu, client, first_element):
    a = ls_dir(cwd, client)

    list_dir = Listbox(root)
    list_dir.grid(row = 2, column = 1, sticky = W, pady = 2)

    for i in range(len(a)):
        list_dir.insert(i, a[i])
    
    if first_element != "":
        cd_option = OptionMenu(root, dirname_global, first_element, *a)

    else:
        cd_option = OptionMenu(root, new_dir, *a)

    cd_option.grid(row = 1, column = 1, sticky = W, pady = 2)


def init_local():
    dirname = StringVar(root, "/")
    view_dir_local = os.listdir(cwd_local)

    listdir_root = []

    for i in range(len(view_dir_local)):
        listdir_root.append(view_dir_local[i])

    dir_list = Listbox(root)
    dir_list.grid(row = 2, column = 0, sticky = W, pady = 2)

    for i in range(len(listdir_root)):
        dir_list.insert(i, listdir_root[i])

    cd_option = OptionMenu(root, dirname, *listdir_root)
    cd_option.grid(row = 1, column = 0, sticky = W, pady = 2)

    return dirname, view_dir, dir_list, cd_option

def init_remote():
    dirname = StringVar(root, "/")

    view_dir = ls_dir(cwd_remote, client)
    a = []

    for i in range(len(view_dir)):
        a.append(view_dir[i])

    dir_list = Listbox(root)
    dir_list.grid(row = 2, column = 1, sticky = W, pady = 2)

    for i in range(len(a)):
        dir_list.insert(i, a[i])

    cd_option = OptionMenu(root, dirname, *a)
    cd_option.grid(row = 1, column = 1, sticky = W, pady = 2)

    return dirname, view_dir, dir_list, cd_option

### init

conn = connection(argv[1], argv[2], argv[3])
client = get_ssh_client(conn = conn)

root = Tk()

### global

cwd_remote = "/"
dirname_global, view_dir, dir_list_global, cd_option_global = init_remote()

def submit_global():
    global cwd_remote, dir_list_global, cd_option_global

    if dirname_global.get() == "..":
        a = cwd_remote.split("/")
        a.pop(-2)

        b = "/".join(a)
        dirname_global.set(b)
        cwd_remote = dirname_global.get()

        if dirname_local.get() == "":
            dirname_local.set("/")

        elif b == "/":
            update_remote_dir(cwd_remote, dirname_global, dir_list_global, cd_option_global, client, "")

        else:
            update_remote_dir(cwd_remote, dirname_global, dir_list_global, cd_option_global, client, "..")

        return
    
    cwd_remote = cwd_remote + dirname_global.get() + "/"

    update_remote_dir(cwd_remote, dirname_global, dir_list_global, cd_option_global, client, "..")

title_global = Label(root, text = "remote").grid(row = 0, column = 1, sticky = W, pady = 2)

sub_btn_global = ttk.Button(root, text = 'Submit', command = submit_global)
sub_btn_global.grid(row = 3, column = 1, sticky = W, pady = 2)

### local

cwd_local = "/"

dirname_local, view_dir, dir_list_local, cd_option_local = init_local()

def submit_local():
    global cwd_local

    if dirname_local.get() == "..":
        a = cwd_local.split("/")
        a.pop(-2)

        b = "/".join(a)
        dirname_local.set(b)
        print(b)

        cwd_local = dirname_local.get()
        tmp = dirname_local.get().replace("/", "")
        dirname_local.set(tmp)

        if dirname_local.get() == "":
            dirname_local.set("/")

        a = os.listdir(cwd_local)

        dir_list_local = Listbox(root)
        dir_list_local.grid(row = 2, column = 0, sticky = W, pady = 2)

        for i in range(len(a)):
            dir_list_local.insert(i, a[i])

        if b == "/":
            cd_option_local = OptionMenu(root, dirname_local, *a)
            cd_option_local.grid(row = 1, column = 0, sticky = W, pady = 2)

        else:
            cd_option_local = OptionMenu(root, dirname_local, "..", *a)
            cd_option_local.grid(row = 1, column = 0, sticky = W, pady = 2)

        return

    cwd_local = cwd_local + dirname_local.get() + "/"
    update_view_dir = os.listdir(cwd_local)

    dir_list_local = Listbox(root)
    dir_list_local.grid(row = 2, column = 0, sticky = W, pady = 2)

    for i in range(len(update_view_dir)):
        dir_list_local.insert(i, update_view_dir[i])

    cd_option_local = OptionMenu(root, dirname_local, "..", *update_view_dir)
    cd_option_local.grid(row = 1, column = 0, sticky = W, pady = 2)

title_local = Label(root, text = "local").grid(row = 0, column = 0, sticky = W, pady = 2)

sub_btn_local = ttk.Button(root, text = 'Submit', command = submit_local)
sub_btn_local.grid(row = 3, column = 0, sticky = W, pady = 2)

### toolbar

title_toolbar = Label(root, text = "toolbar").grid(row = 0, column = 2, sticky = W, pady = 2)

def copy_():
    from_copy = cwd_local + dirname_local.get()
    to_copy = cwd_remote + dirname_local.get()
    copy(from_copy, to_copy, client)
    update_remote_dir(cwd_remote, dirname_global, dir_list_global, cd_option_global, client, "..")

def rm_():
    file_delete = cwd_remote + dirname_global.get()
    rm_file(file_delete, client)
    update_remote_dir(cwd_remote, dirname_global, dir_list_global, cd_option_global, client, "..")

def update_():
    update_remote_dir(cwd_remote, dirname_global, dir_list_global, cd_option_global, client, "..")

    a = os.listdir(cwd_local)

    dir_list_local = Listbox(root)
    dir_list_local.grid(row = 2, column = 0, sticky = W, pady = 2)

    for i in range(len(a)):
        dir_list_local.insert(i, a[i])

    if cwd_local == "/":
        cd_option_local = OptionMenu(root, dirname_local, *a)
        cd_option_local.grid(row = 1, column = 0, sticky = W, pady = 2)

    else:
        cd_option_local = OptionMenu(root, dirname_local, "..", *a)
        cd_option_local.grid(row = 1, column = 0, sticky = W, pady = 2)


copy_btn = ttk.Button(root, text = 'Copy', command = copy_)
copy_btn.grid(row = 1, column = 2, sticky = W, pady = 2)

rm_btn = ttk.Button(root, text = 'rm file', command = rm_)
rm_btn.grid(row = 2, column = 2, sticky = W, pady = 2)

update_btn = ttk.Button(root, text = 'update', command = update_)
update_btn.grid(row = 2, column = 2, sticky = W, pady = 2)

### run app
mainloop()