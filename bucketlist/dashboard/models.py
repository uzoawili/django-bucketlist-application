from datetime import date

from django.db import models
from django.contrib.auth.models import User



class BaseModel(models.Model):
    """ Abstract base class defining common fields and 
        methods to be used in other concrete models.
    """
    class Meta:
        abstract = True

    name = models.TextField(blank=False)
    description = models.TextField(blank=False)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'{}'.format(self.name)
    


class BucketList(BaseModel):
    """ model class defining a bucket list """

    creator = models.ForeignKey(User, related_name='bucketlists', on_delete=models.CASCADE)



class BucketListItem(BaseModel):
    """ model class defining a bucket list item"""
    
    bucketlist = models.ForeignKey('BucketList', related_name='items', on_delete=models.CASCADE)
    done =  models.BooleanField(blank=False, default=False)