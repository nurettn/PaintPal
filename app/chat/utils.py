import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from chat.consumers import ChatConsumer


def broadcast_msg_to_chat(msg,
                          group_name,
                          event_type="update_playerlist"):
    channel_layer = get_channel_layer()
    broadcast_data = {
        'type': event_type,
        'message': msg
    }
    print("GROUP NAME ", group_name)
    async_to_sync(channel_layer.group_send)(group_name, broadcast_data)
