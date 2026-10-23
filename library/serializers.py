from rest_framework import serializers
from .models import Book, Member, Issue, Fine


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"
        read_only_fields = ["issue_date", "due_date", "return_date"]


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = "__all__"