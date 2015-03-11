"""
from rest_framework import serializers
import mongoengine
import rest_framework_mongoengine.serializers as mongo_serializers
# Create your models here.
class Mapping(mongoengine.EmbeddedDocument):
    REF_NO = mongoengine.StringField( default="column_name")
    SiteType = mongoengine.StringField( default="column_name")
    Sitename = mongoengine.StringField( default="column_name")
    Status = mongoengine.StringField( default="column_name")
    aquifer = mongoengine.StringField( default="column_name")
    huc_4 = mongoengine.StringField( default="column_name")
    huc_8 = mongoengine.StringField(default="column_name")
    lat = mongoengine.StringField( default="column_name")
    lon = mongoengine.StringField( default="column_name")


class Source(mongoengine.DynamicDocument):
    id = mongoengine.ObjectIdField()
    name = mongoengine.StringField(required=True, default="name")
    model = mongoengine.StringField(required=True, default="Source")
    status = mongoengine.StringField(required=True, default="Inactive")
    sub = mongoengine.BooleanField(required=True, default=False)
    hassubs = mongoengine.BooleanField(required=True, default=False)
    url = mongoengine.StringField(required=True, default="/")
    value = mongoengine.StringField(required=True, default="value")
    order = mongoengine.FloatField(required=True, default=1.0)
    color = mongoengine.StringField(required=True, default="#00BB22")
    mapping = mongoengine.EmbeddedDocumentField(Mapping,required=True, default={})

    meta = {'app_label': 'catalog', 'model_name': 'Source'}
    def __unicode__(self):
        return self.name
    #class Meta:
        #collection = 'test'
    #    object_name = 'source'
    #    app_label = 'source'

        #permissions = (("can_view_article", "Can view Article"),
        #               ("can_change_article", "Can change Article"),
        #               ("can_delete_article", "Can delete Article"),)

class SourceSerializer(mongo_serializers.MongoEngineModelSerializer):
    #mongoengine.
    api_detail_url = serializers.HyperlinkedIdentityField(lookup_field='id', view_name='source-detail')
    #model = mongoengine.StringField"Source"

    class Meta:
        model = Source
        exclude = ['id', ]

#import django_filters

#class SourceFilter(django_filters.FilterSet):
#    class Meta:
#        model = Source
#        fields = ['name', 'model', 'status']

"""
