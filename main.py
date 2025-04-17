import asyncio
import shutil
import logging
import argparse
from pathlib import Path


logging.basicConfig(
    filename="errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


async def copy_file(file_path, output_folder):
    try:
        ext = file_path.suffix[1:] if file_path.suffix else "no_extension"
        new_folder = output_folder / ext
        new_folder.mkdir(parents=True, exist_ok=True)
        new_path = new_folder / file_path.name

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, shutil.copy2, file_path, new_path)

    except Exception as e:
        logging.error(f"Помилка при копіюванні {file_path}: {e}")

async def process_folder(source_folder, output_folder):
    for item in source_folder.iterdir():
        if item.is_file():
            await copy_file(item, output_folder)
        elif item.is_dir():
            await process_folder(item, output_folder)


async def main():
    parser = argparse.ArgumentParser(description="Сортування файлів за розширенням")
    parser.add_argument("source", help="Шлях до вихідної папки")
    parser.add_argument("output", help="Шлях до цільової папки")
    args = parser.parse_args()

    source = Path(args.source)
    output = Path(args.output)

    if not source.exists() or not source.is_dir():
        print("Вихідна папка не знайдена або не є папкою.")
        return

    await process_folder(source, output)
    print("Сортування завершено!")

if __name__ == "__main__":
    asyncio.run(main())
