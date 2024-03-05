import csv
import math


database_indexes = [2, 8, 11, 14, 17, 20, 53, 82, 85]  # реальные значения


def get_errors():
    csv_file_path = r'EuData.csv'
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        absolute_errors = [[] for _ in range(9)]
        relative_errors = [[] for _ in range(9)]

        for row in reader:
            for data_index, data_value in enumerate(database_indexes):
                value = row[data_value]
                min_error = row[data_value+1]
                max_error = row[data_value+2]
                if value and max_error and min_error:
                    value = float(value)
                    if value == 0: continue
                    min_error = float(min_error)
                    max_error = float(max_error)
                    if not math.isfinite(min_error) or not math.isfinite(max_error): continue
                    relative_error_min = min_error/value
                    relative_error_max = max_error/value
                    relative_errors[data_index].append((relative_error_max+relative_error_min)/2)
                    absolute_errors[data_index].append((max_error+min_error)/2)
        return (absolute_errors, relative_errors)

def main():
    errors_absolute, errors_relative = get_errors()
    average_error = 0
    for error in errors_relative:
        average_error += sum(error)/len(error)
        print(sum(error)/len(error))
    print(average_error/9)
if __name__ == "__main__":
    main()
