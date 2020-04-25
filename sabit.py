import csv
import json
import os
import traceback
from datetime import datetime
from pprint import pprint


def parse_telegram_file(filename: str):
    with open(filename, 'r', encoding="utf8") as myfile:
        contents = json.loads(myfile.read())

    return contents


def get_chat_messages(contents: dict,
                      chat_name: str,
                      from_datetime: datetime,
                      to_datetime: datetime):
    chat = next(
        filter(
            lambda x: x['name'].lower() == chat_name,
            contents['chats']['list']
        ), None
    )
    if chat:
        return list(filter(
            lambda x: from_datetime < datetime.fromisoformat(x['date']) < to_datetime,
            chat['messages']
        ))

    return []


def get_message_statistics(messages: list, keywords: list, prefix: str='KC:'):
    def is_a_user_text_message(obj):
        if (obj['type'] == 'message' and
                'from' in obj and
                'text' in obj and
                type(obj['text']) == str):
            return True
        return False

    # {<username1>: {<date1>: [1, 2, 3], <date2>: [4,5]}}
    user_date_message_ids = {}

    # store all main messages ids
    main_messages_ids = []

    for message in filter(is_a_user_text_message, messages):
        message_text = message['text']
        if message_text.lower().strip().startswith(prefix.lower()):
            username = message['from']
            date = datetime.fromisoformat(message['date']).date()
            message_id = message['id']
            if username not in user_date_message_ids:
                user_date_message_ids[username] = {date: [message_id]}
            else:
                if date not in user_date_message_ids[username]:
                    user_date_message_ids[username][date] = [message_id]
                else:
                    user_date_message_ids[username][date].append(message_id)
            main_messages_ids.append(message_id)

    # {1: {'keyword1': 3, 'keyword2': 4, 'keyword3': 5}}
    answer_count_dict = {_id: {keyword.lower(): 0 for keyword in keywords}
                         for _id in main_messages_ids}

    for message in filter(lambda x: 'reply_to_message_id' in x,
                          filter(is_a_user_text_message, messages)):

        message_text = message['text'].lower().strip()
        reply_to_message_id = message['reply_to_message_id']
        if (reply_to_message_id in main_messages_ids and
                message_text in keywords):
            answer_count_dict[reply_to_message_id][message_text] += 1

    # of type
    # {<username1>: {<date1>: {'count': 100, 'keywords': {'keyword1': 30}}}}
    result = {}
    for username, data in user_date_message_ids.items():
        result[username] = {}
        for date, ids in data.items():
            data_per_keyword = [value for key, value in answer_count_dict.items()
                                if key in ids]
            accumulated = {key: sum(item[key] for item in data_per_keyword)
                           for key in keywords}
            result[username][date] = {
                'count': len(ids),
                'keywords': accumulated
            }

    return result


def create_csv_from_result(accumulated_result: dict,
                           keywords: list):
    # expect accumulated result of type
    # {<username1>: {<date1>: {'count': 100, 'keywords': {'keyword1': 30}}}}
    file_path = os.path.join(os.getcwd(), 'statistics.csv')
    with open(file_path, 'w', encoding='utf8', newline='') as csvfile:
        fieldnames = ['date', 'user', 'count'] + keywords
        writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
        writer.writeheader()
        for user, data_per_date in accumulated_result.items():
            for date, result in data_per_date.items():
                row = result['keywords']
                row['count'] = result['count']
                row['date'] = date
                row['user'] = user
                writer.writerow(row)


def get_inputs():
    chat_name = input("Введите название чата: ")
    if not chat_name:
        raise Exception("Чат не был введен, перезапустите программу")
        input()
    chat_name = chat_name.lower()

    prefix = input("Введите префикс ('КС': по умолчанию): ") or 'КС:'
    keywords_input = input("Введите ключевые ответы разделенные запятой: ")
    if keywords_input is None:
        keywords = list(map(lambda x: x.lower(), ['Идем', 'Бежим', 'Едем']))
    else:
        keywords = [keyword.strip().lower() for keyword in keywords_input.split(',')]

    from_datetime = input("Введите дату начала (дд-мм-гггг): ")
    try:
        from_datetime = datetime.strptime(from_datetime, '%d-%m-%Y')
    except:
        raise Exception("Неправильно введенная дата")

    to_datetime = input("Введите дату окончания (дд-мм-гггг): ")
    try:
        to_datetime = datetime.strptime(to_datetime, '%d-%m-%Y')
    except:
        raise Exception("Неправильно введенная дата")

    return chat_name, prefix, keywords, from_datetime, to_datetime


if __name__ == '__main__':
    print(
        "Удостоверьтесь что export telegram чата находится в той же директории что и этот скрипт"
        "Файл должен называться results.json"
    )
    print("Нажмите Enter для продолжения")
    input()

    try:
        chat_name, prefix, keywords, from_datetime, to_datetime = get_inputs()
        filename = 'result.json'

        contents = parse_telegram_file(filename)
        chat_messages = get_chat_messages(contents, chat_name, from_datetime, to_datetime)
        accumulated_result = get_message_statistics(chat_messages, keywords, prefix)
        create_csv_from_result(accumulated_result, keywords)

        print("Файл statistics.csv был создан в текущей дериктории")
        print("Нажмите Enter для завершения")
        input()
    except Exception:
        print(traceback.format_exc())
        input()
