from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
import PIL
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class Image(models.Model):
    image = models.FileField(
        _("Image"), upload_to="%Y/%m/%d/", help_text=_("Image url and path")
    )
    name = models.CharField(
        _("Name"), max_length=100, help_text=_("Image name"), blank=True
    )
    upload_in = models.DateTimeField(
        _("Upload in"),
        blank=True,
        auto_now_add=True,
        help_text=_("image upload date"),
    )

    uploader = models.ForeignKey(
        User, blank=True, null=True, default=1, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name


class Contribute(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="contribute/")
    more_link = models.URLField()
    description = models.TextField()
    created_in = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="sponsor/")
    more_link = models.URLField()
    description = models.TextField()
    created_in = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return self.name


class New(models.Model):
    title = models.CharField(
        _("Title"), max_length=100, help_text=_("title of the news")
    )
    abstract = models.TextField(_("Abstract"), help_text=_("news summary"))
    processed_abstract = models.TextField(
        _("processed Abstract"),
        help_text=_("news processed summary"),
        blank=True,
        default="",
    )
    content = models.TextField(_("Content"), help_text=_("news content"))
    processed_content = models.TextField(
        _("Processed Content"),
        help_text=_("news processed content"),
        blank=True,
        default="",
    )
    image = models.ImageField(
        _("Image"), upload_to="%Y/%m/%d/", blank=True, help_text=_("news cover image")
    )
    posted_in = models.DateTimeField(
        _("Posted in"),
        default=timezone.now,
        blank=True,
        help_text=_("news posting date"),
    )
    poster = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text=_("news editor")
    )
    views = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title

    def save(self):
        text = str(self.content)
        text = text.replace("\r\n", "\\n ")

        self.processed_content = text

        text_abstract = str(self.abstract)
        text_abstract = text_abstract.replace("\r\n", "\\n ")

        self.processed_abstract = text_abstract

        img = None

        try:
            img = PIL.Image.open(self.image).convert("RGB")
        except:
            img = Image.open(self.image).convert("RGB")

        buffer = BytesIO()

        # Resize/modify the image
        img = img.resize((900, 506))

        # after modifications, save it to the output
        img.save(buffer, format="JPEG", quality=100)

        # change the imagefield value to be the newley modifed image value
        self.image = InMemoryUploadedFile(
            buffer,
            None,
            "%s.jpg" % self.image.name.split(".")[0],
            "image/jpeg",
            len(buffer.getbuffer()),
            None,
        )

        super(New, self).save()
