import os
import cv2
from vidaug import augmentors as va
from skimage.io import imsave

def load_batch(batch_idx):
    # Assuming each batch is a separate image file
    image_folder = r"D:\BCIT\ISSP\yolo\ultralytics-main\data\images"  # replace with your actual folder path
    image_files = os.listdir(image_folder)
    image_file = os.path.join(image_folder, image_files[batch_idx])

    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # convert color space from BGR to RGB
    return [image]  # return image as a list to be compatible with the augmentor

#All available augmentors (Note that any flip, crop, or resize augmentor would require the bounding box be changed as well)
""" RandomRotate
    * RandomResize
    * RandomTranslate
    * RandomShear
    * CenterCrop
    * CornerCrop
    * RandomCrop 
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
augmented_dir = r"D:\BCIT\ISSP\yolo\ultralytics-main\data\augmented_images"
os.makedirs(augmented_dir, exist_ok=True)



# Load a batch of images
for batch_idx in range(len(os.listdir(r"D:\BCIT\ISSP\yolo\ultralytics-main\data\images"))):
    image = load_batch(batch_idx)
    image_aug = seq(image)
    # Save augmented image to a new file
    imsave(os.path.join(augmented_dir, f"image_{batch_idx}_aug.jpg"), (image_aug[0]).astype('uint8'))

# Directory containing the images
image_dir = r"D:\BCIT\ISSP\yolo\ultralytics-main\data\augmented_images"

