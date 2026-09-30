import sys
import os
from pathlib import Path
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection


def get_file_symbols(section, folder_paths):
    for symbol in section.iter_symbols():
        if symbol['st_info']['type'] == 'STT_FILE':
            symbol_name = symbol.name
            if ".conan2_data" in symbol_name:
                folder_paths.add(symbol.name)


def get_folder_paths_from_elf(file_path):
    folder_paths = set()
    with open(file_path, 'rb') as elf_file:
        elf = ELFFile(elf_file)
        for section in elf.iter_sections():
            if isinstance(section, SymbolTableSection):
                get_file_symbols(section, folder_paths)

    return folder_paths


if __name__ == "__main__":

    # Get the arguments passed from common script
    elf_file_path = sys.argv[1:][0]
    folders = get_folder_paths_from_elf(elf_file_path)
    curr_dir = os.getcwd()

    conan_dir = os.path.dirname(os.path.commonpath(folders))
    dir_path = Path(os.path.dirname(curr_dir))
    conan_folder = Path('.conan2_local/')
    temp = conan_dir.split('.conan2_local/')
    docker_path = str(dir_path.joinpath(conan_folder).joinpath(temp[1]))

    path = Path(conan_dir)
    for folder in path.parts:
        if folder.startswith('fnv4'):
            req_folder = folder
            break
    search_string = "/.conan2_local/.conan2_data/"
    index = conan_dir.find(search_string)
    if index != 1:
        local_path = conan_dir[:index+len(search_string)] + req_folder

    print(docker_path, local_path)
