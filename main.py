import argparse
import asyncio
import aiofiles.os
import aiofiles.ospath
import shutil
from pathlib import Path
import logging
import os

# Налаштування логування
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Асинхронна функція для копіювання файлу
async def copy_file(file_path: Path, output_dir: Path):
    try:
        extension = file_path.suffix[1:] if file_path.suffix else "no_extension"
        target_dir = output_dir / extension
        await aiofiles.os.makedirs(target_dir, exist_ok=True)
        target_file = target_dir / file_path.name

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, shutil.copy2, file_path, target_file)
        logger.info(f"Copied: {file_path} → {target_file}")
    except Exception as e:
        logger.error(f"Error copying {file_path}: {e}")

# Асинхронна функція для читання всіх файлів у папці
async def read_folder(source_dir: Path, output_dir: Path):
    tasks = []
    for root, dirs, files in await asyncio.to_thread(lambda: list(os.walk(source_dir))):
        for file in files:
            full_path = Path(root) / file
            tasks.append(copy_file(full_path, output_dir))
    await asyncio.gather(*tasks)

# Основна функція
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str)
    parser.add_argument("output", type=str)

    args = parser.parse_args()

    source_path = Path(args.source).resolve()
    output_path = Path(args.output).resolve()

    if not await aiofiles.ospath.exists(source_path):
        logger.error(f"Вихідна папка не існує: {source_path}")
        return

    await read_folder(source_path, output_path)

if __name__ == "__main__":
    asyncio.run(main())
