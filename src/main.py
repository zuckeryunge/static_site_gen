from generate_webpage import copy_static_to_public_dir



def main():
    path_to_static = "./static"
    path_to_public = "./public"

    copy_static_to_public_dir(path_to_static, path_to_public)



main()
