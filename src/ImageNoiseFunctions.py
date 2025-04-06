# Implements Gaussian blur and occlusion noise functions for image data augmentation, 
# specifically designed for evaluating model robustness to image noise (e.g., for VQA benchmarks).
# Intended as proof-of-concept code for GSoC Proposal.

import numpy as np         # For numerical operations and image representation
import cv2 as cv           # OpenCV library for image processing tasks
import os                  # To check if file path exists

# --- Helper Function ---

def _load_image(img_input: str | np.ndarray) -> np.ndarray:
    """Loads an image, handling both file paths and existing NumPy arrays."""
    if isinstance(img_input, str):
        if not os.path.exists(img_input):
             raise FileNotFoundError(f"Image file not found at: {img_input}")
        img = cv.imread(img_input)
        if img is None:
            raise IOError(f"Failed to read image file (OpenCV returned None): {img_input}")
    elif isinstance(img_input, np.ndarray):
        img = img_input.copy() # Work on a copy to avoid modifying the original array in-place
    else:
        raise TypeError("Input must be a file path (str) or a NumPy ndarray.")

    # Validate basic image properties
    if not (img.ndim == 2 or img.ndim == 3):
             raise ValueError(f"Input NumPy array has unexpected dimensions: {img.ndim}. Expected 2 (grayscale) or 3 (color).")
    if img.size == 0:
        raise ValueError("Input image is empty.")
        
    return img

# --- Noise Functions ---

def apply_gaussian_blur(img_input: str | np.ndarray, blur_level: str) -> np.ndarray:
    """
    Applies Gaussian Blur to an image based on predefined levels.

    Args:
        img_input (str | np.ndarray): Path to the input image or the image as a NumPy array.
        blur_level (str): Level of Gaussian blur ("low", "medium", "high").

    Returns:
        np.ndarray: The blurred image as a NumPy array.

    Raises:
        FileNotFoundError: If image path does not exist.
        IOError: If image file fails to load.
        ValueError: If invalid blur_level is provided or image structure is invalid.
        TypeError: If img_input is not str or np.ndarray.
    """
    img = _load_image(img_input)

    # Map blur_level string to sigma value for GaussianBlur
    match blur_level:
        case "low":
            sigma = 1.0   # Per GSoC plan: Slight softening
        case "medium":
            sigma = 3.0   # Per GSoC plan: Noticeable blur, some detail loss
        case "high":
            sigma = 6.0   # Per GSoC plan: Significant blur, major detail loss
        case _:
            raise ValueError("Invalid blur_level. Choose 'low', 'medium', or 'high'.")
    
    # Apply Gaussian Blur. Using ksize=(0, 0) lets sigma accurately control the blur.
    # This is the standard OpenCV practice for sigma-driven blurring.
    blurred_img = cv.GaussianBlur(img, ksize=(0, 0), sigmaX=sigma, sigmaY=sigma)

    return blurred_img

def apply_occlusion(img_input: str | np.ndarray, occlusion_level: str) -> np.ndarray:
    """
    Applies a rectangular occlusion patch to a random part of the image.
    The patch color is the mean color of the image.

    Args:
        img_input (str | np.ndarray): Path to the input image or the image as a NumPy array.
        occlusion_level (str): Relative size of the occlusion ("low", "medium", "high").

    Returns:
        np.ndarray: The image with occlusion as a NumPy array.

    Raises:
        FileNotFoundError: If image path does not exist.
        IOError: If image file fails to load.
        ValueError: If invalid occlusion_level is provided or image structure is invalid.
        TypeError: If img_input is not str or np.ndarray.
    """
    img = _load_image(img_input)
    img_height, img_width = img.shape[:2]

    # Map occlusion_level string to area ratio
    match occlusion_level:
        case "low":
            ratio = 0.08   # Per GSoC plan: Occlude 8% of image area
        case "medium":
            ratio = 0.20   # Per GSoC plan: Occlude 20% of image area
        case "high":
            ratio = 0.40   # Per GSoC plan: Occlude 40% of image area
        case _:
            raise ValueError("Invalid occlusion_level. Choose 'low', 'medium', or 'high'.")
    
    # Calculate patch dimensions to cover the target area ratio
    # while maintaining the original image's aspect ratio for the patch shape.
    patch_h = int(np.sqrt(ratio) * img_height)
    patch_w = int(np.sqrt(ratio) * img_width)

    # Ensure patch dimensions are at least 1 pixel.
    patch_h = max(1, patch_h)
    patch_w = max(1, patch_w)

    # Generate random top-left corner (x, y) for the patch, ensuring it stays within bounds.
    # Subtract patch dimensions to prevent drawing outside image borders. Max with 0 handles cases where patch dimensions match image dimensions.
    max_y = max(0, img_height - patch_h)
    max_x = max(0, img_width - patch_w)
    # np.random.randint is exclusive of the high value, so add 1 to include max_y/max_x.
    start_y = np.random.randint(0, max_y + 1) 
    start_x = np.random.randint(0, max_x + 1) 
    
    # Calculate end coordinates (exclusive in slicing, inclusive in drawing)
    end_y = start_y + patch_h
    end_x = start_x + patch_w

    # Use the mean color of the image for the occlusion patch for less visual jarring.
    # cv.mean returns (B_mean, G_mean, R_mean, Alpha_mean if exists)
    mean_color = cv.mean(img) 
    
    # Draw the filled rectangle (-1 thickness) onto the image copy
    # Note: This modifies the 'img' array which is already a copy ensured by _load_image.
    cv.rectangle(img, pt1=(start_x, start_y), pt2=(end_x, end_y), color=mean_color, thickness=-1) 

    return img # Return the modified image array

# --- Example Usage ---
if __name__ == "__main__":
    print("Running Image Noise Functions Example...")

    # --- Configuration ---
    # Replace 'path/to/your/test/image.jpg' with an actual path to test, otherwise uses a dummy image.
    example_image_path = None #'assets/test_image.jpg' # Example using a subfolder
    use_gui = True # Set to False if running in an environment without GUI support (e.g., some servers)
    # --- End Configuration ---

    img_input_source = ""
    try:
        if example_image_path and os.path.exists(example_image_path):
             img_input = example_image_path
             img_input_source = f"file: {example_image_path}"
             print(f"Using image from: {example_image_path}")
        else:
             print("Example image path not found or not provided. Creating a dummy gradient image.")
             dummy_img = np.zeros((300, 400, 3), dtype=np.uint8)
             dummy_img[:, :200] = [255, 0, 0]  # Blue on left
             dummy_img[:, 200:] = [0, 0, 255]  # Red on right
             img_input = dummy_img
             img_input_source = "dummy gradient"

        print("\nAttempting Low Blur...")
        blurred_low = apply_gaussian_blur(img_input, "low")
        print("-> Applied Low Blur successfully.")
        if use_gui: cv.imshow("Low Blur", blurred_low)

        print("\nAttempting High Occlusion...")
        occluded_high = apply_occlusion(img_input, "high")
        print("-> Applied High Occlusion successfully.")
        if use_gui: cv.imshow("High Occlusion", occluded_high)

        print("\nAttempting Medium Occlusion then Medium Blur...")
        occluded_medium = apply_occlusion(img_input, "medium") # apply_occlusion returns modified copy
        blurred_and_occluded = apply_gaussian_blur(occluded_medium, "medium") # apply blur to occluded copy
        print("-> Applied Medium Occlusion then Medium Blur successfully.")
        if use_gui: cv.imshow("Medium Occlusion then Medium Blur", blurred_and_occluded)

        if use_gui:
            print("\nPress any key in an image window to close all windows.")
            cv.waitKey(0) # Wait indefinitely for a key press
            cv.destroyAllWindows() # Close windows
            print("Windows closed.")
        else:
            print("\nGUI disabled. Example finished.")

    except (FileNotFoundError, IOError, ValueError, TypeError) as e:
        print(f"\n--- ERROR ---")
        print(f"An error occurred during the example execution with source '{img_input_source}':")
        print(f"{type(e).__name__}: {e}")
        print("---------------")
    except ImportError:
        print("\n--- ERROR ---")
        print("OpenCV (cv2) or NumPy does not seem to be installed.")
        print("Please install them: pip install opencv-python numpy")
        print("---------------")