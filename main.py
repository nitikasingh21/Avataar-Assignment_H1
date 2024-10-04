# -*- coding: utf-8 -*-
"""Avataar Assignment_H1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14wi70NVivKKqQP8mUwdD5C1tVV68jztd?usp=sharing
"""

!pip install matplotlib 
!pip install numpy 

!pip install diffusers transformers accelerate
!pip install controlnet_aux  # For auxiliary tools like canny and normal map extraction

!pip install mediapipe

!pip install --upgrade controlnet_aux

!pip install diffusers transformers torch torchvision opencv-python pillow

from huggingface_hub import notebook_login
notebook_login()

import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel

# Setting the random seed for reproducibility
torch.manual_seed(12345)

# Loading the ControlNet model trained on depth maps
controlnet_depth = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-depth", torch_dtype=torch.float16)

# Loading the base Stable Diffusion model with ControlNet integration
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet_depth,
    torch_dtype=torch.float16
)

#Moving the model to GPU 
pipe = pipe.to("cuda")

from google.colab import files

uploaded_files = files.upload()

from PIL import Image

# Listing of image filenames
image_files = ['1.png', '2.png', '3.png', '4.png', '5.png']

for image_file in image_files:
    # Loading and resizing the image
    depth_image = Image.open(image_file).convert("RGB")
    depth_image = depth_image.resize((512, 512))

    # Displaying the loaded image
    depth_image.show()

import matplotlib.pyplot as plt

# Listing of image filenames
image_files = ['1.png', '2.png', '3.png', '4.png', '5.png']

# Looping through each image file
for image_file in image_files:
    
    depth_image = Image.open(image_file).convert("RGB")
    depth_image = depth_image.resize((512, 512))

    # Displaying the image using matplotlib
    plt.imshow(depth_image)
    plt.axis('off')  
    plt.title(image_file)  
    plt.show()  

"""Handling npy images"""

import numpy as np

# Loading the NPY files 
npy_data = np.load('6.npy')

npy_data = np.load('7.npy')

# Displaying the shape and content of the loaded NPY file
print(npy_data.shape)  # This will show the dimensions of the data
print(npy_data)        # This will print the actual content 

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Loading the NPY file '6.npy'
npy_data = np.load('6.npy')
print(npy_data.shape)  # To show you the dimensions of the array

# Converting the numpy array to an image
npy_image = Image.fromarray(npy_data.astype(np.uint8))
npy_image = npy_image.resize((512, 512))

# Displaying the NPY image using matplotlib
plt.imshow(npy_image, cmap='gray')  
plt.axis('off')
plt.title("Loaded NPY Image")
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Loading the NPY file '7.npy'
npy_data = np.load('7.npy')
print(npy_data.shape)  # This shows you the dimensions of the array

# Convert the numpy array to an image
# If it's a single-channel depth map, ensure it's in the range [0, 255]
npy_image = Image.fromarray(npy_data.astype(np.uint8))
npy_image = npy_image.resize((512, 512)) #We can resize the image if needed

# Displaying the NPY image using matplotlib
plt.imshow(npy_image, cmap='gray')  
plt.axis('off')
plt.title("Loaded NPY Image")
plt.show()

# Loading the NPY file
npy_data = np.load('6.npy') 

# Converting the numpy array to an image
npy_image = Image.fromarray(npy_data.astype(np.uint8))  

# Resizing the image if needed
npy_image = npy_image.resize((512, 512))

# Displaying the NPY image using matplotlib
plt.imshow(npy_image, cmap='gray')  
plt.axis('off')
plt.title("Loaded NPY Image")
plt.show()

# Generating images using ControlNet
prompt = "A beautiful landscape with mountains"
generated_images = pipe(prompt=prompt, image=npy_image).images

# Displaying the generated images
for idx, image in enumerate(generated_images):
    plt.imshow(image)
    plt.axis('off')
    plt.title(f"Generated Image {idx}")
    plt.show()

# Saving generated images
for idx, image in enumerate(generated_images):
    image.save(f"generated_image_{idx}.png")

prompt = "A serene mountain landscape at sunset"
generated_images = pipe(prompt=prompt, image=npy_image).images
for idx, image in enumerate(generated_images):
    plt.imshow(image)
    plt.axis('off')
    plt.title(f"New Generated Image {idx}")
    plt.show()

# Saving generated images
for idx, image in enumerate(generated_images):
    image.save(f"generated_image_{idx}.png")

prompt = "luxurious bedroom interior"
generated_images = pipe(prompt=prompt, image=npy_image).images

# Displaying the new generated images
for idx, image in enumerate(generated_images):
    plt.imshow(image)
    plt.axis('off')
    plt.title(f"New Generated Image {idx}")
    plt.show()

prompt = "House in the forest"
generated_images = pipe(prompt=prompt, image=npy_image).images

for idx, image in enumerate(generated_images):
    plt.imshow(image)
    plt.axis('off')
    plt.title(f"New Generated Image {idx}")
    plt.show()

"""Removing Depth influence temporarily"""

from diffusers import StableDiffusionPipeline
import torch
import cv2
from PIL import Image
import numpy as np

# Loading the pipeline with float32 precision to avoid dtype mismatch
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float32
).to("cuda")

# Loading the image
input_image_path = "/content/1.png"
image = cv2.imread(input_image_path)

if image is None:
    raise FileNotFoundError(f"Image not found at the specified path: {input_image_path}")

# Converting the image to grayscale for edge detection
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Applying Canny edge detection to the image
edges = cv2.Canny(image_gray, 100, 200)

# Converting the edges to a format suitable for the model (PIL Image)
edges_pil = Image.fromarray(edges)

# Converting the image to a tensor and ensure it's of dtype float32
image_tensor = torch.from_numpy(np.array(edges_pil)).unsqueeze(0).to(torch.float32).to("cuda")

# Defining the prompt
prompt = "A futuristic cityscape at sunset with glowing neon lights"

# Generating images using the conditioned edges
with torch.autocast(device_type='cuda', dtype=torch.float16):
    generated_images = pipe(prompt=prompt, image=image_tensor).images

# Displaying the generated images
for i, img in enumerate(generated_images):
    img.save(f"generated_image_{i}.png")
    img.show()

img.save(f"generated_image_{i}.png")

from PIL import Image
import matplotlib.pyplot as plt

for i in range(len(generated_images)):
    img = Image.open(f"generated_image_{i}.png")
    plt.imshow(img)
    plt.axis('on')  # Show axis labels
    plt.show()

from controlnet_aux import CannyDetector

# Generating Canny edges from the depth image
canny_detector = CannyDetector()
canny_image = canny_detector(npy_image)

# Ensuring canny image is resized
canny_image = canny_image.resize((512, 512))

# Displaying the Canny image using matplotlib
plt.imshow(canny_image, cmap='gray')  
plt.axis('off')
plt.title("Canny Edges")
plt.show()

# Using only the Canny edges for generation
prompt = "A detailed landscape scene with clear outlines"
generated_images = pipe(prompt=prompt, image=canny_image).images

# Displaying the generated images
for idx, image in enumerate(generated_images):
    plt.imshow(image)
    plt.axis('off')
    plt.title(f"Generated Image with Canny Edges {idx}")
    plt.show()

# Prompts for each image
prompts = [
    "A detailed landscape scene with clear outlines for depth image",
    "A detailed landscape scene with clear outlines for canny edges"
]

# Combining images into a list
images = [npy_image, canny_image]

# Ensuring the number of prompts matches the number of images
generated_images = pipe(prompt=prompts, image=images).images

# Displaying the generated images
for idx, image in enumerate(generated_images):
    plt.imshow(image)
    plt.axis('off')
    plt.title(f"Generated Image with Both Inputs {idx}")
    plt.show()

from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from transformers import CLIPProcessor, CLIPModel
import torch

# Loading pre-trained ControlNet model from Hugging Face
controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-depth")

# Loading Stable Diffusion pipeline with ControlNet
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16).to("cuda")

# Setting prompt for generation
prompt = "luxury bedroom interior, mountains in the background, beautiful snowy mountains, beautiful landscape, luxurious bedroom interior, walls with cupboard, room with chair, House in the forest"

"""
Part II
Can we generate images of different aspect ratios (use “Metadata/Nocrop/2_nocrop.png” to test this out) using SD? Comment on the generation quality with respect to the aspect ratio of 1:1 for the same image.
"""

import torch
from diffusers import StableDiffusionPipeline

# Loading the Stable Diffusion pipeline
model_id = "CompVis/stable-diffusion-v1-4"  # We can also use any specific model ID
pipe = StableDiffusionPipeline.from_pretrained(model_id).to("cuda")

from google.colab import files

uploaded_files = files.upload()

from PIL import Image

# Loading the image
image_path = '/content/2_nocrop.png'  # Make sure this path is correct
nocrop_image = Image.open(image_path).convert("RGB")

# Displaying the loaded image
nocrop_image.show()

# Generating images with different aspect ratios
# Trying 3 different examples if aspect ratios and corresponding sizes
aspect_ratios = {
    "1:1": (512, 512),  # Square
    "16:9": (512, 288), # Wide
    "9:16": (288, 512)  # Tall
}

# Generating images for each aspect ratio
generated_images = {}

for ratio, size in aspect_ratios.items():
    # Resizing the original image to the specified size
    resized_image = nocrop_image.resize(size)

    # Generating images using the resized image as input
    prompt = "A beautiful landscape with mountains"  # We can change this prompt as needed
    generated_image = pipe(prompt=prompt, image=resized_image).images[0] 

    # Saving the generated image
    generated_images[ratio] = generated_image

# Displaying the generated images
for ratio, image in generated_images.items():
    plt.imshow(image)
    plt.axis('off')
    plt.title(f"Generated Image - Aspect Ratio {ratio}")
    plt.show()

# Generating multiple images
generated_images = pipe(prompt=prompt, image=resized_image).images

# Accessing the first two generated images
first_two_images = generated_images[0:2]

# Displaying the first two generated images
for idx, img in enumerate(first_two_images):
    plt.imshow(img)
    plt.axis('off')  
    plt.title(f"Generated Image {idx + 1} (Aspect Ratio {ratio})")
    plt.show()

# Generate multiple images using the resized image
generated_images = pipe(prompt=prompt, image=resized_image).images

# Access the first two generated images
first_two_images = generated_images[0:2]

# Displaying the first two generated images
for idx, img in enumerate(first_two_images):
    plt.imshow(img)
    plt.axis('off')  # Hide axis numbers and ticks
    plt.title(f"Generated Image {idx + 1} (Aspect Ratio {ratio})")
    plt.show()

# Defining different prompts altogether for testing
prompts = [
    "A serene mountain landscape with a cabin.",
    "A vibrant sunset over the ocean.",
    "A lush green valley with a river running through.",
    "A futuristic city skyline at night.",
    "A peaceful forest with sunlight filtering through the trees."
]

# Aspect ratios and corresponding sizes
aspect_ratios = {
    "1:1": (512, 512),  # Square
    "16:9": (512, 288), # Wide
    "9:16": (288, 512)  # Tall
}

# Generating images for each aspect ratio and prompt
for prompt in prompts:
    for ratio, size in aspect_ratios.items():
        # Resizing the original image to the specified size
        resized_image = nocrop_image.resize(size)

        # Generating images using the resized image as input and the current prompt
        generated_image = pipe(prompt=prompt, image=resized_image).images[0]  # Get the generated image

        # Displaying the generated image
        plt.imshow(generated_image)
        plt.axis('off')
        plt.title(f"Generated Image - {prompt} (Aspect Ratio {ratio})")
        plt.show()

# `npy_image` is  input depth map and `generated_images` contains the outputs
# Example to check if generated images match the input depth in terms of size and visual characteristics
for idx, generated_image in enumerate(generated_images):
    generated_array = np.array(generated_image)  # Converting generated image to array
    if generated_array.shape != np.array(npy_image).shape:
        print(f"Generated image {idx} has different dimensions from input depth.")
    else:
        # Comparing the generated image with the input depth map
        if np.array_equal(generated_array, np.array(npy_image)):
            print(f"Generated image {idx} matches the input depth map.")
        else:
            print(f"Generated image {idx} does not match the input depth map.")

import numpy as np
from PIL import Image

# Assuming npy_image is loaded and represents the depth map
print("Depth Map Shape:", np.array(npy_image).shape)
print("Depth Map Data Type:", np.array(npy_image).dtype)

# Checking if the depth map is in the correct format (2D array for grayscale)
if np.ndim(npy_image) == 3: 
    npy_image = npy_image[:, :, 0] 

# Ensuring it's the right data type
npy_image = np.clip(npy_image, 0, 255).astype(np.uint8)  # Clip values to 0-255 and convert to uint8

# Generating images for each aspect ratio and prompt
for prompt in prompts:
    for ratio, size in aspect_ratios.items():
        # Resizing the original depth map to the current aspect ratio
        resized_depth_map = Image.fromarray(npy_image).resize(size)

        # Converting the resized depth map to an array
        resized_depth_array = np.array(resized_depth_map)

        # Generating images using the resized image as input and the current prompt
        generated_image = pipe(prompt=prompt, image=resized_image).images[0]  

        # Converting the generated image to an array
        generated_array = np.array(generated_image)

        # Checking if the generated image matches the resized depth map
        if generated_array.shape != resized_depth_array.shape:
            print(f"Generated image for prompt '{prompt}' with aspect ratio {ratio} has different dimensions from resized depth map.")
        else:
            # Comparing the generated image with the resized depth map
            if np.array_equal(generated_array, resized_depth_array):
                print(f"Generated image for prompt '{prompt}' matches the resized depth map.")
            else:
                print(f"Generated image for prompt '{prompt}' does not match the resized depth map.")

# Comparing the generated images with input depth map
for prompt in prompts:
    for ratio, size in aspect_ratios.items():
        # Resizing the original depth map to the current aspect ratio
        resized_depth_map = Image.fromarray(npy_image).resize(size)

        # Converting the resized depth map to an array
        resized_depth_array = np.array(resized_depth_map)

        # Generating images using the resized image as input and the current prompt
        generated_image = pipe(prompt=prompt, image=resized_image).images[0]  

        # Converting the generated image to an array
        generated_array = np.array(generated_image)

        # Dimension matching for 1:1 aspect ratio
        if ratio == "1:1":
            if generated_array.shape != resized_depth_array.shape:
                print(f"Generated image for prompt '{prompt}' with aspect ratio {ratio} has different dimensions from resized depth map.")
            else:
                # Comparing the generated image with the resized depth map
                if np.array_equal(generated_array, resized_depth_array):
                    print(f"Generated image for prompt '{prompt}' matches the resized depth map.")
                else:
                    print(f"Generated image for prompt '{prompt}' does not match the resized depth map.")

# Comparing the generated images with input depth map
for prompt in prompts:
    for ratio, size in aspect_ratios.items():
        # Resizing the original depth map to the current aspect ratio
        resized_depth_map = Image.fromarray(npy_image).resize(size)

        # Converting the resized depth map to an array
        resized_depth_array = np.array(resized_depth_map)

        # Generating images using the resized image as input and the current prompt
        generated_image = pipe(prompt=prompt, image=resized_image).images[0]

        # Converting the generated image to an array
        generated_array = np.array(generated_image)

        # Printing dimensions for debugging
        print(f"Generated Image Shape: {generated_array.shape}, Resized Depth Map Shape: {resized_depth_array.shape}")

        # Dimension matching for 1:1 aspect ratio
        if ratio == "1:1":
            if generated_array.shape != resized_depth_array.shape:
                print(f"Generated image for prompt '{prompt}' with aspect ratio {ratio} has different dimensions from resized depth map.")
            else:
                # Comparing the generated image with the resized depth map
                if np.array_equal(generated_array, resized_depth_array):
                    print(f"Generated image for prompt '{prompt}' matches the resized depth map.")
                else:
                    print(f"Generated image for prompt '{prompt}' does not match the resized depth map.")

"""The entire code at once for easy understanding"""

import numpy as np

# Loading both npy files
depth_map_1 = np.load('/content/6.npy')
depth_map_2 = np.load('/content/7.npy')

# Printing shapes and types to check
print("Depth Map 1 Shape:", depth_map_1.shape)
print("Depth Map 1 Data Type:", depth_map_1.dtype)

print("Depth Map 2 Shape:", depth_map_2.shape)
print("Depth Map 2 Data Type:", depth_map_2.dtype)

import torch
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Setting the random seed for reproducibility
torch.manual_seed(12345)

# Loading the ControlNet model trained on depth maps
controlnet_depth = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-depth", torch_dtype=torch.float16)

# Loading the base Stable Diffusion model with ControlNet integration
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    controlnet=controlnet_depth,
    torch_dtype=torch.float16
)
# Loading depth map input image
npy_image = np.load('/content/6.npy')  # Replace with your actual depth map file
nocrop_image = Image.open("2_nocrop.png").convert("RGB")

# Defining prompts and aspect ratios
prompts = [
    "A serene mountain landscape with a cabin.",
    "A vibrant sunset over the ocean.",
    "A lush green valley with a river running through.",
    "A futuristic city skyline at night.",
    "A peaceful forest with sunlight filtering through the trees."
]

aspect_ratios = {
    "1:1": (512, 512),  # Square
    "16:9": (512, 288), # Wide
    "9:16": (288, 512)  # Tall
}

# Generating images for each aspect ratio and prompt
generated_images = []

for prompt in prompts:
    for ratio, size in aspect_ratios.items():
        # Resizing the original image to the specified size
        resized_image = nocrop_image.resize(size)

        # Generating images using the resized image as input and the current prompt
        generated_image = pipe(prompt=prompt, image=resized_image).images[0]  # Get the generated image
        generated_images.append(generated_image)

        # Displaying the generated image
        plt.imshow(generated_image)
        plt.axis('off')
        plt.title(f"Generated Image - {prompt} (Aspect Ratio {ratio})")
        plt.show()

        # Resizing the depth map to match the generated image's aspect ratio
        resized_depth_map = Image.fromarray(npy_image).resize(size)
        resized_depth_array = np.array(resized_depth_map)

        # Converting the generated image to an array
        generated_array = np.array(generated_image)

        # Printing shapes for debugging
        print(f"Generated Image Shape: {generated_array.shape}, Resized Depth Map Shape: {resized_depth_array.shape}")

        # Checking for dimension matching only for 1:1 aspect ratio
        if ratio == "1:1":
            if generated_array.shape[:2] != resized_depth_array.shape:
                print(f"Generated image for prompt '{prompt}' with aspect ratio {ratio} has different dimensions from resized depth map.")
            else:
                # Comparing the generated image with the resized depth map
                if np.array_equal(generated_array[:, :, 0], resized_depth_array):  # Compare only the first channel
                    print(f"Generated image for prompt '{prompt}' matches the resized depth map.")
                else:
                    print(f"Generated image for prompt '{prompt}' does not match the resized depth map.")
        else:
            # Checking for dimension matching of other aspect ratios
            if generated_array.shape != resized_depth_array.shape:
                print(f"Generated image for prompt '{prompt}' with aspect ratio {ratio} has different dimensions from resized depth map.")

# Comparing generated images with input depth map
for prompt in prompts:
    for ratio, size in aspect_ratios.items():
        # Resizing the original depth map to the current aspect ratio
        resized_depth_map = Image.fromarray(npy_image).resize(size)

        # Converting the resized depth map to an array
        resized_depth_array = np.array(resized_depth_map)

        # Generating images using the resized image as input and the current prompt
        generated_image = pipe(prompt=prompt, image=resized_image).images[0]

        # Converting the generated image to an array
        generated_array = np.array(generated_image)

        # Printing shapes for debugging
        print(f"Generated Image Shape: {generated_array.shape}, Resized Depth Map Shape: {resized_depth_array.shape}")

        # Handling 1:1 aspect ratio - Comparing only the first channel of RGB with the depth map
        if ratio == "1:1":
            if generated_array.shape[:2] != resized_depth_array.shape:
                print(f"Generated image for prompt '{prompt}' with aspect ratio {ratio} has different dimensions from resized depth map.")
            else:
                # Grayscale comparison
                if np.array_equal(generated_array[:, :, 0], resized_depth_array):
                    print(f"Generated image for prompt '{prompt}' matches the resized depth map.")
                else:
                    print(f"Generated image for prompt '{prompt}' does not match the resized depth map.")
        else:
            # For other aspect ratios, we expect different dimensions and don't compare content
            print(f"Generated image for prompt '{prompt}' with aspect ratio {ratio} has different dimensions from resized depth map.")

''' Part III'''

# Checking the latency
import time

# Function to generate an image and calculate the latency
def generate_image_with_latency(prompt, depth_image_path):
    depth_image = Image.open(depth_image_path).convert("L").resize((512, 512))  # Load and resize depth image

    # Starting the timer
    start_time = time.time()

    # Generating the image
    generated_image = pipe(prompt=prompt, image=depth_image).images[0]

    # Ending the timer
    end_time = time.time()

    # Calculating the latency
    latency = end_time - start_time
    print(f"Latency for prompt '{prompt}': {latency:.2f} seconds")

    return generated_image

# Example usage for latency measurement
prompt = "A serene mountain landscape with a cabin."
depth_image_path = "path/to/depth_image.png"  # Path to your depth image

# Generate the image and calculate latency
generated_image = generate_image_with_latency(prompt, depth_image_path)

# Optionally, display the generated image
generated_image.show()
