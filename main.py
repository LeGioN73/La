import os
import csv


class Report:
    def __init__(self, number, date, student_name, scholarship_amount, destination):
        self.number = number
        self.date = date
        self.student_name = student_name
        self.scholarship_amount = float(scholarship_amount)
        self.destination = destination

    def __repr__(self):
        return (f"Report(№={self.number}, дата={self.date}, ФИО студента={self.student_name}, "
                f"размер стипендии={self.scholarship_amount}, куда выдается справка={self.destination})")


class ReportsCollection:
    def __init__(self):
        self.reports = []

    def __iter__(self):
        return iter(self.reports)

    def __getitem__(self, index):
        return self.reports[index]

    def __repr__(self):
        return f"ReportsCollection({len(self.reports)} reports)"

    @staticmethod
    def from_csv(filename):
        collection = ReportsCollection()
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                report = Report(
                    number=row['№'],
                    date=row['дата'],
                    student_name=row['ФИО студента'],
                    scholarship_amount=row['размер стипендии'],
                    destination=row['куда выдается справка']
                )
                collection.reports.append(report)
        return collection

    @staticmethod
    def to_csv(filename, collection):
        if collection.reports:
            fieldnames = ['№', 'дата', 'ФИО студента', 'размер стипендии', 'куда выдается справка']
            with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for report in collection:
                    writer.writerow({
                        '№': report.number,
                        'дата': report.date,
                        'ФИО студента': report.student_name,
                        'размер стипендии': report.scholarship_amount,
                        'куда выдается справка': report.destination
                    })

    def add_report(self, report):
        self.reports.append(report)

    def sort_by_string_field(self, field):
        self.reports.sort(key=lambda x: getattr(x, field))

    def sort_by_numeric_field(self, field):
        self.reports.sort(key=lambda x: getattr(x, field))

    def filter_by_criterion(self, field, value):
        return (report for report in self.reports if getattr(report, field) > value)


def create_example_csv(filename):
    data = [
        {'№': '1', 'дата': '2024-01-15', 'ФИО студента': 'Иванов Иван', 'размер стипендии': '12000',
         'куда выдается справка': 'Деканат'},
        {'№': '2', 'дата': '2024-02-20', 'ФИО студента': 'Петров Петр', 'размер стипендии': '8500',
         'куда выдается справка': 'Стипендиальный комитет'},
        {'№': '3', 'дата': '2024-03-10', 'ФИО студента': 'Сидоров Сидор', 'размер стипендии': '11000',
         'куда выдается справка': 'Бухгалтерия'}
    ]
    fieldnames = data[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    # Ввод директории для подсчета файлов
    directory = input("Введите путь к директории: ")
    file_count = len([entry for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry))])
    print(f"Количество файлов в директории: {file_count}")

    # Проверка наличия файла CSV, если его нет, создать пример
    csv_filename = input(
        "Введите полный путь к файлу CSV для чтения данных (например, C:\\Users\\legio\\data.csv): ").strip()
    if not os.path.exists(csv_filename):
        create_example_csv(csv_filename)
        print(f"Создан пример файла {csv_filename}")

    # Чтение данных из файла CSV
    reports = ReportsCollection.from_csv(csv_filename)

    # Сортировка данных по строковому полю (ФИО студента)
    reports.sort_by_string_field('student_name')
    print("Данные, отсортированные по ФИО студента:")
    for report in reports:
        print(report)

    # Сортировка данных по числовому полю (размер стипендии)
    reports.sort_by_numeric_field('scholarship_amount')
    print("Данные, отсортированные по размеру стипендии:")
    for report in reports:
        print(report)

    # Фильтрация данных по критерию (размер стипендии больше 10000)
    filtered_reports = reports.filter_by_criterion('scholarship_amount', 10000)
    print("Данные студентов с размером стипендии больше 10000:")
    for report in filtered_reports:
        print(report)

    # Добавление новых данных
    add_new_data = input("Хотите добавить новую справку? (да/нет): ").strip().lower()
    while add_new_data == 'да':
        number = input("Введите номер справки: ")
        date = input("Введите дату (гггг-мм-дд): ")
        student_name = input("Введите ФИО студента: ")
        scholarship_amount = input("Введите размер стипендии: ")
        destination = input("Введите место выдачи справки: ")
        new_report = Report(number, date, student_name, scholarship_amount, destination)
        reports.add_report(new_report)
        add_new_data = input("Хотите добавить еще одну справку? (да/нет): ").strip().lower()

    # Сохранение новых данных обратно в файл CSV
    save_csv_filename = input(
        "Введите полный путь к файлу CSV для сохранения данных (например, C:\\Users\\legio\\new_data.csv): ").strip()
    ReportsCollection.to_csv(save_csv_filename, reports)
    print(f"Данные сохранены в файл {save_csv_filename}")


if __name__ == "__main__":
    main()
