import os
import shutil



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
        os.mkdir(dest)
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

