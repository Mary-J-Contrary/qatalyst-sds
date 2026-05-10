class MetabolicScheduler:
    """strictness = 0.90 + (0.35 * stress)"""

    def compute_law_strictness(self, temp_norm: float, tension: float) -> float:
        stress = (temp_norm * 0.5) + (tension * 0.5)
        strictness = 0.90 + (0.35 * stress)
        return strictness
