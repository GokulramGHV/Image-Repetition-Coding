import matplotlib.image as image
from PIL import Image
import random

img_name = "dog.png"
img = Image.open(img_name)
thresh = 200
fn = lambda x: 255 if x > thresh else 0
r = img.convert("L").point(fn, mode="1")
r.save(f"{img_name.split('.')[0]}_bw.png")

img_bw = image.imread(f"{img_name.split('.')[0]}_bw.png")
print(img_bw.shape)


def flip(bit, probablity):  # filps the bit with probability
    if probablity > random.random():
        return not bit
    else:
        return bit


def induce_error(img_bw, probablity):
    img_bw_copy = img_bw.copy()
    for i in range(img_bw.shape[0]):
        for j in range(img_bw.shape[1]):
            img_bw_copy[i][j] = flip(img_bw[i][j], probablity)
    return img_bw_copy


def count_error(l):
    return round(sum(l) / len(l))


def generate_img_lst(num_of_imgs, probablity):
    img_lst = []
    for i in range(num_of_imgs):
        img_lst.append(induce_error(img_bw, probablity))
    return img_lst


def generate_final_img(img_lst):
    img_final = image.imread(f"{img_name.split('.')[0]}_bw.png")
    for i in range(img_final.shape[0]):
        for j in range(img_final.shape[1]):
            img_final[i][j] = count_error([img[i][j] for img in img_lst])
    return img_final


img_lst = generate_img_lst(5, 0.15)
print(len(img_lst))
for i, img in enumerate(img_lst):  # save the images
    image.imsave(f"{img_name.split('.')[0]}_bw_error_{i}.png", img, cmap="gray")
img_final = generate_final_img(img_lst)
image.imsave(f"{img_name.split('.')[0]}final.png", img_final, cmap="gray")
