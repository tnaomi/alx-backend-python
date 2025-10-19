from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.
    """
    queryset = Conversation.objects.all().prefetch_related('participants')
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation between users.
        Expected payload:
        {
            "participant_ids": [<user_id_1>, <user_id_2>, ...]
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(self.get_serializer(conversation).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Retrieve all messages in a specific conversation.
        """
        conversation = self.get_object()
        messages = Message.objects.filter(
            sender__in=conversation.participants.all(),
            receiver__in=conversation.participants.all()
        ).order_by('sent_at')

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    """
    queryset = Message.objects.all().select_related('sender', 'receiver')
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message between users.
        Expected payload:
        {
            "sender_id": "<user_id>",
            "receiver_id": "<user_id>",
            "message_body": "Hello!"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(self.get_serializer(message).data, status=status.HTTP_201_CREATED)
