import numpy as np
from PIL import Image

def svd_compress_channel(channel_2d: np.ndarray, k: int) -> np.ndarray:
    """
    channel_2d: (H, W) float array
    returns: (H, W) float array reconstructed from rank-k SVD
    """
    U, S, Vt = np.linalg.svd(channel_2d, full_matrices=False)
    k = max(1, min(k, S.shape[0]))

    Uk = U[:, :k]
    Sk = S[:k]
    Vtk = Vt[:k, :]
    return Uk @ (Sk[:, None] * Vtk)


def compress_image_svd(input_path: str, output_path: str, k: int) -> None:
    """
    Loads an image, applies rank-k SVD compression, saves result.
    Works for grayscale ('L') and RGB images.
    """
    img = Image.open(input_path)

    if img.mode not in ("L", "RGB"):
        img = img.convert("RGB")

    arr = np.asarray(img).astype(np.float32)

    if arr.ndim == 2:  
        recon = svd_compress_channel(arr, k)
        recon = np.clip(recon, 0, 255).astype(np.uint8)
        out = Image.fromarray(recon, mode="L")

    else:
        channels = []
        for c in range(3):
            recon_c = svd_compress_channel(arr[:, :, c], k)
            channels.append(recon_c)
        recon = np.stack(channels, axis=2)
        recon = np.clip(recon, 0, 255).astype(np.uint8)
        out = Image.fromarray(recon, mode="RGB")

    out.save(output_path)
    print(f"Saved compressed image to: {output_path}")


def estimate_storage_ratio(h: int, w: int, k: int, rgb: bool) -> float:
    """
    Rough storage comparison (not counting file encoding like PNG/JPEG):
    Original stores H*W*(1 or 3) numbers.
    Rank-k SVD stores U (H*k) + S (k) + Vt (k*W) per channel.
    """
    channels = 3 if rgb else 1
    original = h * w * channels
    compressed = channels * (h * k + k + k * w)
    return compressed / original


if __name__ == "__main__":

    input_path = "input.jpg"
    output_path = "compressed.png"
    k = 50

    compress_image_svd(input_path, output_path, k)

    img = Image.open(input_path)
    rgb = (img.convert("RGB").mode == "RGB")
    w, h = img.size
    ratio = estimate_storage_ratio(h, w, k, rgb=rgb)
    print(f"Approx. stored numbers ratio (compressed/original): {ratio:.3f}")
