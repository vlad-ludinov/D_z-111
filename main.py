import requests
import argparse
import time
import threading
from multiprocessing import Process, Pool
import asyncio
import aiohttp

# ссылки на картинки
# https://polska-mebel.ru/upload/iblock/c9d/9nu05xz384265g27f0ciog159spmce7l/stulhalmarrafoolkha.jpg
# https://static.insales-cdn.com/images/products/1/4669/191615549/office-furniture-modern-rustic-office-furniture-expansive-dark-office-table-lamps-l-485045f98938.jpg
# https://diamondelectric.ru/images/3018/3017391/chainii_serviz_beatrix_1.jpg

# pip install requests
def download_image(url: str, start_time):
    name = url.split('/')[-1]
    img_data = requests.get(url).content
    save(name, img_data, start_time)


async def download_image_async(url, start_time):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img_data = await response.read()
            name = url.split('/')[-1]
            save(name, img_data, start_time)


def save(name, img_data, start_time):
    with open(name, 'wb') as handler:
        handler.write(img_data)
        print(f"file {name} download: {time.time() - start_time:.3f}")


def download_threading(urls, start_time):
    threads = []

    for url in urls:
        thread = threading.Thread(target=download_image, args=[url, start_time])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def download_multiprocessing(urls, start_time):
    processes = []

    for url in urls:
        process = Process(target=download_image, args=(url, start_time,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


async def download_asyncio_main(urls, start_time):
    tasks = []

    for url in urls:
        task = asyncio.ensure_future(download_image_async(url, start_time))
        tasks.append(task)
    await asyncio.gather(*tasks)


def download_asyncio(urls, start_time):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_asyncio_main(urls, start_time))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="url to jpg")
    parser.add_argument("-u", metavar="u", type=str, nargs="+", help="load jpg from url")
    arg = parser.parse_args()
    start_time = time.time()
    # download_threading(arg.u, start_time)
    # download_multiprocessing(arg.u, start_time)
    download_asyncio(arg.u, start_time)
    print(f"program time is: {time.time() - start_time:.3f}")
