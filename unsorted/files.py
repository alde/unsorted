import os
from ffvideo import VideoStream
import logging
import base64

STATIC_DIR = os.path.dirname(__file__) + '/static/'
logger = logging.getLogger(__name__)


def read_dir(dir):
    return [
        FileRepr(dir, file).to_dict()
        for file in os.listdir(dir)
        if file != 'keep'
    ]


def delete_by_hash(dir, hash):
    file = base64.b16decode(hash).decode('utf-8')
    full_path = '%s/%s' % (dir, file)
    logger.info('Deleting %s' % full_path)
    os.remove(full_path)


class FileRepr:
    def __init__(self, dir, file):
        self.file = file
        self.full_path = '%s/%s' % (dir, file)


    def thumbnail(self):
        filename = STATIC_DIR + self.hash + '.png'
        try:
            open(filename)
        except:
            logger.debug("Generating new thumbnail.")

            pil_image = VideoStream(self.full_path)\
                .get_frame_at_sec(60).image()
            pil_image.save(filename)

        return filename


    @property
    def hash(self):
        return base64.b16encode(self.file).decode('utf-8')


    def to_dict(self):
        return {
            'file': self.file,
            'full_path': self.full_path,
            'thumbnail': self.thumbnail().replace('unsorted', ''),
            'hash': self.hash
        }
