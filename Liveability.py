import csv
import math

def compare_to_earth(row, similarity_indices):
    # Добавлен словарь с важностью молекул атмосферы
    molecule_importance = {'H2O': 3.0, 'CO2': 2.8, 'NH3':2.6,
                           'C': 2.0, 'Na': 1.6, 'O2': 2.1, 'SO2': 1.9,
                           'CH4': 2.1, 'H': 1.6, 'CO': 1.4, 'P': 2.3,
                           'Mg':1.8, 'He':1.6}
    star_hab_zone_coeficient = {
                           'WD': 0.0224, 'Y': 0.0032, 'T':0.0032, 'L': 0.0032,                    # dwarfs
                           'sdOB': 0.1348, 'sdL': 0.0032, 'SdB': 0.0316,'D': 0.0224,# subdwarfs
                           'Pulsar': 0.01, 'PSR': 0.01,                               # neutron stars
                           'M0': 0.2627,'M1': 0.2025,'M2': 0.1703,'M3': 0.1265,'M4': 0.0849,
                                'M5': 0.0548,'M6': 0.0316,'M7': 0.0255,'M8': 0.0228,'M9': 0.0173,# Type M
                           'K4': 0.4472, 'K3': 0.5292, 'K2':0.6083,'K3.5': 0.4899,     # Type K
                                'K2.5': 0.5701, 'K1': 0.6403, 'K0':0.6782, 'K5': 0.4123, 'K9': 0.2811,
                                'K5.5': 0.3937, 'K6':0.3742, 'K7': 0.3162, 'K7.5':0.3058, 'K8': 0.295,
                           'G4': 0.9539,'G3': 0.9899, 'G2': 0.9901,'G2.5': 1.0,       # Type G
                                'G1': 0.9129, 'G0': 0.8607, 'G0.5': 0.8856, 'G5': 0.9434, 'G9': 0.7416,
                                'G6': 0.8888, 'G7': 0.8602, 'G8': 0.8246, 'G8.5': 0.7842, 'G9.5': 0.7106,
                           'F4': 0.4897, 'F3': 0.4623, 'F2': 0.4415,'F1': 0.4026,                # Type F
                                'F0': 0.3716, 'F5': 0.5249, 'F6': 0.6097,
                                'F7': 0.6389, 'F8': 0.7161,'F9': 0.7762,
                           'A0': 0.1622,'A1': 0.1799,'A2': 0.2042,'A3': 0.2427,'A5': 0.2851,
                                'A6': 0.2985, 'A7': 0.3162, 'A8': 0.3311, 'A9': 0.3467,
                           'B0': 0.0047,'B2': 0.0193,'B3': 0.032,'B6': 0.0518,'B9': 0.1179,
                           'V': 1.0, 'I': 0.0045, 'II': 0.0141, 'III': 0.0707, 'IV':0.0447, 'VI':0.2236, 'VII':0.0224,
                            }
    planet_name = row[0]

    # Проверка наличия значения молекул в ячейке и их учет в коэффициенте
    molecules = row[67].split(",")  # Значения молекул в колонке BP
    molecule_coefficient = 1.0  # Начальное значение коэффициента молекул

    # Умножение на коэффициент молекул, если молекула присутствует
    if molecules[0] != '':
        for molecule in molecule_importance:
            if molecule in molecules:
                molecule_coefficient *= molecule_importance[molecule]
        # Деление на коэффициент молекул, если молекула отсутствует
        for key in molecule_importance:
            if key not in molecules:
                molecule_coefficient /= molecule_importance[key]
    else:
        molecule_coefficient = 0.0

    star_type_cell = row[88]
    startype_coefficient = 1.0

    # Проверка, присутствует ли значение типа звезды в словаре важностей
    if star_type_cell != "":


        for star in star_hab_zone_coeficient:
            if star in star_type_cell:
                startype_coefficient *= star_hab_zone_coeficient[star]
        print(startype_coefficient)
    else:
        startype_coefficient = 0.0
    # Формирование словаря сравнения
    comparison_data = {
        'molecules': molecule_coefficient,  # Добавлен коэффициент молекул
        'star_type': startype_coefficient
    }

    # Добавление значений в списки
    for key, value in comparison_data.items():
        if value > 0.0 :
            similarity_indices[key].append(value)

    return planet_name

def main():
    # Укажите путь к вашему CSV-файлу
    csv_file_path = r'EuData.csv'

    # Открытие CSV-файла и чтение данных
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Пропустим первую строку, так как это заголовки

        # Инициализация списков для каждого параметра
        similarity_indices = {
            'molecules': [],
            'star_type':[]
        }

        # Применение функции сравнения ко всей таблице
        total_planets = 0
        for row in reader:
            if reader.line_num <= 5999:
                compare_to_earth(row, similarity_indices)
                total_planets += 1

        # Рассчет средних значений для каждого параметра
        avg_similarity_indices = {key: sum(value) / float(len(value)) if len(value) > 0 else 0.0 for key, value in similarity_indices.items()}

        # Рассчет общего индекса
        final_index = str(math.prod(avg_similarity_indices.values())*100) + "%"

        # Вывод результатов в консоль
        for key, value in avg_similarity_indices.items():
            print(f"\nСреднее значение индекса схожести для {key}: {value:.9f}")

        print(f"\nФинальный общий индекс: {final_index}")
        print(f"\nВсего обработано {total_planets} планет")

if __name__ == "__main__":
    main()
