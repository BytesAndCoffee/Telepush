from dataclasses import dataclass


@dataclass
class Chat:
    first_name: str
    id: int
    last_name: str
    type: str
    username: str


@dataclass
class User:
    first_name: str
    id: int
    is_bot: bool
    language_code: str
    last_name: str
    username: str


@dataclass
class Message:
    chat: Chat
    date: int
    user: User
    message_id: int
    update_id: int
    text: str


def consume(message: dict, update_id: int) -> Message:
    chat = Chat(**message['chat'])
    message['from'].pop('is_premium', None)
    user = User(**message['from'])
    return Message(
        chat,
        message['date'],
        user,
        message['message_id'],
        update_id,
        message['text']
    )


if __name__ == '__main__':
    import requests
    import config

    url = f'https://api.telegram.org/bot{config.token}/getUpdates'
    res = requests.post(url).json()

    messages: list = []
    for msg in res['result']:
        messages.append(consume(msg['message'], msg['update_id']))
        print(messages[-1].text)
