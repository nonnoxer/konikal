import os
import argparse

def create(path):
    if os.path.exists(path):
        os.chdir(path)
        app = open("app.py", "w+")
        app.write("print(\"Hello world!\")")
    else:
        path_list = path.split("/")
        for i in path_list:
            try:
                os.mkdir(i)
            except FileExistsError:
                pass
            except FileNotFoundError:
                print("Invalid path")
                exit()
            os.chdir(i)
        app = open("app.py", "w+")
        app.write("print(\"Hello world!\")")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    create_parser = parser.add_subparsers().add_parser("create")
    create_parser.add_argument("path", nargs="?", default=".", metavar="path", type=str)
    args = parser.parse_args()
    create(vars(args)["path"])
