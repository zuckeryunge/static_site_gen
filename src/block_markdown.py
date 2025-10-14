
def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in split_blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            clean_blocks.append(stripped_block)

    return clean_blocks
