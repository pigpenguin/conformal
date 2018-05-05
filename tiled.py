from math import floor
from PIL import Image
"""
Implements a tiled image with bilinear interpolation
and a function for mapping over them.
"""

class Tiled:
    """
    Tiled image with bilinear interpolation.

    Simple wrapper which provides two main
    functionalities. Using modular arithmetic 
    to mimic tiling behavior, using bilinear
    interpolation to fill gaps between pixels.
    
    The end result is an image which you can 
    get a pixel value for any complex coordinate.

    The type of pixel it returns is based on the
    source image provided, also important to note
    images are adressed "upside down". Upper left
    is (0,0), bottom right is (width,height).
    """
    def __init__(self, im,scale=None,translate=None):
        """
        Create a tileable image

        Parameters
        ----------
        im: image
            the base image which will be tiled
        scale: float
            how much of the complex plane does the image fill
        translate: complex
            where is the center of the image located
        """
        self.__source = im
        self.__translate = -0.5 * complex(im.width,im.height)

        if scale:
            self.__scale = scale
        else:
            self.__scale = min(im.width,im.height)

        if translate:
            self.__translate += translate
         

    def __get_x(self, x):
        """
        Gets the x value of the source image.

        Given an x coordinate of a point in 'global'
        space convert it to an x coordinate from the
        source image.

        Parameters
        ----------
        x : int

        Returns
        -------
        int
        """
        return x % (self.__source.width)

    def __get_y(self, y):
        """
        Gets the y value of the source image.

        Given a y coordinate of a point in 'global'
        space convert it to a y coordinate from the
        source image.

        Parameters
        ----------
        y : int

        Returns
        -------
        int
        """
        return y % (self.__source.height)

    def get_pixel(self, coord):
        """
        Given a coordinate returns the pixel at that point.

        Given a pixel coordinate of a point in 'global'
        space converts it to a pixel coordinate point in 
        'source' space and then returns the pixel at that
        coordinate in the source image.

        Parameters
        ----------
        coord : Tuple of integers

        Returns
        -------
        pixel
        """
        x = self.__get_x(coord[0])
        y = self.__get_y(coord[1])
        return self.__source.getpixel((x,y))

    def bilinear(self, z):
        """
        Bilinear interpolation to grab points.

        Takes a complex coordinate in 'global'
        space, and returns the pixel value at that
        point, using bilinear interpolation to pick
        a value.

        Parameters
        ----------
        z : complex

        Returns
        -------
        pixel
        """
        z = z*self.__scale
        z += self.__translate
        x, y = z.real, z.imag
        x1, y1 = int(floor(x)), int(floor(y))
        x2, y2 = x1+1, y1+1
        left = lerp(self.get_pixel((x1,y1)), self.get_pixel((x1, y2)), y)
        right = lerp(self.get_pixel((x2,y1)), self.get_pixel((x2,y2)), y)
        return lerp(left, right, x)

def lerp(lower, upper, coord):
    """
    Linear interpolation.

    Given an upper and lower value and a coordinate between
    them interpolate between them. The assumption is that
    lower and upper are the values at two adjacent integer
    values thus the fractional part will tell you how close
    you are to the upper coordinate.

    Parameters
    ----------
    lower : number
    upper : number

    Return
    ------
    number
    """
    if isinstance(lower, tuple):
        # If is a tuple interpolate each value
        return tuple([lerp(c, d, coord) for c, d in zip(lower,upper)])
    ratio = coord % 1
    return int(round(lower * (1.0-ratio) + upper * ratio))


def apply_map(source, size, function,scale=None,translate=None):
    """
    Applys the inverse map of a provided function to
    an image. 

    This is really slow, can probably be made faster.
    Also meaning to implement the ability to define
    the "output window". Currently I mulitply and add
    to the preimage variable to scale and move around
    the output.

    Parameters
    ----------
    source : Image
        The source image
    size : Int tuple
        The size of the output image.
    function : complex map

    Returns
    -------
    Image
    """
    source = source.convert("RGB")
    tiled = Tiled(source,scale = 2)
    output = Image.new("RGB",size)
    
    if not scale:
        scale = min(output.width,output.height)

    if not translate:
        translate = -0.5 * complex(output.width,output.height)
    else:
        translate += -0.5 * complex(output.width,output.height)

    for x in range(0,output.width):
        for y in range(0,output.height):
            try:
                image = (complex(x,y)+translate)/scale
                preimage = function(image)
                pixel = tiled.bilinear(preimage)
            except (ZeroDivisionError, ValueError):
                # This happens occasionally, there are probably better
                # ways to handle it (averaging the border of tiling 
                # comes to mind)
                pixel = (0,0,0)
            output.putpixel((x,y), pixel)
    return output
