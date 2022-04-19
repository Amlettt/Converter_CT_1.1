import datetime
import copy
import eel
import csv


@eel.expose
def read_csv(address):
    list_for_secretar = []
    row = []
    """ считываем полученный файл участников для конвертирования в СЕКРЕТАРЬ"""
    with open(address) as f:
        try:
            reader = list(csv.reader(f, delimiter=';'))

            reader.pop(0)  # удаляем первую строчку с названиями колонок

            for i in reader:  # добавляем всем строчкам вначало один столбец (№ в делегации) и еще четыре значения в конец списка, для того чтобы туда закинуть информацию по участии в дистанциях
                i.insert(0, '')
                i.extend(['', '', '', ''])

            index = 1  # номера связок/групп
            number_index = 1  # считаем сколько человек в связке/группе
            klass = ''
            delegacia = ''
            sex = ''
            for i in range(len(reader)):
                a = reader[i][1].lower().split('_')
                if klass != reader[i][1][0]:
                    klass = reader[i][1][0]
                    index = 1
                    number_index = 1
                    delegacia = ''

                if 'sv' in a or 'св' in a:
                    if 'sm' in a or 'см' in a:
                        reader[i][17] = 'см'
                        if delegacia != reader[i][5]:
                            delegacia = reader[i][5]
                            number_index = 1
                            index = 1
                        else:
                            if number_index < 2:
                                number_index += 1
                            else:
                                number_index = 1
                                index += 1

                    elif reader[i][2].lower() == 'м':
                        reader[i][17] = reader[i][2].lower()
                        if delegacia != reader[i][5]:
                            delegacia = reader[i][5]
                            number_index = 1
                            index = 1
                        else:
                            if number_index < 2:
                                number_index += 1
                            else:
                                number_index = 1
                                index += 1

                    elif reader[i][2].lower() == 'ж':
                        reader[i][17] = reader[i][2].lower()
                        if delegacia != reader[i][5]:
                            delegacia = reader[i][5]
                            number_index = 1
                            index = 1
                        else:
                            if number_index < 2:
                                number_index += 1
                            else:
                                number_index = 1
                                index += 1
                    reader[i][18] = str(index)

                elif 'gr' in a or 'гр' in a:
                    if delegacia != reader[i][5]:
                        delegacia = reader[i][5]
                        number_index = 1
                        index = 1
                    else:
                        if number_index >= 4:
                            number_index += 1
                        else:
                            number_index = 1
                            index += 1
                    reader[i][19] = str(index)
                else:
                    reader[i][16] = '1'

            for i in range(len(reader)):  # будем считывать начиная со 2 строчки i=1
                row.clear()

                row = [reader[i][0], reader[i][5], reader[i][7], reader[i][13], reader[i][3] + " " + reader[i][4], reader[i][10],
                       razrayd(reader[i][8]), reader[i][2].lower(), category(reader[i][1]), reader[i][1][0], '',
                       reader[i][16], reader[i][17], reader[i][18], reader[i][19]]
                list_for_secretar.append(copy.deepcopy(row))

            list_for_secretar.sort(key=lambda x: x[1])

            return converting(list_for_secretar)
        finally:
            f.close()


#  вычисляем какую дистанцию бежит спортсмен
# def distance(a, sex, number_svayzka, number_group):
#     a = a.lower().split('_')
#     lib_distance = ['', '', '', '']
#     if 'sv' in a or 'св' in a:
#         if 'sm' in a or 'см' in a:
#             lib_distance[1] = 'см'
#         else:
#             lib_distance[1] = sex
#         lib_distance[2] = number_svayzka
#     elif 'gr' in a or 'гр' in a:
#         lib_distance[3] = number_group
#     else:
#         lib_distance[0] = 1
#     return lib_distance


#  переводим разряды из файла в необходимый формат
def razrayd(text):
    lib_razrayd = {
        'б.р.': 'б/р',
        '3ю': '3ю',
        '2ю': '2ю',
        '1ю': '1ю',
        '3р': '3',
        '2р': '2',
        '1р': '1',
        'кмс': 'КМС',
        'мс': 'МС',
    }
    return lib_razrayd[text]


#  возрастную категорию формируем по концовке группы из оргео
def category(a):
    a = a.split('_')
    lib_category = {
        '10-11': 'МАЛ/ДЕВ-10-11',
        '12-13': 'МАЛ/ДЕВ-12-13',
        '14-15': 'ЮН/ДЕВ-14-15',
        '16-21': 'ЮНР/ЮНРК-16-21'
    }
    return lib_category[a[-1]] if any(map(str.isdigit, a[-1])) else 'М/Ж'


@eel.expose
def converting(rows):
    try:
        with open('Convert_' + str(datetime.date.today()) + '.csv', 'w', newline='') as File:  # создаем файл для записи
            File_write = csv.writer(File, delimiter=';')
            name = (
            '№ п/п', 'Делегация', 'Территория', 'Представитель', 'Фамилия Имя', 'Год рождения', 'Разряд', 'Пол', 'Группа',
            'Класс дистанции', 'Номер чипа', 'личка', 'связка', 'номер связки', 'номер группы')
            File_write.writerow(name)  # записываем в файл названия столбцов\
            delegacia = ''
            index = 0
            for row in rows:
                if delegacia != row[1]:
                    delegacia = row[1]
                    index = 0
                index += 1
                row[0] = index
                File_write.writerow(row)  # записываем по столбцам данные из спорторга переставленного под СЕКРЕТАРЬ

            return 1
    finally:
        File.close()


if __name__ == "__main__":
    eel.init("web")  # расположение папки с html
    eel.start("main.html", size=(400, 520))  # запускаем файл стартовый
