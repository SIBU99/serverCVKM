from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
def vedio_content(instance, filename):
    "this will hold the vedio of the vedio_content"
    return f"content/tutorial_vedio/{filename}"

def vedio_type_checker(value):
    "this will check the vedio type"
    filename = value.name
    print(filename)
    filename, extension = filename.split(".")
    if extension in ["mp4","wmv","wma","flv","3gp","mkv",]:
        return value
    else:
        msg = "Please Provide the Vedio in Correct Format"
        raise ValidationError(msg)


class VedioTutorial(models.Model):
    "this will Hold the vedio information and guide for the user"
    title = models.CharField(
        verbose_name="Title", 
        max_length=50,
    )
    vedio = models.FileField(
        verbose_name="Vedio Content",
        upload_to=vedio_content,
        max_length=100,
        validators=[
            vedio_type_checker,
        ]
    )
    language = models.CharField(
        verbose_name="Language Type", 
        max_length=50,
    )
    text_content = models.TextField(
        verbose_name="Textual Content",
        help_text="This will hold the texual content of the vedio and realated information"
    )
    
    class Meta:
        verbose_name = "Vedio Tutorial"
        verbose_name_plural = "Vedio Tutorials"
