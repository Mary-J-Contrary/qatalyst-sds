import torch
from typing import Tuple


class GodelMetaCritic:
    """Evaluates proposal variance; squashes if > 0.08."""

    def __init__(self, max_variance: float = 0.08):
        self.max_variance = max_variance

    def critique(self, proposal: torch.Tensor) -> Tuple[torch.Tensor, float]:
        variance = float(torch.var(proposal))
        if variance > self.max_variance:
            adjusted = (proposal * 0.6) + (0.4 * 0.5)
            return adjusted, variance
        return proposal, variance
