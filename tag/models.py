from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
import string
from random import SystemRandom


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    #  aqui começam os campos para a relação genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=1000)

    # Um campo que representa a relação genérica que conhece os campos acima (content_type e object_id)

    content_object = GenericForeignKey('content_type', 'object_id')  # noqa

    def save(self, *args, **kwargs):
        if not self.slug:
            rand = ''.join(
                SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5
                )
            )
            self.slug = slugify(f'{self.name}-{rand}')

        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    