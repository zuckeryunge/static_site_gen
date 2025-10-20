import os
import shutil



def copy_to_public(public_path, static_path):
    if not os.path.exists(public_path):
        os.mkdir(public_path)
        print(f"created directory {public_path}")
    
    # if inhalt drin then delete
    # log
    #
    # list all the files of static_src_path
    # log how many files are there
    #
    # copy each element into public_dst_path
    # log each cpied file and path and error


def main():
    path_to_public = "../public"
    path_to_static = "../static"
    copy_to_public(path_to_public, path_to_static)



main()
