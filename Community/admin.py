from django.contrib import admin
from .models import (
    PostIng,
    Comment,
    Reply,
)
# Register your models here.
admin.site.register(PostIng)
admin.site.register(Comment)
admin.site.register(Reply)