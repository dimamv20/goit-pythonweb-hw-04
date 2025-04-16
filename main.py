import argparse
import asyncio
import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
l = logging.getLogger(__name__)

async def copy_file(file_path, output_folder):
    try:
        extension = file_path.suffix[1:] if file_path.suffix else "no_extension"
        target_folder = output_folder / extension
        os.makedirs(target_folder, exist_ok=True)
        new_file_path = target_folder / file_path.name
        await asyncio.to_thread(shutil.copy2, file_path, new_file_path)
        l.info(f"Coped: {file_path} → {new_file_path}")
    except Exception as e:
        l.error(f"Error while copy {file_path}: {e}")

async def process_folder(source_folder, output_folder):
    tasks = []
    for root, dirs, files in await asyncio.to_thread(os.walk, source_folder):
        for file_name in files:
            full_path = Path(root) / file_name
            tasks.append(copy_file(full_path, output_folder))
    await asyncio.gather(*tasks)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str)
    parser.add_argument("target", type=str)
    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    target_path = Path(args.output).resolve()

    if not source_path.exists():
        l.error(f"Folder isn't finded: {source_path}")
        return

    await process_folder(source_path, target_path)

if __name__ == "__main__":
    asyncio.run(main())
