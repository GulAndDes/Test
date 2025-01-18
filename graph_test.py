import argparse

# Функция записи данных с файла в массивы
def parse_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    # Убираем лишние пробелы и переносы строк
    lines = [line.strip() for line in lines]

    # Инициализация массивов
    array_1 = []  # Первая строка с NV и NE
    array_2 = []  # Пары узлов
    array_3 = []  # Правила агент-функции

    # Флаги для отслеживания текущего блока данных
    current_block = 1

    for line in lines:
        if not line:  
            current_block += 1
            continue

        if current_block == 1:
            # Обрабатываем первую строку с NV и NE
            array_1 = list(map(int, line.split()))
        elif current_block == 2:
            # Обрабатываем пары узлов
            array_2.append(list(map(int, line.split())))
        elif current_block == 3:
            # Обрабатываем правила агент-функции
            array_3.append(line)

    return array_1, array_2, array_3

# Функция для установки значений атрибутов узлов в соответствии с правилами
def process_vertex_values(
    array_1, array_2, array_3, array_of_vertex_from, value_of_vertex, value_of_edge
):
    for i in range(array_1[0]):
        if array_3[i] == "min":
            min_value = float("inf")
            for j in array_of_vertex_from[i]:
                if value_of_edge[j] < min_value:
                    min_value = value_of_edge[j]
            value_of_vertex[i] = min_value
        elif array_3[i][0] == "v":
            value_of_vertex[i] = value_of_vertex[int(array_3[i][2]) - 1]
        elif array_3[i][0] == "e":
            value_of_vertex[i] = value_of_edge[int(array_3[i][2]) - 1]
        else:
            value_of_vertex[i] = float(array_3[i])

# Функция для установки значений атрибутов ребер в соответствии с правилами
def process_edge_values(
    array_1,
    array_2,
    array_3,
    array_of_vertex_in,
    array_of_vertex_from,
    value_of_vertex,
    value_of_edge,
):
    for i in range(array_1[1]):
        if array_3[i + array_1[0]][0] == "v":
            value_of_edge[i] = value_of_vertex[int(array_3[i + array_1[0]][2]) - 1]
        elif array_3[i + array_1[0]][0] == "e":
            value_of_edge[i] = value_of_edge[int(array_3[i + array_1[0]][2]) - 1]
        elif array_3[i + array_1[0]][0] == "*":
            value_of_edge[i] = value_of_vertex[array_2[i][0] - 1]
            for j in array_of_vertex_from[array_2[i][0] - 1]:
                value_of_edge[i] *= value_of_edge[j]
        else:
            value_of_edge[i] = float(array_3[i + array_1[0]])


def write_output(output_file, value_of_vertex, value_of_edge):
    with open(output_file, "w") as f:
        # Записываем значения атрибутов узлов
        for value in value_of_vertex:
            f.write(f"{value}\n")

        # Записываем значения атрибутов рёбер
        for value in value_of_edge:
            f.write(f"{value}\n")


def main(input_file, output_file):
    array_1, array_2, array_3 = parse_file(input_file)

    array_of_vertex_from = [[] for _ in range(array_1[0])]
    array_of_vertex_in = [[] for _ in range(array_1[0])]

    value_of_edge = [float("inf")] * array_1[1]
    value_of_vertex = [float("inf")] * array_1[0]

    c = 0
    for i in array_2:
        i.append(c)
        c += 1

    for i in range(array_1[0]):
        for j in array_2:
            if j[1] == i + 1:
                array_of_vertex_from[i].append(j[2])
            if j[0] == i + 1:
                array_of_vertex_in[i].append(j[2])

    # Итеративное обновление значений до тех пор, пока они не перестанут изменяться
    changed = True
    while changed:
        changed = False
        old_vertex_values = value_of_vertex.copy()
        old_edge_values = value_of_edge.copy()

        process_vertex_values(
            array_1,
            array_2,
            array_3,
            array_of_vertex_from,
            value_of_vertex,
            value_of_edge,
        )
        process_edge_values(
            array_1,
            array_2,
            array_3,
            array_of_vertex_in,
            array_of_vertex_from,
            value_of_vertex,
            value_of_edge,
        )

        if old_vertex_values != value_of_vertex or old_edge_values != value_of_edge:
            changed = True

    # Вывод результатов в файл
    write_output(output_file, value_of_vertex, value_of_edge)


if __name__ == "__main__":
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Обработка аннотируемого метаграфа.")
    parser.add_argument("input_file", type=str, help="Имя файла с входными данными.")
    parser.add_argument(
        "output_file", type=str, help="Имя файла для записи результата."
    )
    args = parser.parse_args()

    # Запуск основной программы
    main(args.input_file, args.output_file)
