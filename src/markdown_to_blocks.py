from textnode import *
from splitnode import *

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    final_list = []
    for block in block_list:
        new_value = block.strip()
        if len(new_value) == 0:
            continue
        final_list.append(new_value)

    return final_list