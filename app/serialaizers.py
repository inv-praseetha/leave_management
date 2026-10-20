
from rest_framework import serializers
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator
from .models import User
class UserSerialaizer(serializers.ModelSerializer):

    email = serializers.EmailField(
    required=True,
    validators=[
        UniqueValidator(
            queryset=User.objects.all(),
            message="A user with this email already exists."
        )
    ]
)
    password=serializers.CharField(write_only=True, validators=[
            RegexValidator(
                regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
                message="Password must contain at least 8 characters, one uppercase, one lowercase, one digit, and one special character."
            )
        ])
    employee_name=serializers.CharField(
        validators=[
            RegexValidator(r'^[a-zA-Z ]+$',message="Employee name should only contain alphabets and spaces"),
            UniqueValidator(queryset=User.objects.all(),message="Employee name already exists")
        ]
    )
        
    class Meta:
        model = User
        fields = ['employee_name','email', 'password','role','departmet','joining_date','emp_id','manager_id']
        
      
       
    def create(self,validated_data):
        # import pdb
        # pdb.set_trace()
        employee_name=validated_data.get('employee_name')
        validated_data['username']=employee_name
        emp_id=User.objects.order_by('-id').first()
        print("gfgydgdygdgyd",emp_id.id)
        if emp_id:
            prev_emp_id=emp_id.emp_id
            if prev_emp_id is not None:
                next_emp_id=int(prev_emp_id)+1
                validated_data['emp_id']=next_emp_id
            else:
             validated_data['emp_id']=10001
        user=User.objects.create_user(**validated_data)
        return user
    