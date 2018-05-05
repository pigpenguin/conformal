import cmath
import math
""" 
Defines some basic conformal maps
"""
def mobius(a,b,c,d):
    """
    Mobius transformation.

    Parameters
    ----------
    a : complex number
    b : complex number
    c : complex number
    d : complex number

    Returns
    -------
    function from C -> C
    """
    return lambda z: (a*z + b)/(c*z + d)

def mobius_inverse(a,b,c,d):
    """
    Inverse of a Mobius transformation.

    Parameters
    ----------
    a : complex number
    b : complex number
    c : complex number
    d : complex number

    Returns
    -------
    function from C -> C
    """
    return lambda z: (d*z - b)/(-c*z + a)

def spiral(height,width,z):
    """
    The inverse of a spiral map.

    This is currenly broken, there is a discontinuity due to a branch
    cut which I think is fixable due to the fact we know something about
    the preimage in theory. 
    
    The idea behind the math is that e^z sends vertical lines to circles,
    so we scale to make it so the diagonal of the image becomes 2pi in 
    length, then rotate the image so the diagonal is vertical. In theory
    then mapping the points forward with e^z should cause the image to 
    spiral.

    This function does all that in reverse:

    log z -> rotate by -phi -> scale mapping 2pi to the length of the diagonal 

    Parameters
    ----------
    height: int
        height of the reigon you want to spiral
    width: int
        width of the reigon you want to spiral
    z: complex
        the image of the spiral map

    Returns
    -------
    complex preimage of z under the spiral
    """
    diagonal = math.sqrt(height**2 + width**2)
    phi = math.atan(float(height/width))
    z = cmath.log(z)
    z = z * cmath.exp(1j*phi)
    z = z * (diagonal/(2*math.pi))
    return z

