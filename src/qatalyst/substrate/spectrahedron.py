from typing import Tuple


class SpectrahedronGeometryEngine:
    """Classifies where the system sits relative to the warped stability region."""

    def classify(self, system_energy: float, dynamic_bound: float) -> Tuple[str, float]:
        margin = dynamic_bound - system_energy
        state = "STABLE" if margin > 0 else "WARPED"
        return state, margin
