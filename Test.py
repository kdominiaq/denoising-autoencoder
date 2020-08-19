import torch
from torchvision.utils import save_image
from Dataset import Dataset
from torch import nn
from skimage.util import random_noise
from Params import Params


def image_save(img, name):
    '''
    saves the pics under the given path name
    :param img: tensor size -> torch.Size([1, 3, 32, 96])
    :param name: path name
    :return: none
    '''
    img = img.view(img.size(0), 3, 32, -1) # -1 -> when we dont know about size of width/height -> must be 96
    save_image(img, name)


# test
class Test(Params):
    def __init__(self, device):
        super().__init__()
        self._device = device
        self._criterion_test = nn.MSELoss()
        model = torch.load(self.model_save_PATH)
        model.eval()
        for i, data in enumerate(Dataset.test_loader()):
            # prepare test dataset
            clean_img_test, _ = data[0], data[1]
            noised_img_test = torch.tensor(random_noise(clean_img_test, mode='s&p', salt_vs_pepper=0.5, clip=True))
            clean_img_test, noised_img_test = clean_img_test.to(device), noised_img_test.to(device)

            test_output = model(noised_img_test)
            _, predicted = torch.max(test_output.data, 1)

            all_test = torch.cat((clean_img_test, noised_img_test, test_output), 3)
            image_save(all_test, f"./{i + 1}_all_vs1.png")

            loss_test = + self._criterion_test(test_output, clean_img_test).item()
            if i == self.num_test_images - 1:
                average_loss_test = loss_test / self.num_test_images
                print(f'Average loss: {average_loss_test:.4f}')
                break

