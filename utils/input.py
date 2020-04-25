from datetime import datetime
import json
import os


settings_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'settings.json'
)


class Settings(object):

    def __init__(self):
        if not os.path.exists(settings_file_path):
            self._chat_name = None
            self._prefix = None
            self._keywords = None
            self._date_from = None
            self._date_to = None
            self.encoding = None
            self.save()
        else:
            with open(settings_file_path, 'r') as settings_file:
                settings_dict = json.loads(settings_file.read())

            self._chat_name = settings_dict['chat_name']
            self._prefix = settings_dict['prefix']
            self._keywords = settings_dict['keywords']
            self._date_from = (datetime.strptime(settings_dict['date_from'], '%d.%m.%Y').date()
                               if settings_dict['date_from'] else None)
            self._date_to = (datetime.strptime(settings_dict['date_to'], '%d.%m.%Y').date()
                             if settings_dict['date_to'] else None)
            self.encoding = settings_dict['encoding']

    def save(self):
        with open(settings_file_path, 'w') as settings_file:
            settings_file.write(json.dumps({
                'chat_name': self.chat_name if self.chat_name else None,
                'prefix': self.prefix if self.prefix else None,
                'keywords': self.keywords,
                'date_from': self.date_from.strftime('%d.%m.%Y') if self.date_from else None,
                'date_to': self.date_to.strftime('%d.%m.%Y') if self.date_to else None,
                'encoding': self.encoding if self.encoding else None,
            }))

    @property
    def as_string_list(self):
        return [
            self.chat_name if self.chat_name else "",
            self.prefix if self.prefix else "",
            ', '.join(self.keywords) if self.keywords else "",
            self.date_from.strftime('%d.%m.%Y') if self.date_from else "",
            self.date_to.strftime('%d.%m.%Y') if self.date_to else "",
            self.encoding if self.encoding else "",
        ]

    @property
    def chat_name(self):
        return self._chat_name

    @chat_name.setter
    def chat_name(self, value: str):
        self._chat_name = value
        self.save()

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
        self._encoding = value
        self.save()


class InputSettings(object):
    settings = Settings()
    chat_name_num = 1
    chat_name_label = 'Название Чата: '
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

    @classmethod
    def print_settings(cls):
        print("")
        annotations = zip(
            (cls.chat_name_num, cls.prefix_num, cls.keywords_num,
             cls.date_from_num, cls.date_to_num, cls.encoding_num),
            (cls.chat_name_label, cls.prefix_label, cls.keywords_label,
             cls.date_from_label, cls.date_to_label, cls.encoding_label),
            cls.settings.as_string_list,
        )
        for i, label, setting in annotations:
            print ('{0}) {1} {2} '.format(i, label, setting))

    @classmethod
    def input_chat_name(cls):
        chat_name = input(cls.chat_name_label).strip()
        if chat_name in (None, ""):
            print('Поле не должно быть пустым ')
            cls.input_chat_name()

        cls.settings.chat_name = chat_name

    @classmethod
    def input_prefix(cls):
        prefix = input(cls.prefix_label).strip()
        if prefix in (None, ""):
            print('Поле не должно быть пустым ')
            cls.input_prefix()

        cls.settings.prefix = prefix

    @classmethod
    def input_keywords(cls):
        keywords = input(cls.keywords_label).strip()
        if keywords in (None, ""):
            print('Поле не должно быть пустым ')
            cls.input_keywords()

        cls.settings.keywords = keywords

    @classmethod
    def input_date_from(cls):
        date_from = input(cls.date_from_label).strip()
        if date_from in (None, ""):
            print('Поле не должно быть пустым ')
            cls.input_date_from()

        try:
            cls.settings.date_from = date_from
        except ValueError:
            print('Неверный формат ')
            cls.input_date_from()

    @classmethod
    def input_date_to(cls):
        date_to = input(cls.date_to_label).strip()
        if date_to in (None, ""):
            print('Поле не должно быть пустым ')
            cls.input_date_to()

        try:
            cls.settings.date_to = date_to
        except ValueError:
            print('Неверный формат ')
            cls.input_date_to()

    @classmethod
    def input_encoding(cls):
        encoding = input(cls.encoding_label).strip()
        if encoding not in ("utf8", ""):
            print('Допустимы только: utf8 или пустое значение')
            cls.input_encoding()

        cls.settings.ecnoding = encoding

    @classmethod
    def input_setting(cls):
        print (
            """\n"""
            """Нажмите enter для запуска\n"""
            """введите list для показа текущих настроек, """
            """или номер параметра для изменения"""
        )
        value = input()

        if value == "":
            if not all((cls.settings.chat_name,
                        cls.settings.prefix,
                        cls.settings.keywords,
                        cls.settings.date_from,
                        cls.settings.date_to)):
                print(" Не все настройки были введены ")
                cls.input_setting()
            return
        elif value == "list":
            cls.print_settings()
        elif value == '1':
            cls.input_chat_name()
        elif value == '2':
            cls.input_prefix()
        elif value == '3':
            cls.input_keywords()
        elif value == '4':
            cls.input_date_from()
        elif value == '5':
            cls.input_date_to()
        elif value == '6':
            cls.input_encoding()
        else:
            print(" Неккоректный ввод ")

        cls.input_setting()
