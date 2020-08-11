import csv
import json
import os
from datetime import datetime
import traceback


def is_a_user_text_message(obj):
    if (obj['type'] == 'message' and
            'from' in obj and
            'text' in obj):
        return True
    return False


class TelegramParser(object):
    def __init__(self, telegram_filepath: str):
        self.telegram_filepath = telegram_filepath

    def get_file_contents(self):
        with open(self.telegram_filepath, 'r', encoding="utf8") as myfile:
            contents = json.loads(myfile.read())

        return contents

    @staticmethod
    def get_chat_messages(contents: dict,
                          from_datetime: datetime,
                          to_datetime: datetime):
        chat = contents

        messages = list(filter(
            lambda x: from_datetime <= datetime.fromisoformat(x['date']).date() <= to_datetime,
            chat['messages']
        ))

        if not messages:
            raise Exception(
                "Нет сообщений за текущий период: {:%d.%m.%Y} - {:%d.%m.%Y}".format(
                    from_datetime, to_datetime
                )
            )

        return messages

    @staticmethod
    def get_message_text(message_struct: dict):
        message_text = message_struct['text']
        if type(message_text) in (str, bytes):
            pass
        elif type(message_text) == list:
            message_text = message_text[0]
        else:
            message_text = ""
        if type(message_text) != str:
            raise AttributeError(f'{message_text} is not a string. Cant use lower method on it')

        return message_text.lower().strip()

    @classmethod
    def get_message_statistics(cls, messages: list, keywords: list, prefix: str):
        # {<username1>: {<date1>: [1, 2, 3], <date2>: [4,5]}}
        user_date_message_ids = {}

        # store all main messages ids
        main_messages_ids = []

        for message in filter(is_a_user_text_message, messages):
            message_text = cls.get_message_text(message)
            if message_text.startswith(prefix.lower()):
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

    def get_accumulated_statistics(self,
                                   prefix: str,
                                   keywords: str,
                                   date_from: datetime,
                                   date_to: datetime):
        file_contents = self.get_file_contents()
        chat_messages = self.get_chat_messages(file_contents, date_from, date_to)
        statistic = self.get_message_statistics(chat_messages, keywords, prefix)

        return statistic


class StatisticsWriter(object):

    def create_csv_from_result(accumulated_result: dict,
                               keywords: list,
                               encoding: str=None):
        # expect accumulated result of type
        # {<username1>: {<date1>: {'count': 100, 'keywords': {'keyword1': 30}}}}
        file_path = os.path.join(os.getcwd(), 'statistics.csv')
        with open(file_path, 'w', encoding=encoding, newline='') as csvfile:
            fieldnames = ['date', 'user', 'count'] + keywords
            writer = csv.DictWriter(csvfile, delimiter=";", fieldnames=fieldnames)
            # writer.writeheader()
            for user, data_per_date in accumulated_result.items():
                for date, result in data_per_date.items():
                    row = result['keywords']
                    row['count'] = result['count']
                    row['date'] = date.strftime('%d.%m.%Y')
                    row['user'] = user
                    writer.writerow(row)
