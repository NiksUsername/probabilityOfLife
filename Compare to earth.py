import csv
import math


def compare_to_earth(row, similarity_indices, stars):
    ev = {'mass': 0.003146633, 'radius': 0.0892857, 'orbital_p': 365.256,
          'eccen': 0.0167, 'temp': 343.0, 'inclin': 23.45,
          's_maj_axis': 1.01671388, 'star_mass': 1.0, 'star_radius': 1.0}

    planet_name = row[0]

    star_name = row[68]

    # Проверка наличия значений в ячейках
    mv = float(row[2]) if row[2] else 0.0
    rv = float(row[8]) if row[8] and ev['radius'] != 0.0 else 0.0
    opv = float(row[11]) if row[11] and ev['orbital_p'] != 0.0 else 0.0
    evv = float(row[17]) if row[17] and ev['eccen'] != 0.0 else 0.0
    tv = float(row[53]) if row[53] and ev['temp'] != 0.0 else 0.0
    iv = float(row[20]) if row[20] and ev['inclin'] != 0.0 else 0.0
    smav = float(row[14]) if row[14] and ev['s_maj_axis'] != 0.0 else 0.0  # Добавлен semi-major-axis
    if star_name not in stars:
        stars.append(star_name)
        star_mass_v = float(row[82]) if row[82] and ev['star_mass'] != 0.0 else 0.0  # Добавлен star_mass
        star_radius_v = float(row[85]) if row[85] and ev['star_radius'] != 0.0 else 0.0  # Добавлен star_radius
        try:
            star_age = float(row[89])
        except ValueError:
            star_age = 0.0
    else:
        star_mass_v = 0.0
        star_radius_v = 0.0
        star_age = 0.0

    comparison_data = {
        'mass': (mv / ev['mass']) if mv / ev['mass'] < 1.0 else ev['mass'] / mv,
        'radius': (rv / ev['radius']) if rv / ev['radius'] < 1.0 else ev['radius'] / rv,
        'orbital_period': (opv / ev['orbital_p']) if opv / ev['orbital_p'] < 1.0 else ev['orbital_p'] / opv,
        'eccentricity': (evv / ev['eccen']) if evv / ev['eccen'] < 1.0 else ev['eccen'] / evv,
        'temperature': (tv / ev['temp']) if tv / ev['temp'] < 1.0 else ev['temp'] / tv,
        'inclination': (iv / ev['inclin']) if iv / ev['inclin'] < 1.0 else ev['inclin'] / iv if iv > 0.0 else 0.0,
        'semi_major_axis': (smav / ev['s_maj_axis']) if smav / ev['s_maj_axis'] < 1.0 else ev['s_maj_axis'] / smav,
        'star_mass': (star_mass_v / ev['star_mass']) if star_mass_v / ev['star_mass'] < 1.0 else ev['star_mass'] / star_mass_v,
        'star_radius': (star_radius_v / ev['star_radius']) if star_radius_v / ev['star_radius'] < 1.0 else ev['star_radius'] / star_radius_v,
        'star_age': star_age,
    }

    # Добавление значений в списки
    for key, value in comparison_data.items():
        if value > 0 :
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
            'mass': [],
            'radius': [],
            'orbital_period': [],
            'eccentricity': [],
            'temperature': [],
            'inclination': [],
            'semi_major_axis': [],
            'star_mass': [],
            'star_radius': [],
            'star_age': [],
        }

        # Применение функции сравнения ко всей таблице
        total_planets = 0
        stars = []
        for row in reader:
            if reader.line_num <= 5999:
                compare_to_earth(row, similarity_indices, stars)
                total_planets += 1

        # Рассчет средних значений для каждого параметра
        avg_similarity_indices = {key: sum(value) / float(len(value)) if len(value) > 0 else 0.0 for key, value in similarity_indices.items()}

        # Рассчет общего индекса
        final_index = str(math.prod(avg_similarity_indices.values())*100) + "%"

        # Вывод результатов в консоль
        for key, value in avg_similarity_indices.items():
            print(f"\nСреднее значение индекса схожести для {key}: {value:.9f}")

        print(f"\nФинальный общий коэфициент: {final_index}")
        print(f"\nВсего обработано {total_planets} планет")


if __name__ == "__main__":
    main()
