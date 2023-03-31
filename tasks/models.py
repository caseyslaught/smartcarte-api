from django.db import models
import uuid

from account.models import Account, DemoUser, Organization, Region
from SmartCarteApi.common import get_utc_datetime_now


class BaseTask(models.Model):
    
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    datetime_created = models.DateTimeField(default=get_utc_datetime_now)
    datetime_completed = models.DateTimeField(null=True)
    datetime_updated = models.DateTimeField(null=True)

    type = models.CharField(max_length=40, null=True) # demo_classification, burn_areas, forest_change, lulc_change, lulc_classification
    status = models.CharField(max_length=50) # pending, running, complete, failed
    status_message = models.CharField(max_length=200, null=True, blank=True)
    status_long_message = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class DemoLandcoverClassificationTask(BaseTask):

    # parameters
    date = models.DateField()
    region_geojson = models.TextField()
    email = models.EmailField(null=True, blank=True)
    demo_user = models.ForeignKey(DemoUser, on_delete=models.CASCADE, related_name='demo_classification_tasks', null=True)

    # results
    statistics_json = models.TextField(null=True, blank=True) # summary of results in JSON format
    imagery_tif_href = models.CharField(max_length=240, null=True, blank=True)
    imagery_tiles_href = models.CharField(max_length=240, null=True, blank=True)
    landcover_tif_href = models.CharField(max_length=240, null=True, blank=True)
    landcover_tiles_href = models.CharField(max_length=240, null=True, blank=True)
    rgb_tif_href = models.CharField(max_length=240, null=True, blank=True)


class ForestChangeTask(BaseTask):

    start_date = models.DateField()
    end_date = models.DateField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='tasks')

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='forest_change_tasks')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='forest_change_tasks')

    gain_area = models.IntegerField(null=True) # m2
    loss_area = models.IntegerField(null=True)
    total_area = models.IntegerField(null=True) # total non-masked area
    
    # ex. https://data.smartcarte.com/.../rgb_byte_tiles/{z}/{y}/{x}.png
    before_rgb_tiles_href = models.CharField(max_length=200, null=True) 
    after_rgb_tiles_href = models.CharField(max_length=200, null=True)
    change_tiles_href = models.CharField(max_length=200, null=True)

