# Conformal Mapping
A naive first attempt at conformaly mapping images. Given an
image and an *inverse* map it will produce the image under the
map. It works on animated gifs too.

## How it works
Given an inverse map it scans over an empty image and for each pixel
it finds the preimage poit and just copies over the value. This is
why you need to supply an inverse map.

## Examples
Just some examples of what it does to various images. (It likes
tileable images a lot better).

### Static
It can map this ![static-preimage](/images/source.jpg)

To this ![static-image](/images/output.jpg)

### Animated
It also does gifs! Mapping 

![anim-preimage](/images/source.gif)

To this 

![anim-image](/images/output.gif)

## Setting up
This program is based on python 3 and uses 
[pillow](https://pillow.readthedocs.io/en/latest/index.html)
to do all image manipulation.

Easiest way to set up would be to set up pipenv on your machine 
and simply run pipenv install in the directory with the pipfile
as it will set up a virtual enviroment and install all needed
packages for you. See [here](docs.python-guide.org/en/latest/dev/virtualenvs)
if you have no idea what I'm talking about.


## Current issues
Well theres a lot, kind of just threw this together but:
* It's slow. I'm doing the conformal map once per pixel, not sure if I missed some
pillow primitive which might speed it up.
* It's inffecient with file size. The bilinear interpolation doesn't like palettes. 
if you give it a gif it will conver it to RGB. This takes up imense file size, pillow
allows for some palette stuff, I just haven't done it yet.
* Branch cuts are sad. In general I think this isn't fixable, but in the case
of the spiral function in conformal.py it definitely is. Just haven't sorted it out
yet. Currently it makes spirals like this:

![failed branch cut](/images/branchfail.jpg)

