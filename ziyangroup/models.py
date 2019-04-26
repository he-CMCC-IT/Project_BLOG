from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    REGION_CHOICES = (('dang_wu_gong_kai', '党务公开'),
                      ('huo_dong_lue_ying', '活动掠影'),
                      ('rong_yu_zhan_shi', '荣誉展示'),
                      ('kai_zhan_gong_shi', '开展公示'),
                      ('gui_zhang_zhi_du', '规章制度'),)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200, blank=True)
    region = models.CharField(max_length=200, choices=REGION_CHOICES, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ziyangroup:image_detail', args=[self.id, self.slug])
