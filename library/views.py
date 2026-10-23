# from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from . import sql_reports
from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Book, Member, Issue, Fine
from .serializers import BookSerializer, MemberSerializer, IssueSerializer

FINE_PER_DAY = Decimal("5.00")


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["category", "author"]
    search_fields = ["title", "author"]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        book = serializer.validated_data["book"]
        if book.available_copies < 1:
            raise serializers.ValidationError("Book not available")
        book.available_copies -= 1
        book.save()
        serializer.save(due_date=timezone.localdate() + timedelta(days=14))

    @action(detail=True, methods=["post"], url_path="return")
    @transaction.atomic
    def return_book(self, request, pk=None):
        issue = self.get_object()
        if issue.return_date:
            return Response({"error": "Already returned"}, status=400)

        today = timezone.localdate()
        issue.return_date = today
        issue.save()

        issue.book.available_copies += 1
        issue.book.save()

        late_days = (today - issue.due_date).days
        fine_amount = Decimal("0.00")
        if late_days > 0:
            fine_amount = late_days * FINE_PER_DAY
            Fine.objects.create(issue=issue, amount=fine_amount)

        return Response({"late_days": max(late_days, 0), "fine": fine_amount})
    
    
class OverdueReport(APIView):
    def get(self, request):
        return Response(sql_reports.overdue_books())


class PopularBooksReport(APIView):
    def get(self, request):
        return Response(sql_reports.popular_books())


class TopMembersReport(APIView):
    def get(self, request):
        return Response(sql_reports.top_members()) 