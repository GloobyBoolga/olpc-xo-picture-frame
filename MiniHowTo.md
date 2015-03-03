#summary Explain how to install and run

## Introduction

I had a broken OLPC XO (stuck keys) so I wanted to use it as a wifi-enabled picture frame.
I tried out various things (via picasa,...) but ended up using feh + wget + !MacMini as a server.

But now I use the [https://developers.google.com/picasa-web/docs/2.0/developers_guide Google Data API] to access my !PicasaWeb albums via [https://developers.google.com/picasa-web/docs/1.0/developers_guide_python python] instead of wget+custom server.

The following are quick-n-dirty instructions to get things going.


# Details
Assumes python 2.7

## One time setups
   * `yum install feh`
   * Setup [app-passwords](http://support.google.com/accounts/bin/answer.py?hl=en&answer=185833) in your Google account. 
   * Setup a netrc with the username/password needed for the Goodle Data API. My script will ask netrc for _picasaweb_ as the machine.

`echo machine picasaweb login ` *you@gmail.com* `  password  ` *the_app_password_generated_above* ` > ~/.netrc`

   * Prepare an album on picasaweb.google.com. The Default is _OLPC XO !PictureFrame2_.

## Getting the script onto the XO and running
   * Upload the scripts and gdata subdirectory into `/home/olpc/olpc-xo-picture-frame` as the scripts assume `picture_frame_sw_dir=/home/olpc/olpc-xo-picture-frame`. I just rsync my git repo with

      {{{ rsync -ra --exclude=.git --exclude=pics ../olpc-xo-picture-frame olpc@192.168.1.102:.}}}

   * Run the script.
      `/home/olpc/olpc-xo-picture-frame/slideshow "" "" "your album name"`<br>
      or add it to your `~/.xsession` (chmod +x'd)

### Sample invocations

   * `slideshow 1 300 "2012-08-20_21 Altea, Spain"`
      * would fetch the _2012-08-20_21 Altea, Spain_
      * delay 1 sec between pics
      * refetch album ever 300 sec.

   * `slideshow`
      * would fetch the default _OLPC XO PictureFrame2_ album
      * delay 1h between pictures
      * reload album every 10 minutes

   * `slideshow 10 "" "2012-08-20_21 Altea, Spain"`
      * would fetch the _2012-08-20_21 Altea, Spain_
      * delay 10 sec between pics
      * refetch album ever 10 minutes
