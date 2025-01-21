import csv

def filter_vacancy(file_path, output_path):
    try:
        # Открываем CSV файл для чтения
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Проверяем наличие необходимых столбцов
            if 'name' not in reader.fieldnames:
                raise ValueError("Отсутствует обязательный столбец 'name' в CSV файле.")

            # Фильтруем строки, где 'name' содержит 'c++' или 'с++'
            filtered_vacancies = [row for row in reader if 'name' in row and any(keyword in row['name'].lower() for keyword in ['c++', 'с++'])]

        # Сохраняем результат в новый CSV файл
        with open(output_path, mode='w', encoding='utf-8', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(filtered_vacancies)

        print(f"Найдено {len(filtered_vacancies)} вакансий, соответствующих критериям. Результаты сохранены в файл: {output_path}")

    except FileNotFoundError:
        print(f"Файл {file_path} не найден. Проверьте путь к файлу.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

input_file = '../data/vacancies_2024.csv'
output_file = '../data/vacancies_by_name.csv'

filter_vacancy(input_file, output_file)
