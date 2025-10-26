from generate_webpage import copy_static_to_public_dir, generate_page



def main():
    path_to_static = "./static"
    path_to_public = "./public"

    copy_static_to_public_dir(path_to_static, path_to_public)
    
    generate_page("./content/index.md", "./template.html", path_to_public + "/index.html")

main()
