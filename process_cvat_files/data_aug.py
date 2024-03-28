''''Documentation can be found at https://github.com/okankop/vidaug/tree/master/vidaug/augmentors'''
import os
import cv2
from vidaug import augmentors as va
from skimage.io import imsave

image_folder  = './train_val_dataset/train'
output_folder = './train_val_dataset/augmented_images'

#To do: Load bounding box file location

def load_batch(batch_idx):
    # Assuming each batch is a separate image file
    image_files = os.listdir(image_folder)
    image_file = os.path.join(image_folder, image_files[batch_idx])

    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # convert color space from BGR to RGB
    return [image]  # return image as a list to be compatible with the augmentor

#All available augmentors (Note that any flip, crop, or resize augmentor would require the bounding box be changed as well). Also, all random augmentations are difficult to do when there is a bounding box involved. Maybe do the augmentation while the bounding box doesn't exist?
""" RandomRotate (Random, diffiuclt to manage with bounding box)
    * RandomResize (Random, diffiuclt to manage with bounding box)
    * RandomTranslate (Random, diffiuclt to manage with bounding box)
    * RandomShear (Random, diffiuclt to manage with bounding box)
    * CenterCrop (Bounding box needs to be resized based on image. Note that occasionally the bounding box may be outside the image after cropping. Need to check for this)
    * CornerCrop (Bounding box needs to be resized based on image. Note that occasionally the bounding box may be outside the image after cropping. Need to check for this)
    * RandomCrop  (Bounding box needs to be resized based on image. Note that occasionally the bounding box may be outside the image after cropping. Need to check for this)
    * HorizontalFlip
    * VerticalFlip
    * GaussianBlur
    * ElasticTransformation
    * PiecewiseAffineTransform
    * Superpixel
    * Sequential
    * OneOf
    * SomeOf
    * Sometimes
    * InvertColor
    * Add
    * Multiply
    * Pepper
    * Salt
    * TemporalBeginCrop
    * TemporalCenterCrop
    * TemporalRandomCrop
    * InverseOrder
    * Downsample
    * Upsample
    * TemporalFit
    * TemporalElasticTransformation
    """

sometimes = lambda aug: va.Sometimes(0.5, aug) # Used to apply augmentor with 50% probability
seq = va.Sequential([
    #va.RandomCrop(size=(240, 180)), # randomly crop video with a size of (240 x 180)
    #va.RandomRotate(degrees=10), # randomly rotates the video with a degree randomly choosen from [-10, 10]  
    #sometimes(va.HorizontalFlip()) # horizontally flip the video with 50% probability
    #va.ElasticTransformation(alpha=100, sigma=10)
    #va.Superpixel()
    #va.GaussianBlur(sigma=1.0),
    #va.Superpixel(p_replace=1, n_segments=1000)
])

# Create a new directory for augmented images

os.makedirs(output_folder, exist_ok=True)



# Load a batch of images
for batch_idx in range(len(os.listdir(image_folder))):
    image = load_batch(batch_idx)
    image_aug = seq(image)
    # Save augmented image to a new file
    imsave(os.path.join(output_folder, f"image_{batch_idx}_aug.jpg"), (image_aug[0]).astype('uint8'))



