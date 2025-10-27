import sys
from generate_webpage import copy_static_to_public_dir, generate_pages_recursive



def main():
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    path_to_static = "./static"
    path_to_public = "./docs"
    path_to_content = "./content"
    path_to_template = "./template.html"

    copy_static_to_public_dir(path_to_static, path_to_public)
    generate_pages_recursive(basepath, path_to_content, path_to_template, path_to_public)

main()
