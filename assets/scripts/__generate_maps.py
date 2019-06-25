from glob import glob
import os
from PIL import Image
from pathlib import Path

def generate_minimaps(style = "native"):
    """
    See available styles on
    https://help.farbox.com/pygments.html
    """
    wdir = os.path.dirname(os.path.realpath(__file__))
    files = glob(os.path.join(wdir, "*.py"))
    files.remove(os.path.join(wdir, "__minimap.py"))
    files.remove(os.path.join(wdir, "__generate_maps.py"))
    script = os.path.join(wdir, "__minimap.py")

    for fname in files:
        fname = Path(fname) # type: Path
        imgpath = os.path.join(fname.parent.parent, "img/software", fname.name + ".png")
        os.system("python3 {} {} -o {} -w 20 -h 20 --overwrite -s {}".format(script, fname, imgpath, style))
        imageObject = Image.open(imgpath)
        cropped = imageObject.crop((0, 0, 500, 500))
        cropped.save(imgpath)

if __name__ == "__main__":
    generate_minimaps(style = "friendly")
