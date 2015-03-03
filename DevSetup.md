# Introduction #

This is a quick description of what my development environment looks like.

# Details #
On my laptop, I keep all the scripts and needed python libraries in one directory which makes testing locally as easy as
```
export PYTHONPATH=.:~+/gdata-2.0.17/src
picasaweb.py
```



I pushed my ssh pub key to the various OLPCs I use

```
scp /home/jpa/.ssh/id_dsa.pub olpc@192.168.1.113:.ssh/authorized_keys
```
Of course followed by
```
chmod go-rwx ~olpc/.ssh ~olpc/.ssh/authorized_keys
```
on the OLPC.

I enabled sshd on the OLPC-XO with
` chkconfig sshd on ; service sshd restart `

This allows to rsync everything over
`  rsync -ra --exclude=.git --exclude=pics ../olpc-xo-picture-frame olpc@192.168.1.113:. `

Of course the ` ~/.netrc ` is not the same on each device.