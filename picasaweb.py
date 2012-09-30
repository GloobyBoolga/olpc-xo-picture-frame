#! /usr/bin/python
"""Quick'n'dirty prog to get pictures from a picasa album.

Uses the google API to get url info.
See:
  https://developers.google.com/picasa-web/docs/1.0/developers_guide_python#PhotosInfo
  https://developers.google.com/picasa-web/docs/2.0/reference
"""

import gdata.photos
import gdata.photos.service
import netrc
import os
import sys
import urllib

class PicasaWebAlbum(object):
  """Class to work on the picasa web via the Google Data API.

  The login/password are extracted from ~/.netrc.
  The 'machine' is assumed to be 'picasaweb'. 
  """
  def __init__(self, album_name, out_dir):
    self.album_name = album_name
    self.out_dir = out_dir
    # Set the size of the photos, max_size is one of:
    # 94, 110, 128, 200, 220, 288, 320, 400, 512, 576, 640, 720, 800, 912, 1024, 1152, 1280, 1440, 1600
    self.max_size = 1280
    # Maximum number of photos to look at.
    self.photo_limit = 500
    # Number of album titles to look at.
    self.album_limit = 200
    self.netrc_machine = 'picasaweb'
    self.login = None
    self.password = None

  def loadConfig(self):
    """Loads the config info.

    Relies on netrc, assumes machine is 'picasaweb'.
    """
    try:
      cfg = netrc.netrc()
      self.login, _, self.password = cfg.authenticators(self.netrc_machine)
    except (TypeError, IOError), e:
      print 'Failed to get auth config from netrc file for:', self.netrc_machine
      raise
    print self.login, self.password

  def prepOutDir(self):
    """Makes sure the output dir is workable."""
    if not os.path.exists(self.out_dir):
      os.mkdir(self.out_dir)
    elif os.path.exists(self.out_dir) and not os.path.isdir(self.out_dir):
      raise UserWarning("out dir(" + self.out_dir + ") path is not a dir")

  def fetch(self):
    """Fetches the selected album into the output directory.

    Uses:
      - album_name, out_dir, photo_limit
    """
    print 'fetching <', self.album_name, '> into ', self.out_dir
    pws = gdata.photos.service.PhotosService()
    pws.ClientLogin(self.login, self.password)
    #Get all albums
    albums = pws.GetUserFeed(kind='album', limit=self.album_limit).entry

    for album in albums:
      if album.title.text.find(self.album_name) < 0: continue
      print '* ', album.title.text, album.gphoto_id.text
      photos = pws.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo&imgmax=%d' % (
              self.login, album.gphoto_id.text, self.max_size),
                           limit=self.photo_limit)
      for photo in photos.entry:
        print '  ', photo.title.text, photo.content.src
        urllib.urlretrieve(photo.content.src, os.path.join(self.out_dir, photo.title.text))

def main(argv):
  if argv:
    album_name = argv.pop(0)
  if argv:
    out_dir = argv.pop(0)
  if argv:
    photo_limit = int(argv.pop(0))
    if photo_limit < 1:
      raise UserWarning('photo_limit ' + str(photo_limit) + ' should be >= 1.')

  if not album_name:
    album_name = 'MMG and JPA Wedding 2012-08-18'
  if not out_dir:
    out_dir = './pics'
  if not photo_limit:
    photo_limit = 5

  p = PicasaWebAlbum(album_name, out_dir)
  p.loadConfig();
  p.photo_limit = photo_limit
  p.prepOutDir()
  p.fetch()

if __name__ == '__main__':
  main(sys.argv[1:])
