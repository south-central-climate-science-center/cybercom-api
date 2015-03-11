_author__ = 'mstacy'
from django.conf.urls import patterns, url
from catalog.views import Catalog,CatalogData, CatalogDataDetail # SourceList, SourceDetail
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
                       url(r'^data/$', Catalog.as_view(),name='catalog-list'),
                       url(r'^data/(?P<database>[^/]+)/$',Catalog.as_view(),name='catalog-list'),
                       url(r'^data/(?P<database>[^/]+)/(?P<collection>[^/]+)/$',CatalogData.as_view(),name='catalog-detail'),
                       url(r'^data/(?P<database>[^/]+)/(?P<collection>[^/]+)/(?P<id>[^/]+)/$', CatalogDataDetail.as_view(),
                           name='catalog-detail-id'),
                       #url(r'^source/$', SourceList.as_view(), name='source-list'),
                       #url(r'^source/(?P<id>[^/]+)/$', SourceDetail.as_view(), name='source-detail'),

)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'jsonp', 'xml', 'yaml'])
