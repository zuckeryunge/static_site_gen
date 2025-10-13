
def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in split_blocks:
        block.strip()
        if block != "":
            clean_blocks.append(block)

    return clean_blocks
