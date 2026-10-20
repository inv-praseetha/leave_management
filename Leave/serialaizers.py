from rest_framework import serializers
from Leave.models import LeaveRequest
class LeaveRequestSerialaizer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'reason','total_days','id','status']
        
    def validate_status(self, value):
        if value not in LeaveRequest.Status.values:
            raise serializers.ValidationError("Invalid status")
        return value