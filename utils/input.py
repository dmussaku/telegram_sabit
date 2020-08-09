from datetime import datetime
import json
import os


class Settings(object):

    def __init__(self, settings_file_path):
        self.settings_file_path = settings_file_path
        if not os.path.exists(settings_file_path):
            self._prefix = None
            self._keywords = None
            self._date_from = None
            self._date_to = None
            self.encoding = None
            self.save()
        else:
            with open(settings_file_path, 'r') as settings_file:
                settings_dict = json.loads(settings_file.read())

            self._prefix = settings_dict['prefix']
            self._keywords = settings_dict['keywords']
            self._date_from = (datetime.strptime(settings_dict['date_from'], '%d.%m.%Y').date()
                               if settings_dict['date_from'] else None)
            self._date_to = (datetime.strptime(settings_dict['date_to'], '%d.%m.%Y').date()
                             if settings_dict['date_to'] else None)
            self.encoding = settings_dict['encoding']

    def save(self):
        with open(self.settings_file_path, 'w') as settings_file:
            settings_file.write(json.dumps({
                'prefix': self.prefix if self.prefix else None,
                'keywords': self.keywords,
                'date_from': self.date_from.strftime('%d.%m.%Y') if self.date_from else None,
                'date_to': self.date_to.strftime('%d.%m.%Y') if self.date_to else None,
                'encoding': self.encoding if self.encoding else None,
            }))

    @property
    def as_string_list(self):
        return [
            self.prefix if self.prefix else "",
            ', '.join(self.keywords) if self.keywords else "",
            self.date_from.strftime('%d.%m.%Y') if self.date_from else "",
            self.date_to.strftime('%d.%m.%Y') if self.date_to else "",
            self.encoding if self.encoding else "",
        ]

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value: str):
        self._prefix = value
        self.save()

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value: str):
        self._keywords = [keyword.strip().lower()
                          for keyword in value.split(',')
                          if keyword]
        self.save()

    @property
    def date_from(self):
        return self._date_from

    @date_from.setter
    def date_from(self, value: str):
        self._date_from = datetime.strptime(value, '%d.%m.%Y').date()
        self.save()

    @property
    def date_to(self):
        return self._date_to

    @date_to.setter
    def date_to(self, value: str):
        self._date_to = datetime.strptime(value, '%d.%m.%Y').date()
        self.save()

    @property
    def encoding(self):
        return self._encoding

    @encoding.setter
    def encoding(self, value: str):
        self._encoding = None if value == "" else value
        self.save()


class InputSettings(object):
    prefix_num = 2
    prefix_label = 'Префикс: '
    keywords_num = 3
    keywords_label = 'Термины (ввод через запятую): '
    date_from_num = 4
    date_from_label = 'Дата начала (дд.мм.гггг): '
    date_to_num = 5
    date_to_label = 'Дата окончания (дд.мм.гггг): '
    encoding_num = 6
    encoding_label = 'Кодировка файла (utf8 или пустое значение): '

    def __init__(self, settings_file_path):
        self.settings = Settings(settings_file_path)

    def print_settings(self):
        print("")
        annotations = zip(
            (self.prefix_num, self.keywords_num,
             self.date_from_num, self.date_to_num, self.encoding_num),
            (self.prefix_label, self.keywords_label,
             self.date_from_label, self.date_to_label, self.encoding_label),
            self.settings.as_string_list,
        )
        for i, label, setting in annotations:
            print ('{0}) {1} {2} '.format(i, label, setting))

    def input_prefix(self):
        prefix = input(self.prefix_label).strip()
        if prefix in (None, ""):
            print('Поле не должно быть пустым ')
            self.input_prefix()

        self.settings.prefix = prefix

    def input_keywords(self):
        keywords = input(self.keywords_label).strip()
        if keywords in (None, ""):
            print('Поле не должно быть пустым ')
            self.input_keywords()

        self.settings.keywords = keywords

    def input_date_from(self):
        date_from = input(self.date_from_label).strip()
        if date_from in (None, ""):
            print('Поле не должно быть пустым ')
            self.input_date_from()

        try:
            self.settings.date_from = date_from
        except ValueError:
            print('Неверный формат ')
            self.input_date_from()

    def input_date_to(self):
        date_to = input(self.date_to_label).strip()
        if date_to in (None, ""):
            print('Поле не должно быть пустым ')
            self.input_date_to()

        try:
            self.settings.date_to = date_to
        except ValueError:
            print('Неверный формат ')
            self.input_date_to()

    def input_encoding(self):
        encoding = input(self.encoding_label).strip()
        if encoding not in ("utf8", ""):
            print('Допустимы только: utf8 или пустое значение')
            self.input_encoding()

        self.settings.encoding = encoding

    def input_setting(self):
        print (
            """\n"""
            """Нажмите enter для запуска\n"""
            """введите list для показа текущих настроек, """
            """или номер параметра для изменения"""
        )
        value = input()

        if value == "":
            if not all((self.settings.prefix,
                        self.settings.keywords,
                        self.settings.date_from,
                        self.settings.date_to)):
                print(" Не все настройки были введены ")
                self.input_setting()
            return
        elif value == "list":
            self.print_settings()
        elif value == '2':
            self.input_prefix()
        elif value == '3':
            self.input_keywords()
        elif value == '4':
            self.input_date_from()
        elif value == '5':
            self.input_date_to()
        elif value == '6':
            self.input_encoding()
        else:
            print(" Неккоректный ввод ")

        self.input_setting()
