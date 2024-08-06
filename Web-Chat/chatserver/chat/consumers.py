import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import os

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope['user'].username

        self.write_to_log_file(username, message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    def chat_message(self, event):
        message = event['message']
        username = event['username']

        self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    def write_to_log_file(self, username, message):
        log_dir = os.path.join('logs', self.room_name)
        os.makedirs(log_dir, exist_ok=True)

        log_file_path = os.path.join(log_dir, f'{self.room_name}.log')

        with open(log_file_path, 'a') as log_file:
            log_file.write(f'{username}: {message}\n')
