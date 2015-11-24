from datetime import date

from django.db import models
from django.contrib.auth.models import User



class BaseModel(models.Model):
    """ Abstract base class defining common fields and 
        methods to be used in other concrete models.
    """
    class Meta:
        abstract = True

    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(blank=True, default='')
    date_created = models.DateField(editable=False, auto_now_add=True)
    date_modified = models.DateField(editable=False, auto_now=True)

    def __unicode__(self):
        return u'{}'.format(self.name)
    


class BucketList(BaseModel):
    """ Model class defining a bucket list """

    created_by = models.ForeignKey(User, related_name='bucketlists', on_delete=models.CASCADE)

    @property
    def num_items(self):
        """
        Gets and returns the number of items in this bucketlist.
        """
        return self.items.count()

    @property
    def num_done_items(self):
        """
        Gets and returns the number of items in this bucketlist that
        are marked as done.
        """
        return self.items.filter(done=True).count()



class BucketListItem(BaseModel):
    """ Model class defining a bucket list item"""
    
    bucketlist = models.ForeignKey('BucketList', related_name='items', on_delete=models.CASCADE)
    done =  models.BooleanField(blank=False, default=False)







