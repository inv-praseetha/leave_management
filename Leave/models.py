from django.db import models


class LeaveRequest(models.Model):
    class LeaveType(models.TextChoices):
      CASUAL="CASUAL","casual"
      SICKNESS="SICKNESS","sickness"
      EARNED="EARNED","earned"
    class Status(models.TextChoices):
      PENDING="PENDING","pending"
      APPROVED="APPROVED","approved"
      REJECTED="REJECTED","rejected"
    employee=models.ForeignKey('app.User',on_delete=models.SET_NULL,null=True,related_name='employee')
    start_date=models.DateField()
    end_date=models.DateField()
    leave_type=models.CharField(max_length=100,choices=LeaveType.choices)
    status=models.CharField(max_length=100,choices=Status.choices,default=Status.PENDING,error_messages={
        "invalid_choice": "Invalid status"
    })
    total_days=models.IntegerField(null=True,blank=True)
    reason=models.TextField()
    applied_date=models.DateTimeField(auto_now_add=True)
    approved_by=models.ForeignKey('app.User',on_delete=models.SET_NULL,null=True,related_name='approved_by')
    approved_date=models.DateTimeField(null=True,blank=True)
    rejection_reason=models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.employee.employee_name
class LeaveBalance(models.Model):
    employee=models.ForeignKey('app.User',on_delete=models.SET_NULL,null=True)
    leave_type=models.CharField(max_length=100,choices=LeaveRequest.LeaveType.choices)
    available_balance=models.IntegerField()
    totally_available=models.IntegerField()
    year=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    
    