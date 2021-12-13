import shutil
from pathlib import Path

from loguru import logger

from src.data import DATA_DIR
from src.utils.io import read_json



class OrganizeFiles:
    """
    This class is used to organize file in a directory
    by moving files into directories based on extention.
    """
    def __init__(self, directory):
        self.directory = Path(directory)
        if not self.directory.exists():
            raise FileNotFoundError(f"{self.directory} does not exist")

        logger.info(f"Organizing files in {directory}...")
        self.extensions_dest = {}
        ext_dir = read_json(DATA_DIR / "extensions.json")
        for dir_name, ext_list in ext_dir.items():
            for ext in ext_list:
                self.extensions_dest[ext] = dir_name
        print(self.extensions_dest)


    def __call__(self):
        """ Organize files in a directory by moving them
        to sub directories based on extension.
        """
        file_extensions = []
        for file_path in self.directory.iterdir():

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
                DEST_DIR = self.directory / 'other'
            else:
                DEST_DIR = self.directory / self.extensions_dest[file_path.suffix]

            DEST_DIR.mkdir(exist_ok = True)
            logger.info(f"Moving {file_path} to {DEST_DIR}...")
            shutil.move(str(file_path), str(DEST_DIR))

if __name__ == "__main__":
    org_files = OrganizeFiles\
        ('/mnt/d/Download')
    org_files()
    logger.info("Done!")


