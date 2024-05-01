import asyncio
import aiofiles.os
import argparse
import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(filename='file_sorting.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

async def move_file(file, destination, created_dirs):
    try:
        if destination not in created_dirs:
            if not destination.exists():
                await asyncio.to_thread(os.makedirs, destination, exist_ok=True)
            created_dirs.add(destination)
        await asyncio.to_thread(shutil.move, file, destination.joinpath(file.name))
        print(f"File {file.name} moved to {destination}")
    except Exception as e:
        logging.error(f"Error moving file {file}: {e}")
        print(f"Error moving file {file}: {e}")

async def sort_files(source_folder, output_folder):
    source_path = Path(source_folder).resolve()
    output_path = Path(output_folder).resolve()
    created_dirs = set()

    tasks = []
    for file in source_path.iterdir():
        if file.is_file() and not file.name.startswith('.'):
            destination = output_path.joinpath(file.suffix.replace('.', '').lower())
            tasks.append(asyncio.create_task(move_file(file, destination, created_dirs)))

    await asyncio.gather(*tasks)

async def main(source_folder, output_folder):
    if not Path(source_folder).exists() or not Path(output_folder).exists():
        logging.error("One or more specified directories do not exist.")
        print("One or more specified directories do not exist.")
        return
    await sort_files(source_folder, output_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sort files into subfolders based on file extensions.")
    parser.add_argument("source_folder", type=str, help="The path to the source folder.")
    parser.add_argument("output_folder", type=str, help="The path to the output folder.")
    args = parser.parse_args()
    asyncio.run(main(args.source_folder, args.output_folder))

