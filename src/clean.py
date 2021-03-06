import shutil
from pathlib import Path
from typing import Union

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json
import sys 

class OrganizeFiles:
    """
    This class is used to organize file in a directory
    by moving files into directories based on extention.
    """
    def __init__(self):
        self.extensions_dest = {}
        ext_dir = read_json(DATA_DIR / "extensions.json")
        for dir_name, ext_list in ext_dir.items():
            for ext in ext_list:
                self.extensions_dest[ext] = dir_name
        # print(self.extensions_dest)


    def __call__(self, directory: Union(str, Path)):
        """ Organize files in a directory by moving them
        to sub directories based on extension.
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"{directory} does not exist")

        logger.info(f"Organizing files in {directory}...")
        file_extensions = []
        for file_path in directory.iterdir():

            #ignore directory
            if file_path.is_dir():
                continue

            # ignore hidden files
            if file_path.name.startswith('.'):
                continue

            # get all file types
            file_extensions.append(file_path.suffix)
            # move files
            if file_path.suffix not in self.extensions_dest:
                DEST_DIR = directory / 'other'
            else:
                DEST_DIR = directory / self.extensions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok = True)
            logger.info(f"Moving {file_path} to {DEST_DIR}...")
            shutil.move(str(file_path), str(DEST_DIR))

if __name__ == "__main__":
    org_files = OrganizeFiles()
    org_files(sys.argv[1])
    logger.info("Done!")


