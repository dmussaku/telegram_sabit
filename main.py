import os
import traceback

from utils.input import InputSettings
from utils.parser import TelegramParser, StatisticsWriter


telegram_filepath = os.path.join(os.getcwd(), 'result.json')


if __name__ == '__main__':
    if not os.path.exists(telegram_filepath):
        print(
            "\033[91m Файл result.json не найден \n"
            "Удостоверьтесь что export telegram чата находится в той же директории что и этот скрипт.\033[0m"
        )
        input("Нажмите enter для выхода\n")
    else:
        try:
            InputSettings.input_setting()
            telegram_parser = TelegramParser(telegram_filepath)
            accumulated_statistics = telegram_parser.get_accumulated_statistics(
                InputSettings.settings.chat_name,
                InputSettings.settings.prefix,
                InputSettings.settings.keywords,
                InputSettings.settings.date_from,
                InputSettings.settings.date_to,
            )
            StatisticsWriter.create_csv_from_result(
                accumulated_statistics,
                InputSettings.settings.keywords
            )

            print("Файл statistics.csv был создан в текущей дериктории")
            print("Нажмите Enter для завершения")
            input()
        except Exception:
            print(traceback.format_exc())
            input()
