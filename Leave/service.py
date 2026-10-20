from django.core.exceptions import ValidationError
from .models import LeaveBalance,LeaveRequest
from django.db.models import Q
from django.utils import timezone
class LeaveService:
    @staticmethod
    def create_leave(validated_data,employee):
        
        current_date=timezone.localdate()
        start_date=validated_data.get('start_date')
        end_date=validated_data.get('end_date')
        # type=validated_data.get("leave_type")
        # print(type)
        # if type not in LeaveRequest.LeaveType:
        #     return Response({"message":f"invalid {type} leave type please enter a valid leave type"},status=status.HTTP_400_BAD_REQUEST)
        # print("type",type)
        # data=LeaveBalance.objects.filter(employee=employee).first()
        # if not data:
        #     return Response({"message":f"the employee have no{type} leaves"},status=status.HTTP_200_OK)
        if start_date<current_date or end_date<current_date:
            raise ValidationError({"message":"you can not apply for leave for past dates"})
        elif start_date>end_date:
            raise ValidationError({"message":"start date should be before end date"})
        # check_leave_request=LeaveRequest.objects.filter(employee=employee,start_date=validated_data.get('start_date'),end_date=validated_data.get('end_date')).first()
        check_leave_request = LeaveRequest.objects.filter(Q(employee=employee, start_date=validated_data.get('start_date')) | Q(employee=employee, end_date=validated_data.get('end_date'))).exclude(status=LeaveRequest.Status.REJECTED).first()
        print("check_leave_request",check_leave_request)
        if check_leave_request:
            raise ValidationError({"message":f"you have already applied leave for this dates {validated_data.get('start_date')} to {validated_data.get('end_date')}  please chnage the dates"})
    
        
        
        
        else:
      
        
            validated_data['total_days']=(validated_data.get('end_date')-validated_data.get('start_date')).days+1
            days=validated_data['total_days']
            balance_check=LeaveBalance.objects.filter(employee=employee,leave_type=validated_data.get('leave_type')).first()
            if not balance_check:
                raise ValidationError({"message":f"you have no {validated_data.get('leave_type')} leaves"})
            elif balance_check.available_balance<=days:
                raise ValidationError({"message":"you do not have sufficient balance"})
            else:
                leave = LeaveRequest.objects.create(
                    employee=employee,
                    **validated_data
                )
            # balance=LeaveBalance.objects.filter(employee=employee,leave_type=validated_data.get('leave_type')).first()
            # print("balance",balance)
            # balance.available_balance-=validated_data.get('total_days'
            # print("balance.available_balance",balance.available_balance)
            # balance.save()
        

            return leave
    # def accept_leave(validated_data,employee):




    def accept_leave(validated_data, employee, leave_id):

        # 1. Get status from request data
        status_value = validated_data.get("status")

        if status_value not in LeaveRequest.Status.values:
            raise ValidationError({"message": "Invalid status"})
            if status_value ==  LeaveRequest.Status.REJECTED:
                raise ValidationError({"message": "Leave already rejected so you cant approve this leave"})
                if status_value ==  LeaveRequest.Status.APPROVED:
                    raise ValidationError({"message": "Leave already approved"})

        # 2. Fetch the existing leave request using ID
        leave = LeaveRequest.objects.select_for_update().filter(
            id=leave_id,
            employee__manager_id=employee
        ).first()

        if leave is None:
            raise ValidationError({"message": "Leave request not found"})

        if leave.status == status_value:
            raise ValidationError({"message": "Leave already approved"})

        # 3. Get total_days and leave_type from database
        total_days = leave.total_days
        leave_type = leave.leave_type
        leave_employee = leave.employee

        # 4. Deduct balance only when approving
        if status_value == LeaveRequest.Status.APPROVED:

            balance = LeaveBalance.objects.select_for_update().filter(
                employee=leave_employee,
                leave_type=leave_type
            ).first()

            if balance is None:
                raise ValidationError({"message": "Leave balance not found"})

            if balance.available_balance < total_days:
                raise ValidationError({"message": "Insufficient leave balance"})

            balance.available_balance -= total_days
            balance.save(update_fields=["available_balance"])
        elif status_value== LeaveRequest.Status.REJECTED:
            if leave.status==LeaveRequest.Status.APPROVED:
                balance = LeaveBalance.objects.filter(
                    employee=leave_employee,
                    leave_type=leave_type
                ).first()
                
                balance.available_balance += total_days
                balance.save(update_fields=["available_balance"])
                
                

        # 5. Update the leave request
        leave.status = status_value
        leave.approved_by = employee
        leave.approved_date = timezone.now()
        leave.save()

        return leave
        # status=validated_data.get("status")
        # print(".....",status)
        # if status not in LeaveRequest.Status:
        #     raise ValidationError({"message":"invalid status"})
        # validated_data['status']=status
        # validated_data['approved_date']=timezone.now()
        # validated_data['approved_by']=employee
        # LeaveRequest.objects.filter(id=validated_data.get("id")).update(**validated_data)
        # balance=LeaveBalance.objects.filter(employee=employee,leave_type=validated_data.get('leave_type')).first()
        # balance.available_balance-=validated_data.get('total_days')
        # balance.save()
        
        # return LeaveRequest.objects.get(id=validated_data.get("id"))
