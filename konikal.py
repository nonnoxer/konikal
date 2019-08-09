import os
import argparse
from distutils.dir_util import copy_tree

def create(path):
    print(" * Creating files at specified path...")
    if os.path.exists(path):
        os.chdir(path)
        copy_tree(os.path.abspath(os.path.join(__file__, "..", "app")), ".")
    else:
        path_list = os.path.split(path)
        for i in path_list:
            try:
                os.mkdir(i)
            except FileExistsError:
                pass
            except FileNotFoundError:
                print("Invalid path")
                exit()
            os.chdir(i)
        copy_tree(os.path.abspath(os.path.join(__file__, "..", "app")), ".")
    print(" * Done! Launch app.py and navigate to http://localhost:5000/admin to get started!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="konikal", usage="konikal create [path]")
    create_parser = parser.add_subparsers().add_parser("create")
    create_parser.add_argument("path", nargs="?", default=".", metavar="path", type=str)
    args = parser.parse_args()
    create(vars(args)["path"])
