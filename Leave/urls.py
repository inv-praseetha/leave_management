from Leave.views import LeaveCreationAPIView,ManagerLeaveApprovalView,LeaveHistory
from django.contrib import admin
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('create/',LeaveCreationAPIView.as_view()),
    path('list/request/',ManagerLeaveApprovalView.as_view()),
    path('edit/status/<int:id>/',ManagerLeaveApprovalView.as_view()),
    path('history/<int:id>/',LeaveHistory.as_view()),

]
