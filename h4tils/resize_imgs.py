import os
import fire
from PIL import Image
from joblib import Parallel, delayed
from .misc import get_project_path, timer


def load_resize_save(size, img_path, save_path):
    """Loads and image, resize it and saves it.

    Parameters
    ----------
    size : int
        pixel width and height of the new image.
        NOTE: the new images are going to be square.
    img_path : str
        Path to the image to load.
    save_path : str
        Path to save the resized image.
    """
    img_name = os.path.basename(img_path)
    img = Image.open(img_path).resize((size, size))
    img.save(os.path.join(save_path, img_name))


@timer
def resize_imgs(size, imgs_set_paths, save_path):
    """Function that resizes a set of images in a folder in parallel.

    Parameters
    ----------
    size : int
        Dimension of the width / height of the image.
        NOTE: the images are going to be square.
    imgs_set_paths : list of strings
        List containing the paths of each image.
    save_path : str
        Path to the folder where the new images are going to be saved.
    """
    Parallel(n_jobs=-1, verbose=10)(delayed(load_resize_save)(size, img_path, save_path)
                                    for img_path in imgs_set_paths)

