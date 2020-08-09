import os
import traceback

from utils.input import InputSettings
from utils.parser import TelegramParser, StatisticsWriter


telegram_filepath = os.path.join(os.getcwd(), 'result.json')
settings_file_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'settings.json'
)


if __name__ == '__main__':
    if not os.path.exists(telegram_filepath):
        print(
            "Файл result.json не найден \n"
            "Удостоверьтесь что export telegram чата находится в той же директории что и этот скрипт."
        )
        input("Нажмите enter для выхода\n")
    else:
        try:
            input_settings = InputSettings(settings_file_path)
            input_settings.print_settings()
            input_settings.input_setting()
            telegram_parser = TelegramParser(telegram_filepath)
            accumulated_statistics = telegram_parser.get_accumulated_statistics(
                input_settings.settings.prefix,
                input_settings.settings.keywords,
                input_settings.settings.date_from,
                input_settings.settings.date_to,
            )
            StatisticsWriter.create_csv_from_result(
                accumulated_statistics,
                input_settings.settings.keywords,
                input_settings.settings.encoding,
            )

            print("Файл statistics.csv был создан в текущей дериктории")
            print("Нажмите Enter для завершения")
            input()
        except Exception:
            print(traceback.format_exc())
            input()
