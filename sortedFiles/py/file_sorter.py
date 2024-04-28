import asyncio
import aiofiles.os
import argparse
import os
import shutil
from pathlib import Path


async def move_file(file, destination):
    if not destination.exists():
        await asyncio.to_thread(os.makedirs, destination, exist_ok=True)
    await asyncio.to_thread(shutil.move, file, destination.joinpath(file.name))
    print(f"File {file.name} moved to {destination}")


async def sort_files(source_folder, output_folder):
    source_path = Path(source_folder).resolve()
    output_path = Path(output_folder).resolve()

    tasks = []
    for file in source_path.iterdir():
        if file.is_file():
            destination = output_path.joinpath(file.suffix.replace('.', ''))
            tasks.append(asyncio.create_task(move_file(file, destination)))

    await asyncio.gather(*tasks)

async def main(source_folder, output_folder):
    await sort_files(source_folder, output_folder)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sort files into subfolders based on file extensions.")
    parser.add_argument("source_folder", type=str, help="The path to the source folder.")
    parser.add_argument("output_folder", type=str, help="The path to the output folder.")
    args = parser.parse_args()
    asyncio.run(main(args.source_folder, args.output_folder))
