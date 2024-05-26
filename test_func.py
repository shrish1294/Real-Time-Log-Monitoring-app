import os
import logging

import traceback
logger = logging.Logger('loggers')



def tail(f, lines=10):
    """reads a large file in chunks of buffer size 1024 and returns last number of lines"""
    total_lines_wanted = lines

    BLOCK_SIZE = 1024
    f.seek(0, 2)
    block_end_byte = f.tell()
    lines_to_go = total_lines_wanted
    block_number = -1
    blocks = []
    while lines_to_go > 0 and block_end_byte > 0:
        if (block_end_byte - BLOCK_SIZE > 0):
            f.seek(block_number*BLOCK_SIZE, 2)
            blocks.append(f.read(BLOCK_SIZE))
        else:
            f.seek(0,0)
            blocks.append(f.read(block_end_byte))
        lines_found = blocks[-1].count(b'\n')
        lines_to_go -= lines_found
        block_end_byte -= BLOCK_SIZE
        block_number -= 1
    all_read_text = b''.join(reversed(blocks))
    return all_read_text.splitlines()[-total_lines_wanted:]



def return_last_10_lines(file_path):
    """from a given file_path returns last 10 lines of the code"""
    line_list = []
    try:
        with open("log_file.txt", 'rb') as f:
            lines = tail(f)
            for i in lines:
                line_list.append(i.decode())
                line_list.append("<br>")
    except Exception:
        logger.error(f"error during exec return_last_10_lines: {traceback.format_exc()}")
        return None
    return line_list 
   
