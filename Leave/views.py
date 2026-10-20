
from app.permission import IsEmployee,IsManager
from rest_framework.views import APIView
from .models import LeaveBalance,LeaveRequest
from rest_framework.response import Response
from rest_framework import status
from .serialaizers import LeaveRequestSerialaizer
from .service import LeaveService
from django.core.exceptions import ValidationError
# Create your views here.
class LeaveCreationAPIView(APIView):
    permission_classes=[IsEmployee]
    def post(self,request):
        id=request.user
        print(id)
        type=request.data.get("leave_type")
        if type not in LeaveRequest.LeaveType:
            return Response({"message":f"invalid {type} leave type please enter a valid leave type"},status=status.HTTP_400_BAD_REQUEST)
        print("type",type)
        data=LeaveBalance.objects.filter(employee=id).first()
        if not data:
            return Response({"message":f"the employee have no{type} leaves"},status=status.HTTP_200_OK)
        data=LeaveRequestSerialaizer(data=request.data)
        if data.is_valid():
            try:
                leave=LeaveService.create_leave(validated_data=data.validated_data,employee=request.user)
                response=LeaveRequestSerialaizer(leave)
                return Response(response.data,status=status.HTTP_201_CREATED)  
            except ValidationError as e:
                return Response(e.error_dict,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        data=LeaveRequest.objects.filter(employee=request.user)
        print("data is",data)
        if not data:
            return Response({"message":"no leave requests the corresponding manager"},status=status.HTTP_404_NOT_FOUND) 
        statuss=request.query_params.get("status")
        if statuss:
            data=data.filter(status=statuss)
        else:
            data=data.order_by("-id")
        
        serailizer=LeaveRequestSerialaizer(data,many=True)
        print("serailizer is",serailizer.data)
        return Response(serailizer.data,status=status.HTTP_200_OK)
        
class ManagerLeaveApprovalView(APIView):
    permission_classes=[IsManager]
    def get(self,request):
        data=LeaveRequest.objects.filter(employee__manager_id=request.user)
        if not data:
            return Response({"message":"no leave requests the corresponding manager"},status=status.HTTP_404_NOT_FOUND) 
        status=request.query_params.get("status")
        if status:
            data=data.filter(status=status)
        data=data.order_by("-id")
        serailizer=LeaveRequestSerialaizer(data,many=True)
        return Response(serailizer.data,status=status.HTTP_200_OK)
    # def patch(self,request,id):
    #     id=request.data.get("id")
    #     leave_id=LeaveRequest.objects.filter(id=id)
    #     if not leave_id:
    #         return Response({"message":"request not found"},status=status.HTTP_404_NOT_FOUND)   
    #     data=LeaveRequest.objects.get(employee__manager_id=request.user,id=id)
    #     if not data:
    #         return Response({"message":"you have no permission approve this leave request"},status=status.HTTP_404_NOT_FOUND) 
    #     try:
    #         accept=LeaveService.accept_leave(employee=request.user,validated_data=data.validated_data)
    #     # data.status=request.data.get("status")
    #     # # data.approved_date=timezone.now()
    #     # data.approved_by=request.user
    #     # data.save()
    #     except ValidationError as e:
    #             return Response(e.error_dict,status=status.HTTP_400_BAD_REQUEST)
    #     return Response(LeaveRequestSerialaizer(data).data,status=status.HTTP_200_OK)
        
    
    def patch(self, request, id):
    # 1. Find the leave request and check manager permission
        try:
            leave = LeaveRequest.objects.get(
                employee__manager_id=request.user,
                id=id,
            )
        except LeaveRequest.DoesNotExist:
            return Response(
                {"message": "Leave request not found or you have no permission"},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Validate the request data
        serializer = LeaveRequestSerialaizer(
            leave,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        print("....,,,,,",serializer.validated_data)

        # 3. Pass validated data to service
        try:
            updated_leave = LeaveService.accept_leave(
                employee=request.user,
                validated_data=serializer.validated_data,
                leave_id=leave.id
            )
        except ValidationError as e:
            return Response(
                e.error_dict,
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Return updated leave
        return Response(
            LeaveRequestSerialaizer(updated_leave).data,
            status=status.HTTP_200_OK
        )
class LeaveHistory(APIView):
    permission_classes=[IsManager]
    def get(self,request,id):
        try:
            data=LeaveRequest.objects.filter(employee__manager_id=request.user,employee=id,status=LeaveRequest.Status.APPROVED)
            if not data:
                return Response({"message":"you have no permission to view this leave request"},status=status.HTTP_404_NOT_FOUND)    
            data=LeaveRequestSerialaizer(data,many=True)
            return Response(data.data,status=status.HTTP_200_OK)
        except LeaveRequest.DoesNotExist:
            return Response({"message":"leave request not found"},status=status.HTTP_404_NOT_FOUND)
