# websockets/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .tracking import UserTracker
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    """ChatConsumer is a class that faciliates Websocket communication between the server and clients"""
    userTrack = UserTracker()
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': self.scope
        #     }
        # )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        event = text_data_json['event']
        if event == 'JOIN':
            user_name = text_data_json['user_name']
            message = text_data_json['message']
            self.userTrack.add_user(user_name)
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'event': 'JOIN',
                    'user_name': user_name,
                    'connected_users': self.userTrack.get_connected_users()
                }
            )

        if event == 'LEAVE':
            message = text_data_json['message']
            user_name = text_data_json['user_name']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'event': 'LEAVE',
                    'user_name': user_name
                }
            )

        if event == 'SEND':
            message = text_data_json['message']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'event': 'SEND',
                    'message': message
                }
            )
        
        if event == 'SPIN':
            category = text_data_json['category']
            id = text_data_json['id']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'event': 'SPIN',
                    'category': category,
                    'id': id
                }
            )
        
        if event == 'CHOOSE':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'event': 'CHOOSE',
                    'question': text_data_json['question'],
                    'choices': text_data_json['choices'],
                    'correct_answer': text_data_json['correct_answer'],
                    'question_id': text_data_json['question_id']
                }
            )
        
        if event == 'ANSWER':
            logger.debug('Got an Answer')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'event': 'ANSWER',
                    'message': text_data_json['message'],
                    'user_choice': text_data_json['userChoice']
                }
            )
        
        if event == 'BUZZ':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'event': 'BUZZ',
                    'player': text_data_json['player'],
                    'time': text_data_json['time']
                }
            )
        
        if event == 'START':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'event': 'START'
                }
            )
        # if event == 'UPDATE_TABLE':
        #     users = self.userTrack.get_connected_users()
        #     await self.channel_layer.group_send(
        #         self.room_group_name,
        #         {
        #             'type': 'chat_message',
        #             'event': 'UPDATE_TABLE',
        #             'connected_users' : users
        #         }
        #     )


    # Receive message from room group
    async def chat_message(self, res):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "payload": res,
        }))