from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from random import choice
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import requests as req
from django.db.models.signals import post_save
from django.dispatch import receiver




# Create your models here.
"""
Target:
1. Create A Farmer Account
2. Create A Expert Account
3. Create A Others Account
4. Create A Buyers Account
"""

def farmer_dp_upload(instance, filename):
    return f"dp/{instance.farmer_id}/{filename}"

def validate_phone_number(value):
    "this will validate the phone number"
    if len(value) is 10 and value.isdigit():
        try:
            _ = Farmer.objects.get(farmer_phone= value)
            print("farmer")
            data_dic["exists"] = True
        except Farmer.DoesNotExist:
            try:
                _ = Expert.objects.get(expert_phone = value)
                print("expert")
                data_dic["exists"] = True
            except Expert.DoesNotExist:
                try:
                    _ = Others.objects.get(other_phone = value)
                    print("Others")
                    data_dic["exists"] = True
                except:
                    return value
    else:
        raise ValidationError("Provide A Valid Phone Number")


class Farmer(models.Model):
    "this will hold the information of the farmer"
    farmer_id = models.UUIDField(
        verbose_name="Farmer's ID",
        help_text = "Farmer's Unique ID",
        primary_key = True,
        unique=True,
        default=uuid4
    )
    farmer_user_auth = models.OneToOneField(
        User, 
        verbose_name="Famer's Authentication Account", 
        on_delete=models.CASCADE,
        related_name="farmer_account",
    )
    farmer_full_name = models.CharField(
        verbose_name="Farmer's Fullname",
        help_text="Farmer's Full Name", 
        max_length=100
    )
    farmer_gender = models.CharField(
        verbose_name="Farmer's Gender", 
        max_length=20,
        choices=[
            ("female", "Female"),
            ("male", "Male"),
            ("other","Other"),
        ],
        default="male",
    )
    

    farmer_email = models.EmailField(
        verbose_name="Farmer's Email",
        help_text="Farmer's Digital Point Of Contact",
        blank=True,
        null=True, 
        max_length=254
    )
    farmer_verified_email = models.BooleanField(
        verbose_name="Farmer's Email Verified",
        default=False
    )
    farmer_phone = models.CharField(
        verbose_name="Farmer's Phone Number",
        unique=True, 
        max_length=10,
        validators=[
            validate_phone_number,
        ]
    )
    farmer_verified_phone = models.BooleanField(
        verbose_name="Farmer's Phone Verified",
        default=False
    )
    
    farmer_doj = models.DateTimeField(
        verbose_name="D.O.J",
        help_text = "When did the farmer Created The Account" ,
        auto_now_add=True
    )
    farmer_dp = models.ImageField(
        verbose_name="Farmer's Profile Pic", 
        upload_to=farmer_dp_upload,
        default= "dp/default.jpg",
        height_field=None, 
        width_field=None, 
        max_length=None,
    )

    #address section of the farmer
    farmer_plot_no = models.CharField(
        verbose_name="Plot No", 
        help_text="Farmer's Plot No",
        blank=True,
        default="",
        max_length=50
    )
    farmer_street = models.CharField(
        verbose_name="Steet", 
        help_text="Farmer's Street",
        max_length=150
    )
    farmer_landmark = models.CharField(
        verbose_name="Landmark",
        help_text="Farmer's Landmark",
        blank=True,
        null = True,
        max_length=100,
    )
    farmer_place = models.CharField(
        verbose_name="Places",
        help_text="Farmer's Palces", 
        max_length=70
    )
    farmer_city = models.CharField(
        verbose_name="City",
        help_text="Farmer's City", 
        max_length=60
    )
    farmer_state = models.CharField(
        verbose_name="State",
        help_text="Farmer's State", 
        max_length=70,
    )
    farmer_country = models.CharField(
        verbose_name="Country",
        help_text="Farmer's Counrty", 
        max_length=50
    )


    @property
    def farmer_account_allowed(self):
        return True if self.farmer_verified_phone else False
    
    @property
    def farmer_digital_marketing_allowed(self):
        return True if self.farmer_verified_email else False


    class Meta:
        verbose_name = "Farmer"
        verbose_name_plural = "Farmers"
    
    def __str__(self):
        return self.farmer_full_name
    
    def __call__(self):
        print ("working all right")
    
    def save(self, *args, **kwargs):
        "this will trigger when the model is saved"
        names = self.farmer_full_name.split(" ")
        names = [name.capitalize() for name in names]
        self.farmer_full_name = " ".join(names)
        super(Farmer, self).save()

def docs_upload_location(instance, filename):
    return f"docs/verify/{instance.applicant_full_name}/{filename}"

class ExpertApply(models.Model):
    "This will store the information of the Expert"
    applicant_id = models.UUIDField(
        verbose_name="Expert's ID",
        help_text = "Expert Applicant's Unique ID",
        primary_key = True,
        unique=True,
        default=uuid4
    )
    applicant_full_name = models.CharField(
        verbose_name="Applicant's Fullname",
        help_text="Applicant's Full Name", 
        max_length=100
    )
    applicant_gender = models.CharField(
        verbose_name="Applicant's Gender", 
        max_length=20,
        choices=[
            ("female", "Female"),
            ("male", "Male"),
            ("other","Other"),
        ],
        default="male",
    )
    applicant_status = models.CharField(
        verbose_name="Status of the Application", 
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending",
    )

    applicant_email = models.EmailField(
        verbose_name="Applicant's Email",
        help_text="Applicant's Digital Point Of Contact",
        unique=True,
        max_length=254
    )

    applicant_verified_email = models.BooleanField(
        verbose_name="Applicant's Email Verified",
        default=False
    )
    applicant_phone = models.CharField(
        verbose_name="Applicant's Phone Number",
        unique=True, 
        max_length=10,
        validators=[
            validate_phone_number,
        ]
    )
    applicant_verified_phone = models.BooleanField(
        verbose_name="Applicant's Phone Verified",
        default=False
    )

    #address section of the farmer
    applicant_plot_no = models.CharField(
        verbose_name="Plot No", 
        help_text="Applicant's Plot No",
        blank=True,
        default="",
        max_length=50
    )
    applicant_street = models.CharField(
        verbose_name="Steet", 
        help_text="Applicant's Street",
        max_length=150
    )
    applicant_landmark = models.CharField(
        verbose_name="Landmark",
        help_text="Applicant's Landmark",
        blank=True,
        null = True,
        max_length=100,
    )
    applicant_place = models.CharField(
        verbose_name="Places",
        help_text="Applicant's Palces", 
        max_length=70
    )
    applicant_city = models.CharField(
        verbose_name="City",
        help_text="Applicant's City", 
        max_length=60
    )
    applicant_state = models.CharField(
        verbose_name="State",
        help_text="Applicant's State", 
        max_length=70,
    )
    applicant_country = models.CharField(
        verbose_name="Country",
        help_text="Applicant's Counrty", 
        max_length=50
    )
    # applicant_supported_docs = models.FileField(
    #     verbose_name="Applicant Supported Docs",
    #      help_text="Applicants Supported Docs In zip Format",
    #     upload_to=docs_upload_location, 
    #     max_length=100
    # )

    @property
    def applicant_supported_docs(self):
        return self.linked_account_doc.all()

    class Meta:
        verbose_name = "ExpertApply"
        verbose_name_plural = "ExpertApplys"

@receiver(post_save, sender = ExpertApply)
def create_expert_account(sender, instance, *args, **kwargs):
    "this will triger when the application is passed"
    if instance.applicant_status == "accepted":
        no_of_expert = Expert.objects.count()
        
        user = User.objects.create(
            username = f"expert{no_of_expert + 1}"
        )
        user.set_password("Cvrce@123") #default password

        exp = Expert()
        exp.expert_user_auth = user
        exp.expert_full_name = instance.applicant_full_name
        exp.expert_gender = instance.applicant_gender
        exp.expert_email = instance.applicant_email
        exp.expert_verified_email = instance.applicant_verified_email
        exp.expert_phone = instance.applicant_phone
        exp.expert_verified_phone = instance.applicant_verified_phone
        exp.expert_plot_no = instance.applicant_plot_no
        exp.expert_street = instance.applicant_street
        exp.expert_landmark = instance.applicant_landmark
        exp.expert_place = instance.applicant_place
        exp.expert_city = instance.applicant_city
        exp.expert_state = instance.applicant_state
        exp.expert_country = instance.applicant_country
        exp.save()


def expert_dp_upload(instance, filename):
    return f"dp/{instance.expert_id}/{filename}"

class Expert(models.Model):
    "This will hold the information of the expert"
    expert_id = models.UUIDField(
        verbose_name="Expert's ID",
        help_text = "Expert's Unique ID",
        primary_key = True,
        unique=True,
        default=uuid4
    )
    expert_user_auth = models.OneToOneField(
        User, 
        verbose_name="Famer's Authentication Account", 
        on_delete=models.CASCADE,
        related_name="expert_account",
    )
    expert_full_name = models.CharField(
        verbose_name="Expert's Fullname",
        help_text="Expert's Full Name", 
        max_length=100
    )
    expert_gender = models.CharField(
        verbose_name="Expert's Gender", 
        max_length=20,
        choices=[
            ("female", "Female"),
            ("male", "Male"),
            ("other","Other"),
        ],
        default="male",
    )

    expert_email = models.EmailField(
        verbose_name="Expert's Email",
        help_text="Expert's Digital Point Of Contact",
        unique=True,
        max_length=254
    )
    expert_verified_email = models.BooleanField(
        verbose_name="Expert's Email Verified",
        default=False
    )
    expert_phone = models.CharField(
        verbose_name="Expert's Phone Number",  
        unique=True, 
        max_length=10,
        validators=[
            validate_phone_number,
        ]
    )
    expert_verified_phone = models.BooleanField(
        verbose_name="Expert's Phone Verified",
        default=False
    )

    #address section of the farmer
    expert_plot_no = models.CharField(
        verbose_name="Plot No", 
        help_text="Expert's Plot No",
        blank=True,
        default="",
        max_length=50
    )
    expert_street = models.CharField(
        verbose_name="Steet", 
        help_text="Expert's Street",
        max_length=150
    )
    expert_landmark = models.CharField(
        verbose_name="Landmark",
        help_text="Expert's Landmark",
        blank=True,
        null = True,
        max_length=100,
    )
    expert_place = models.CharField(
        verbose_name="Places",
        help_text="Expert's Palces", 
        max_length=70
    )
    expert_city = models.CharField(
        verbose_name="City",
        help_text="Expert's City", 
        max_length=60
    )
    expert_state = models.CharField(
        verbose_name="State",
        help_text="Expert's State", 
        max_length=70,
    )
    expert_country = models.CharField(
        verbose_name="Country",
        help_text="Expert's Counrty", 
        max_length=50
    )
    expert_dp = models.ImageField(
        verbose_name="Expert's Profile Pic", 
        upload_to=expert_dp_upload,
        default= "dp/default.jpg",
        height_field=None, 
        width_field=None, 
        max_length=None,
    )
    expert_doj = models.DateTimeField(
        verbose_name="Expert's D.O.J.",  
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Expert"
        verbose_name_plural = "Experts"


def other_dp_upload(instance, filename):
    return f"dp/{instance.id}/{filename}"

class Others(models.Model):
    "This will store the information of the Others Account"
    other_user_auth = models.OneToOneField(
        User, 
        verbose_name="Other's Authentication Account", 
        on_delete=models.CASCADE,
        related_name="other_account",
    )
    other_full_name = models.CharField(
        verbose_name="Other's Fullname",
        help_text="Expert's Full Name", 
        max_length=100
    )
    other_gender = models.CharField(
        verbose_name="Other's Gender", 
        max_length=20,
        choices=[
            ("female", "Female"),
            ("male", "Male"),
            ("other","Other"),
        ],
        default="male",
    )

    other_email = models.EmailField(
        verbose_name="Other's Email",
        help_text="Other's Digital Point Of Contact",
        unique=True,
        max_length=254
    )
    other_verified_email = models.BooleanField(
        verbose_name="Other's Email Verified",
        default=False
    )
    other_phone = models.CharField(
        verbose_name="Other's Phone Number",  
        unique=True, 
        max_length=10,
        validators=[
            validate_phone_number,
        ]
    )
    other_verified_phone = models.BooleanField(
        verbose_name="Other's Phone Verified",
        default=False
    )
    other_post = models.TextField(
        verbose_name="Post Or Designation"
    )
    other_address = models.TextField(
        verbose_name="Other's Address",
    )
    other_dp = models.ImageField(
        verbose_name="Other's DP", 
        upload_to=other_dp_upload, 
        height_field=None, 
        width_field=None, 
        max_length=None
    )

    class Meta:
        verbose_name = "Others"
        verbose_name_plural = "Otherss"

class OTPTokenPhone(models.Model):
    "this will used as a otp based varification of otp"

    phone_number = models.CharField(
        verbose_name="Phone Number", 
        max_length=10,
        validators=[
            validate_phone_number
        ]
    )

    token = models.CharField(
        verbose_name="Token", 
        max_length=4,
        blank=True,
    )

    purpose = models.CharField(
        verbose_name="Purpose", 
        max_length=50,
        choices=[
            ("vermob", "Verification Mobile"),
            ("forpas", "Forgot Password"),
            ("indent", "Identify The Account")
        ],
        default="ver",
    )
    created_on = models.DateTimeField(
        verbose_name="Created On", 
        auto_now_add=True, 
    )
    change_request = models.BooleanField(
        verbose_name="Regenerate Token",
        default = True,
    )
    token_used = models.BooleanField(
        verbose_name="Token Used",
        default = False
    )
    token_update = models.BooleanField(
        verbose_name="Token Update",
        default=False
    )

    @property
    def is_reupdate(self):
        current_date_time = timezone.now()
        print(self.created_on, "#"*20)
        return True if self.created_on - current_date_time > timedelta(days=1, hours=12) else False

    @property
    def is_expired(self):
        current_date_time = timezone.now()
        return True if self.created_on - current_date_time > timedelta(minutes=10) else False

    def save(self, *args, **kwargs):
        "this will triger when the model is saved"
        if not self.token_used:
                if self.change_request:
                    token = self.generate_otp()
                    self.token = token
                    phone_number = self.phone_number
                    if self.purpose == "vermob":
                        temp_id = 23399
                    elif self.purpose == "forpas":
                        temp_id = 23422 #change it
                    elif self.purpose == "indent":
                        temp_id = 23423 #Change it
                    self.change_request = False
                    self.send_the_otp_in_mobile(token, phone_number, temp_id)
                    super(OTPTokenPhone, self).save()
        elif self.token_update:
            if self.is_reupdate:
                if self.change_request:
                    self.created_on = timezone.now()
                    token = self.generate_otp()
                    self.token = token
                    phone_number = self.phone_number
                    if self.purpose == "vermob":
                        temp_id = 23399
                    elif self.purpose == "forpas":
                        temp_id = 23422 #change it
                    elif self.purpose == "indent":
                        temp_id = 23423 #Change it
                    self.change_request = False
                    self.token_update = False
                    self.send_the_otp_in_mobile(token, phone_number, temp_id)
                    super(OTPTokenPhone, self).save()
        else:
            super(OTPTokenPhone, self).save()

    
    def __str__(self):
        return f"{self.phone_number} | {self.purpose}"

    def generate_otp(self):
        "this will generate 4 digit otp for mobile number"
        token = 0
        l = [ i for i in range(1,10) ]
        for _ in range(4):
            temp_token = choice(l)
            token *= 10
            token += temp_token
        else:
            token = str(token)
            return token
    
    def send_the_otp_in_mobile(self, otp, phone_no, temp_id):
        "this will send the otp using fast2sms api"
        url = "https://www.fast2sms.com/dev/bulk"
        #hide the api key
        key = "1zrRO4aB5F2spjYolkVqNtxAdJeZuHnhEDWMX9P3KS8UGIic7Q0Xo3yEaK1znpNJO8cdeSCGxFbMrALU"
        #key = os.environ.get("sms_api", None)
        querystring = dict()
        count = 3
        while count:
            querystring["authorization"] = key
            querystring["sender_id"]= "FSTSMS"
            querystring["language"]= "english"
            querystring["route"]="qt"
            querystring["numbers"] = f"{phone_no}"
            querystring["message"] = f"{temp_id}" #! change the templete code so that we can execute it as per our requirement
            querystring["variables"] = "{BB}|{AA}"#? change look over it
            querystring["variables_values"] = f"{phone_no}|{otp}" #? look over it
        
            headers = {
            'cache-control': "no-cache"
            }
            count -= 1
            response = req.request("GET", url, headers=headers, params=querystring)
            if response.status_code == 200:
                print("Send the otp")
                return 200
        else:
            print("Failed the otp")
            return 404
    
    class Meta:
        verbose_name = "OTPToken"
        verbose_name_plural = "OTPTokens"
        unique_together = (
            "phone_number",
            "purpose",
        )

def document_upload(instance, filename):
    return f"document/{instance.id}/{filename}"

class Document(models.Model):
    "this will Store the Documents of the Applying Person"
    file = models.FileField(
        verbose_name="File Upload", 
        upload_to=document_upload, 
        max_length=100
    )
    linked = models.ForeignKey(
        "Account.ExpertApply", 
        verbose_name="", 
        on_delete=models.CASCADE,
        related_name="linked_account_doc"
    )

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    