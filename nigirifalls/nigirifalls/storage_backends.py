from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = settings.AWS_MEDIA_LOCATION
    default_acl = 'private'  # To turn access control list into private use only. Will use it in models.py
    file_overwrite = False  # Not to replace files even they have same name
    custom_domain = False


class PublicStorage(S3Boto3Storage):
    location = settings.AWS_PUBLIC_LOCATION
    file_overwrite = False
