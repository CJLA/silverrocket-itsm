from rest_framework import viewsets

from .models import Ticket
from .serializers import TicketDetailSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("created_by", "assigned_to").order_by(
        "-created_at"
    )
    serializer_class = TicketDetailSerializer
    lookup_field = "display_id"

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
