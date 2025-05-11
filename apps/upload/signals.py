
from PIL import Image
from django.db.models import signals
from django.dispatch import receiver


@receiver(signals.post_save, sender='upload.ImageUpload')
def image_compressor(sender, **kwargs): 
    with Image.open(kwargs["instance"].file.path) as photo:
        photo.save(kwargs["instance"].file.path, optimize=True, quality=70)

