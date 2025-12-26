# SVD Image Compression (Python)

This project demonstrates image compression using Singular Value Decomposition (SVD) by approximating an image matrix using only the top k singular values (a rank-k approximation). Keeping fewer singular values reduces the amount of information needed to represent the image, trading detail for compression.

______

# How to Run:
1) Install dependencies

`pip install pillow numpy matplotlib`

matplotlib is optional unless you add visualization. The core script only needs pillow + numpy.
___

2) Put an image in the project folder

Example: `input.jpg`

You can also use PNG: `input.png`

___

3) Run the script

`python svd_compress.py`

___

4) (Optional) Change the compression level

k = 50 is the moderate

k = 5 (very strong compression, visible blur)

k = 20 (strong compression)

k = 100 (higher quality)

___

### What the saved image looks like

For small k: smoother / blurrier, fine details disappear first.

For larger k: closer to the original, sharper edges and textures preserved.
___

# Expected Output

When you run the script, a new compressed image file will be created in the project directory.

Example output file:
compressed_k50.png

The terminal will print something similar to:

Saved compressed image to: compressed_k50.png  
Approx. stored numbers ratio (compressed/original): 0.145

The printed ratio is a rough mathematical comparison between:
- the number of values needed to store the original image
- the number of values needed to store the rank-k SVD representation

This ratio does NOT represent the final PNG or JPEG file size, since those formats apply their own compression.

___

# How SVD Image Compression Works

An image can be represented as a matrix of pixel intensities.

Grayscale image:
- 2D matrix of shape (H, W)

RGB image:
- Three 2D matrices (R, G, B), each of shape (H, W)

Singular Value Decomposition (SVD) factorizes a matrix A into:

A = U Σ Vᵀ

Where:
- U contains patterns across rows
- Σ (Sigma) contains singular values that represent the importance of each pattern
- Vᵀ contains patterns across columns

The singular values are sorted from largest to smallest.  
Larger singular values contain more visual information.

To compress the image, we keep only the top k singular values and discard the rest:

A ≈ Uₖ Σₖ Vₖᵀ

This produces the best possible rank-k approximation of the original image.

___

# Function Explanations

## svd_compress_channel(channel_2d, k)

Purpose:  
Compresses a single 2D image channel using rank-k SVD.

Inputs:
- channel_2d: a 2D NumPy array of shape (H, W)
- k: number of singular values to keep

Steps:
1) Compute the SVD of the matrix:
   U, S, Vᵀ = svd(channel_2d)

2) Select only the top k components:
   - Uₖ → first k columns of U
   - Sₖ → first k singular values
   - Vₖᵀ → first k rows of Vᵀ

3) Reconstruct the channel using:
   Uₖ Σₖ Vₖᵀ

Instead of explicitly building the diagonal matrix Σₖ, the implementation multiplies each row of Vᵀ by its corresponding singular value for efficiency.

Output:
- A reconstructed 2D matrix of shape (H, W)

This matrix is an approximation of the original channel with reduced information.

___

## compress_image_svd(input_path, output_path, k)

Purpose:  
Loads an image, applies SVD compression, and saves the result.

Steps:
1) Load the image from disk.
2) Convert it to either grayscale (L) or RGB if needed.
3) Convert pixel values to float for numerical stability.
4) Apply SVD compression:
   - Directly for grayscale images
   - Separately for R, G, and B channels in RGB images
5) Clip reconstructed values to the valid range [0, 255].
6) Convert back to unsigned 8-bit integers.
7) Save the compressed image.

Why RGB channels are compressed separately:
Each color channel is an independent matrix, and SVD works on 2D matrices.  
Compressing channels separately preserves color structure.

___

## estimate_storage_ratio(h, w, k, rgb)

Purpose:  
Estimates how much data is needed to store the SVD representation compared to the original image.

Original storage:
- Grayscale: H × W values
- RGB: H × W × 3 values

Compressed storage per channel:
- U matrix: H × k
- Singular values: k
- Vᵀ matrix: k × W

Total per channel:
Hk + k + kW

The function returns:
compressed_storage / original_storage

This value is for understanding compression efficiency, not actual file size.

___

# Choosing a Good k Value

Small k:
- High compression
- Loss of fine details
- Visible blur

Large k:
- Better image quality
- Less compression

General guideline:
Start with:

k ≈ 5% to 10% of min(H, W)

Then adjust based on visual quality.

Examples:
- Logos / cartoons → smaller k
- Photographs → larger k

___

# Limitations

- This implementation uses full SVD, which can be slow for very large images.
- File size on disk depends on image format compression (PNG, JPEG).
- This approach is mainly educational and demonstrates low-rank approximation.

___

# Summary

This project shows how SVD can be used to:
- Represent images as matrices
- Remove less important information
- Trade visual detail for compression

It demonstrates a fundamental idea used in many compression and dimensionality reduction techniques.

