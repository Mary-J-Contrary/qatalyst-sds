import torch
from typing import List
from qatalyst.shared import DEVICE, DTYPE


class HCA1_Substrate:
    """Holomorphic Compute Architecture (HCA-1). Zero-copy state array."""

    def __init__(self, entities: int = 1000):
        self.entities = entities
        self.state_tensor = torch.zeros((entities, 6), device=DEVICE, dtype=DTYPE)
        self.memory_pool = bytearray(entities * 6 * 4)
        print(f"[*] HCA-1 Substrate: {entities} nodes allocated on {DEVICE}")

    def upsert_telemetry(self, entity_id: int, vector: List[float]) -> None:
        with torch.no_grad():
            self.state_tensor[entity_id] = torch.tensor(
                vector, device=DEVICE, dtype=DTYPE
            )
