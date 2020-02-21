from django.db import models
from uuid import uuid4
from Account.models import (
    Farmer,
    Expert,
    Others
)
from django.core.exceptions import ValidationError
# Create your models here.
def upload_image(instance, filename):
    return f"post/{instance.post_id}/{filename}"

class PostIng(models.Model):
    "this will hold the information of the post"
    post_id = models.UUIDField(
        verbose_name="Post ID",
        help_text = "Post's Unique ID",
        primary_key = True,
        unique=True,
        default=uuid4
    )
    tags = models.TextField(
        verbose_name="Tags For unique Identification",
        help_text="Comma Separted data",
    )
    description = models.TextField(
        verbose_name="Description",
        help_text = "Information to Pass"
    )
    farmer = models.ForeignKey(
        "Account.Farmer", 
        verbose_name="Farmer Account", 
        on_delete=models.CASCADE,
        blank = True,
        null = True,
        related_name="farmer_posts"
        )
    expert = models.ForeignKey(
        "Account.Expert", 
        verbose_name="Expert", 
        on_delete=models.CASCADE,
        blank = True,
        null = True,
        related_name="expert_posts"
    )
    other  = models.ForeignKey(
        "Account.Others", 
        verbose_name="Others", 
        on_delete=models.CASCADE,
        blank = True,
        null =True,
        related_name="other_posts"
    )
    when = models.DateTimeField(
        verbose_name="When", 
        auto_now_add=True
    )
    img_url = models.URLField(
        verbose_name="Image_url", 
        max_length=200,
        blank=True,
        null=True
    )
    img = models.ImageField(
        verbose_name="Image", 
        upload_to=upload_image, 
        height_field=None, 
        width_field=None, 
        max_length=None,
        blank=True,
        null=True,
    )
    
    
    @property
    def tags_separated(self):
        data = self.tags
        return str(data).split(",")

    @property
    def comments(self):
        return self.post_comment.all()

    @property
    def name(self):
        if self.farmer:
            return self.farmer.farmer_full_name
        elif self.expert:
            return self.expert.expert_full_name
        elif self.other:
            return self.other_full_name

    class Meta:
        verbose_name = "PostIng"
        verbose_name_plural = "PostIngs"

def upload_image_com(instance, filename):
    return f"comment/{instance.comment_id}/{filename}"
class Comment(models.Model):
    "this will hold the information of the comment"
    comment_id = models.UUIDField(
        verbose_name="Comment ID",
        help_text = "Comment's Unique ID",
        primary_key = True,
        unique=True,
        default=uuid4
    )
    farmer = models.ForeignKey(
        "Account.Farmer", 
        verbose_name="Farmer Account", 
        on_delete=models.CASCADE,
        blank = True,
        null = True,
        related_name="farmer_comment"
        )
    expert = models.ForeignKey(
        "Account.Expert", 
        verbose_name="Expert", 
        on_delete=models.CASCADE,
        blank = True,
        null = True,
        related_name="expert_comment"
    )
    other  = models.ForeignKey(
        "Account.Others", 
        verbose_name="Others", 
        on_delete=models.CASCADE,
        blank = True,
        null =True,
        related_name="other_comment"
    )
    post = models.ForeignKey(
        PostIng, 
        verbose_name="Post commented", 
        on_delete=models.CASCADE,
        related_name="post_comment",
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Description of the comment"
    )
    tags = models.TextField(
        verbose_name="Tags For unique Identification",
        help_text="Comma Separted data",
    )
    when = models.DateTimeField(
        verbose_name="When",  
        auto_now_add=True
    )
    img_url = models.URLField(
        verbose_name="Image_url", 
        max_length=200,
        blank=True,
        null=True
    )
    img = models.ImageField(
        verbose_name="Image", 
        upload_to=upload_image_com, 
        height_field=None, 
        width_field=None, 
        max_length=None,
        blank=True,
        null=True,
    )

    @property
    def tags_list(self):
        data = str(self.tags)
        return data.split(",")
    
    @property
    def replys(self):
        return self.Comment_reply.all()
    
    @property
    def name(self):
        if self.farmer:
            return self.farmer.farmer_full_name
        elif self.expert:
            return self.expert.expert_full_name
        elif self.other:
            return self.other_full_name
        
def upload_image_reply(instance, filename):
    return f"reply/{instance.id}/{filename}"
class Reply(models.Model):
    "this will handel the information of the reply"

    description = models.TextField(
        verbose_name="Reply Back"
    )
    farmer = models.ForeignKey(
        "Account.Farmer", 
        verbose_name="Farmer Account", 
        on_delete=models.CASCADE,
        blank = True,
        null = True,
        related_name="farmer_reply"
        )
    expert = models.ForeignKey(
        "Account.Expert", 
        verbose_name="Expert", 
        on_delete=models.CASCADE,
        blank = True,
        null = True,
        related_name="expert_reply"
    )
    other  = models.ForeignKey(
        "Account.Others", 
        verbose_name="Others", 
        on_delete=models.CASCADE,
        blank = True,
        null =True,
        related_name="other_reply"
    )
    comment = models.ForeignKey(
        Comment, 
        verbose_name="Reply On Comment", 
        on_delete=models.CASCADE, 
        related_name="Comment_reply",
    )
    img_url = models.URLField(
        verbose_name="Image_url", 
        max_length=200,
        blank=True,
        null=True
    )
    img = models.ImageField(
        verbose_name="Image", 
        upload_to=upload_image_reply, 
        height_field=None, 
        width_field=None, 
        max_length=None,
        blank=True,
        null=True,
    )
    when = models.DateTimeField(
        verbose_name="when It was Replied",  
        auto_now_add=True,
    )

    @property
    def name(self):
        if self.farmer:
            return self.farmer.farmer_full_name
        elif self.expert:
            return self.expert.expert_full_name
        elif self.other:
            return self.other_full_name