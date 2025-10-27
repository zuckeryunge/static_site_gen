import os
import shutil
from block_markdown import markdown_to_html_node



def copy_static_to_public_dir(src, dest):
    print("-----------------------------------------------------")
    if os.path.exists(dest):
        shutil.rmtree(dest)
        print(f"--- deleted directory {dest}")
        print("---")

    print("--- starting copying files")
    print("-----------------------------------------------------")
    
    copy_src_to_dest_recursively(src, dest)

    print("-----------------------------------------------------")



def copy_src_to_dest_recursively(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
        print(f"--- created directory {dest}")
            
    inside_src = os.listdir(src)
    print(f"--- {len(inside_src)} items in {src}")
    if len(inside_src) > 0: 
        print(f">->->- opening branch")
        for item in inside_src:
            new_src = os.path.join(src, item)
            new_dest = os.path.join(dest, item)

            if os.path.isfile(new_src):
                shutil.copy(new_src, new_dest)
                print(f"--- copied {item} from {src} to {dest}")
            else:
                copy_src_to_dest_recursively(new_src, new_dest)
        print(f"<-<-<- finished branch")
    else:
        print(f"-o-o-o empy directory: {src}")



def extract_title(markdown):
    split_md = markdown.split("\n")
    for line in split_md:
        if line.startswith("# "):
            return line[2:]
    raise Exception("yo, there is no heading")





def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # reading and saving contents of the files
    open_from = open(from_path)
    markdown_src = open_from.read()
    open_from.close()
    open_template = open(template_path)
    template_src = open_template.read()
    open_template.close()
    # converting markdown to html_code
    html_node = markdown_to_html_node(markdown_src)
    html_string = html_node.to_html()
    # setting title of the hmtl doc
    html_title = extract_title(markdown_src)
    html_doc = template_src.replace("{{ Title }}", html_title)
    # inserting the content <div> into the html doc <body>
    html_doc = html_doc.replace("{{ Content }}", html_string)
    # setting basepath for hyperlinks
    html_doc.replace('href="/', f'href="{basepath}')
    html_doc.replace('src="/', f'src="{basepath}')
    # creating destinatioin directory and file
    split_path = dest_path.split("/")
    if len(split_path) > 1:
        dir_path = "/".join(split_path[:-1])
        os.makedirs(dir_path, exist_ok=True)
        file_path = dir_path + "/" + split_path[-1]
    else:
        file_path = dest_path
    write_file = open(file_path, "w")
    write_file.write(html_doc)
    write_file.close()


    
def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    # Crawl every entry in the content directory
    print("--------- generating page ----------")
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
        print(f"--- created directory {dest_dir_path}")
    # look into folder, list contents
    # convert and copy md files
    # go deeper into folders
    # if no md: exception
    inside_src = os.listdir(dir_path_content)
    print(f"--- {len(inside_src)} items in {dir_path_content}")
    if len(inside_src) > 0: 
        for item in inside_src:
            new_src = os.path.join(dir_path_content, item)

    # For each markdown file found, generate a new .html file using the same template.html. The generated pages should be written to the public directory in the same directory structure.
            if os.path.isfile(new_src):
                if item[-3:] != ".md":
                    raise Exception(f"file: {item} ist no markdown file (.md)")
                item_html = item[:-2] + "html"
                new_dest = os.path.join(dest_dir_path, item_html)
                generate_page(basepath, new_src, template_path, new_dest)
                print(f"--- generated {item_html} from {dir_path_content} to {dest_dir_path}")
            else:
                new_dest = os.path.join(dest_dir_path, item)
                generate_pages_recursive(basepath, new_src, template_path, new_dest)
    else:
        print(f"-o-o-o empy directory: {dir_path_content}")
