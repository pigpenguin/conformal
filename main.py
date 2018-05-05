from PIL import Image, ImageSequence
from tiled import apply_map
from conformal import spiral
"""
Boring file loading stuff used to calle the
stuff from tiled and conformal
"""

input_file = "source.jpg"
output_file = "output.png"
# Not gifs
output_size = (512,512)
# Gifs
#output_size = (256,256)

input_image = Image.open(input_file)

conformal_map = lambda z : spiral(input_image.height,input_image.width,z)
#conformal_map = mobius_inverse(1,-1j,1,1j)

if input_image.format == "GIF":
    # Currently produces bloated files, the linear 
    # interpolation does not like working with a 
    # a palette so this does everything in rgb
    # at the end should realy convert to a palette
    # again to save space
    frames = []
    index = 0
    for frame in ImageSequence.Iterator(input_image):
        index += 1
        print("Computing frame:", index)
        output = apply_map(input_image,output_size,conformal_map)
        frames.append(output)
    
    # All of this just facilitates animation
    # Save every frame one after the other
    # Loop forever
    # 33 miliseconds per frame: 30fps
    frames[0].save(output_file,
                   save_all=True,
                   append_images=frames[1:],
                   loop=0,
                   duration=33)
else:
    apply_map(input_image,output_size,conformal_map).save(output_file)

print("done")
