import numpy as np
from PIL import Image
from torch.utils.data import Dataset


class ImageLoader(Dataset):
    def __init__(self, imgs_path, targets=None, transform=None):
        """Returns and image and target (if give) by its index.

        Parameters
        ----------
        imgs_path : list of str
            List containing the paths to the images.
        targets : iterable, default None
            Iterable containing the correspondig targets.
            If `None` then no target will be extracted and
            `None` will be returned. This behaviour corresponds
            as if the data was from the test set.
        transform : albumentations.core.composition.Compose
            Transformations that are going to be applied over
            the selected image.

        Returns
        -------
        sample : dict
            Dictionary containing two keys `input` for the inputs
            and `target` for the corresponding target."""
        self.imgs_path = imgs_path
        self.targets = targets
        self.transform = transform

    def __len__(self):
        return len(self.imgs_path)

    def __getitem__(self, idx):
        img = Image.open(self.imgs_path[idx])
        img = np.array(img)

        # Assign a target if exists.
        if self.targets is not None:
            target = self.targets[idx]
        else:
            target = None

        if self.transform is not None:
            img = self.transform(image=img)
            img = img["image"]

        img = np.transpose(img, (2, 0, 1)).astype(np.float32)

        if target is not None:
            sample = {"input": img,
                      "target": target}
        else:
            sample = {"input": img}

        return sample
