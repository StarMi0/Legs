import os
from multiprocessing import Pool, cpu_count

from PIL import Image


def resize_png(png_file_path, save_file_path):
    """
    Функция resize_png изменяет размер и формат изображения в формате PNG. Она принимает два аргумента: 
    путь к исходному файлу PNG png_file_path и путь, по которому нужно сохранить измененное изображение 
    save_file_path.

    Сначала функция открывает исходное изображение PNG с помощью модуля Pillow, вычисляет размеры 
    нового квадратного изображения и определяет координаты его центра. Затем исходное изображение 
    обрезается до квадрата и изменяется его размер до 1024 на 1024 пикселей с помощью метода resize.

    Далее создается новое квадратное изображение с черным фоном, определяются координаты 
    его центра и обрезанное изображение вставляется в центр нового изображения с помощью 
    метода paste.
    """
    # Открыть изображение PNG
    with Image.open(png_file_path) as im:
        # Вычислить размеры нового изображения
        width, height = im.size
        new_size = min(width, height)

        # Определить координаты центра изображения
        left = (width - new_size) / 2
        top = (height - new_size) / 2
        right = (width + new_size) / 2
        bottom = (height + new_size) / 2

        # Обрезать изображение до квадрата
        im = im.crop((left, top, right, bottom))

        # Изменить размер изображения до 1024 на 1024 пикселей
        im = im.resize((1024, 1024), resample=Image.LANCZOS)

        # Создать новое изображение с черным фоном
        new_im = Image.new("RGB", (1024, 1024), (0, 0, 0))

        # Вычислить координаты центра нового изображения
        new_left = (1024 - new_size) / 2
        new_top = (1024 - new_size) / 2
        new_right = (1024 + new_size) / 2
        new_bottom = (1024 + new_size) / 2

        # Вставить обрезанное изображение в центр нового изображения
        new_im.paste(im, (int(new_left), int(new_top)))

        # Сохранить новое изображение в выбранном пути
        new_im.save(save_file_path)

        # Вывести сообщение об успешном сохранении
        print(f"Изображение успешно сохранено в {os.path.abspath(save_file_path)}")


def process_file(png_file_path, output_dir):
    """
    Функция process_file принимает путь к файлу PNG и путь для сохранения изображения, 
    обрабатывает файлы, используя функцию resize_png для изменения размера изображения 
    и сохранения его в новой папке.
    """
    # Получить путь для сохранения
    model_number = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(png_file_path)))))
    additional_number = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(png_file_path))))
    angle = os.path.basename(os.path.dirname(os.path.dirname(png_file_path)))
    view = os.path.basename(os.path.dirname(png_file_path))
    
    new_model_number_1 = (model_number + '1')
    new_model_number_2 = (model_number + '2')
    # print(new_model_number_1, new_model_number_2)
    new_output_dir_1 = os.path.join(output_dir, new_model_number_1, angle, view)
    new_output_dir_2 = os.path.join(output_dir, new_model_number_2, angle, view)
    if not os.path.exists(new_output_dir_1):
        os.makedirs(new_output_dir_1)
    if not os.path.exists(new_output_dir_2):
        os.makedirs(new_output_dir_2)
    new_file_path_1 = os.path.join(new_output_dir_1, os.path.basename(png_file_path))
    new_file_path_2 = os.path.join(new_output_dir_2, os.path.basename(png_file_path))

    # Изменить размер и сохранить изображение в новой папке
    resize_png(png_file_path, new_file_path_1)
    resize_png(png_file_path, new_file_path_2)


def main(input_dir, output_dir):
    """
    Функция main является точкой входа в программу. Она создает пул потоков и проходит по всем файлам PNG во входной 
    директории и всех ее подпапках. Для каждого файла PNG, она добавляет задачу в пул потоков для обработки в функции 
    process_file. После того, как все задачи были добавлены в пул потоков, функция main завершает все потоки.
    """
    # Создать пул потоков
    pool = Pool(processes=cpu_count())
    print('pool ok')
    # Пройти по всем файлам PNG во входной директории и всех ее подпапках
    for root, dirs, files in os.walk(input_dir):
        
        for file_name in files:
            if file_name.endswith(".png"):
                # Получить путь к файлу PNG
                png_file_path = os.path.join(root, file_name)
                

                # Добавить задачу в пул потоков
                pool.apply_async(process_file, args=(png_file_path, output_dir))

    # Завершить все потоки
    pool.close()
    pool.join()


if __name__ == "__main__":
    input_dir = "data/validation_dataset/models_alexandr_5_remaining_gold"
    output_dir = "data_a/validation_dataset1"
    main(input_dir, output_dir)
