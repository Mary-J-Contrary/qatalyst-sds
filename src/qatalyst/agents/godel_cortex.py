import torch
from qatalyst.shared import DEVICE, DTYPE


class GodelAgent:
    """
    Gödel Cortex - 1.5x Panic Factor & Non-linear warping.
    """

    BASELINE = 0.50
    PANIC_MULTIPLIER = 1.5

    def synthesize_routing(self, hypermesh_state: torch.Tensor) -> torch.Tensor:
        stress_signal = float(torch.mean(hypermesh_state))
        panic_factor = stress_signal * self.PANIC_MULTIPLIER

        angles = torch.tensor([1.1, 0.9, 0.4, 1.2], device=DEVICE, dtype=DTYPE)
        sin_vals = torch.sin(angles)
        cos_vals = torch.cos(angles)

        base = self.BASELINE
        action_vector = torch.tensor(
            [
                base + panic_factor * sin_vals[0].item(),
                base - panic_factor * cos_vals[1].item(),
                base + panic_factor * 0.8,
                base - panic_factor * 0.8,
                base + panic_factor * sin_vals[2].item(),
                base - panic_factor * cos_vals[3].item(),
            ],
            dtype=DTYPE,
            device=DEVICE,
        )

        return torch.clamp(action_vector, 0.0, 1.0)
