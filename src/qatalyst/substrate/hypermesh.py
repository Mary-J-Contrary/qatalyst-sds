import torch
from typing import Dict
from qatalyst.shared import DEVICE, DTYPE


class HyperMeshEngine:
    """Triadic causal state representation for advanced context."""

    def build_triads(self, telemetry: Dict[str, float]) -> torch.Tensor:
        triad_1 = torch.tensor(
            [telemetry["T_norm"], telemetry["E"], telemetry["policy"]],
            dtype=DTYPE,
            device=DEVICE,
        )
        triad_2 = torch.tensor(
            [telemetry["trust"], telemetry["latency"], telemetry["cost"]],
            dtype=DTYPE,
            device=DEVICE,
        )
        return torch.cat([triad_1, triad_2], dim=0)
