import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float32

torch.set_default_device(DEVICE)
torch.set_default_dtype(DTYPE)
