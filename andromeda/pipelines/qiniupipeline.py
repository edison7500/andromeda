from qiniu import BucketManager
from scrapy.pipelines.images import ImagesPipeline
from andromeda import settings
from email.utils import parsedate_tz, mktime_tz

from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config


# from scrapy.utils.misc import md5sum


class QNFilesStore(object):

    # OSS_ACCESS_KEY_ID       = settings.OSS_ACCESS_KEY_ID
    # OSS_SECRET_ACCESS_KEY   = settings.OSS_SECRET_ACCESS_KEY
    # OSS_ENDPOINT            = settings.OSS_ENDPOINT
    # OSS_BUCKET              = settings.OSS_BUCKET
    QINIU_ACCESS_KEY        = settings.QINIU_ACCESS_KEY
    QINIU_SECRET_KEY        = settings.QINIU_SECRET_KEY
    QINIU_BUCKET_NAME       = settings.QINIU_BUCKET_NAME

    # HEADERS = {
    #     'Cache-Control': 'max-age=172800',
    #     'Expires': 180,
    # }

    def __init__(self, uri):
        self.q  = Auth(self.QINIU_ACCESS_KEY, self.QINIU_SECRET_KEY)
        # self.oss_bucket = self._get_oss_bucket()

    # def _get_qn_bucket(self):
    #     return self.QINIU_BUCKET_NAME

        # auth    = oss2.Auth(self.OSS_ACCESS_KEY_ID, self.OSS_SECRET_ACCESS_KEY)
        # return oss2.Bucket(auth, self.OSS_ENDPOINT, self.OSS_BUCKET)

    def persist_file(self, path, buf, info, meta=None, headers=None):
        # headers.update(self.HEADERS)
        # res = self.oss_bucket.put_object(path, buf.getvalue())
        # print res
        token       = self.q.upload_token(self.QINIU_BUCKET_NAME, path)
        res, info   = put_data(token, path, buf.getvalue())
        print("persist res", res)


    def stat_file(self, path, info):
        bucket = BucketManager(self.q)
        ret, qninfo = bucket.stat(self.QINIU_BUCKET_NAME, path)
        if 'hash' in ret:
            modified_tuple = parsedate_tz(ret['putTime'])
            modified_stamp = int(mktime_tz(modified_tuple))
            return {'checksum': path, 'last_modified': modified_stamp}
        return {}

class QNImagesPipeline(ImagesPipeline):

    STORE_SCHEMES = {
        # '': FSFilesStore,
        # 'file': FSFilesStore,
        'qiniu': QNFilesStore,
    }

    @classmethod
    def from_settings(cls, settings):
        qiniustore                      = cls.STORE_SCHEMES['qiniu']
        qiniustore.QINIU_ACCESS_KEY     = settings['QINIU_ACCESS_KEY']
        qiniustore.QINIU_SECRET_KEY     = settings['QINIU_SECRET_KEY']
        qiniustore.QINIU_BUCKET_NAME    = settings['QINIU_BUCKET_NAME']
        store_uri                       = settings['IMAGES_STORE']

        return cls(store_uri, settings=settings)

    def _get_store(self, uri):
        store_cls   = self.STORE_SCHEMES['qiniu']
        return store_cls(uri)

    def file_path(self, request, response=None, info=None):
        filename = super(QNImagesPipeline, self).file_path(request, response, info)
        filename = filename.replace('full/', settings.IMAGES_STORE)
        return filename