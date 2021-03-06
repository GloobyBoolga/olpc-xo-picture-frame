#! /usr/bin/python
"""Quick'n'dirty prog to get pictures from a picasa album.

Uses the google API to get url info.
See:
  https://developers.google.com/picasa-web/docs/1.0/developers_guide_python#PhotosInfo
  https://developers.google.com/picasa-web/docs/2.0/reference
"""

import argparse
import gdata.photos
import gdata.photos.service
import netrc
import os
import re
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
    self.valid_imgmax_sizes = (94, 110, 128, 200, 220, 288, 320, 400, 512, 576, 640, 720, 800, 912, 1024, 1152, 1280, 1440, 1600)
    self.imgmax_size = 1280
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
      print 'Failed to get auth config from netrc file for:', self.netrc_machine, 'e=', e
      raise
    print self.login, self.password

  def prepOutDir(self):
    """Makes sure the output dir is workable."""
    if not os.path.exists(self.out_dir):
      os.mkdir(self.out_dir)
    elif os.path.exists(self.out_dir) and not os.path.isdir(self.out_dir):
      raise UserWarning("out dir(" + self.out_dir + ") path is not a dir")

  def extractSlideshowInfo(self, album_description):
    cfg_file = open(os.path.join(self.out_dir, 'slideshow.config'), 'w')
    for var,val in re.findall('(?m)slideshow:(?P<varName>[^=]+)=(?P<varValue>.*$)', album_description):
      print '%(var)s="%(val)s"' % { 'var': var, 'val': val }
      print >> cfg_file,  '%(var)s="%(val)s"' % { 'var': var, 'val': val }
    cfg_file.close()

  def fetch(self):
    """Fetches the selected album into the output directory.

    Uses:
      - album_name, out_dir, photo_limit
    """
    print 'fetching at most', self.photo_limit, 'photos from <' + self.album_name + '> into', self.out_dir
    pws = gdata.photos.service.PhotosService()
    pws.ClientLogin(self.login, self.password)
    #Get all albums
    albums = pws.GetUserFeed(kind='album', limit=self.album_limit).entry

    for album in albums:
      if album.title.text.find(self.album_name) < 0: continue
      print '* ', album.title.text, album.gphoto_id.text, album.media.description.text
      self.extractSlideshowInfo(album.media.description.text)
      photos = pws.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo&imgmax=%d' % (
              self.login, album.gphoto_id.text, self.imgmax_size),
                           limit=self.photo_limit)
      for photo in photos.entry:
        print '  ', photo.title.text, photo.content.src
        urllib.urlretrieve(photo.content.src, os.path.join(self.out_dir, photo.title.text))

def main(argv):
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--album_name', default='MMG and JPA Wedding 2012-08-18', help='The name of the album to fetch')
  parser.add_argument('--out_dir', default='./pics', help='The directory to put photos into')
  parser.add_argument('--photo_limit', default=5, type=int, help='Must be >= 1')
  parser.add_argument('--imgmax_size', default=666, type=int, help='Upper limit of the img size requested')
  args = parser.parse_args(argv)
  if args.photo_limit < 1:
    raise UserWarning('photo_limit ' + str(args.photo_limit) + ' should be >= 1.')
  p = PicasaWebAlbum(args.album_name, args.out_dir)
  if args.imgmax_size not in p.valid_imgmax_sizes:
    # Having a wrong size like 666 still seems to work ... for now?
    print 'imgmax_size ' + str(args.imgmax_size) + ' not within ' + str(p.valid_imgmax_sizes)
  p.imgmax_size = args.imgmax_size

  p.loadConfig();
  p.photo_limit = args.photo_limit
  p.prepOutDir()
  p.fetch()

if __name__ == '__main__':
  main(sys.argv[1:])
