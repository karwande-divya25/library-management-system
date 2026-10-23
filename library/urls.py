# from rest_framework.routers import DefaultRouter
# from .views import BookViewSet, MemberViewSet, IssueViewSet

# router = DefaultRouter()
# router.register("books", BookViewSet)
# router.register("members", MemberViewSet)
# router.register("issues", IssueViewSet)

# urlpatterns = router.urls

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (BookViewSet, MemberViewSet, IssueViewSet,
                    OverdueReport, PopularBooksReport, TopMembersReport)

router = DefaultRouter()
router.register("books", BookViewSet)
router.register("members", MemberViewSet)
router.register("issues", IssueViewSet)

urlpatterns = [
    path("reports/overdue/", OverdueReport.as_view()),
    path("reports/popular-books/", PopularBooksReport.as_view()),
    path("reports/top-members/", TopMembersReport.as_view()),
] + router.urls