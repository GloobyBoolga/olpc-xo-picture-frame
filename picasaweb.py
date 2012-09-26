#! /usr/bin/python
"""Quick'n'dirty prog to get pictures from a picasa album.

Uses the google API to get url info.
See:
  https://developers.google.com/picasa-web/docs/1.0/developers_guide_python#PhotosInfo
  https://developers.google.com/picasa-web/docs/2.0/reference
"""
  
import gdata.photos
import gdata.photos.service
import os
import sys
import urllib

class PicasaWebAlbum(object):
  # recentTime = time.mktime(time.strptime('2012-07-01 00:00:00', '%Y-%m-%d %H:%M:%S'))

  # 94, 110, 128, 200, 220, 288, 320, 400, 512, 576, 640, 720, 800, 912, 1024, 1152, 1280, 1440, 1600
  max_size = 96
  username = 'abgrall.jp'
  app_password = 'yvgncfdgxlccvogl'
  photo_limit = 500

  def fetch(self, album_name, out_dir):
    pws = gdata.photos.service.PhotosService()
    pws.ClientLogin(self.username, self.app_password)
    #Get all albums
    albums = pws.GetUserFeed(kind='album', limit=200).entry

    for album in albums:
      if album.title.text.find(album_name) < 0: continue
      print '* ', album.title.text, album.gphoto_id.text
      photos = pws.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo&imgmax=%d' % (
              self.username, album.gphoto_id.text, self.max_size),
                           limit=self.photo_limit)
      for photo in photos.entry:
        print '  ', photo.title.text, photo.content.src
        urllib.urlretrieve(photo.content.src, os.path.join(out_dir, photo.title.text))

def main(argv):
  p = PicasaWebAlbum()
  album_name = 'MMG and JPA Wedding 2012-08-18'
  out_dir = './pics'
  if argv:
    album_name = argv[0]
  if len(argv) > 1:
    out_dir = argv[1]
  p.fetch(album_name, out_dir)

if __name__ == '__main__':
  main(sys.argv[1:])
