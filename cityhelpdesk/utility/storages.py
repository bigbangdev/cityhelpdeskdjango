# coding=utf-8
from __future__ import absolute_import

from django.contrib.staticfiles.storage import CachedFilesMixin
from storages.backends.s3boto import S3BotoStorage

try:
    from pipeline.storage import PipelineMixin
    class S3PipelineStorage (PipelineMixin, S3BotoStorage):
        pass

    class S3PipelineCachedStorage (PipelineMixin, CachedFilesMixin, S3BotoStorage):
        pass
except ImportError:
    pass
