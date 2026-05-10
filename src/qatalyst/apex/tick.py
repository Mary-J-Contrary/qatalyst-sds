from typing import Dict
import torch
from qatalyst.substrate.hca1 import HCA1_Substrate
from qatalyst.substrate.hypermesh import HyperMeshEngine
from qatalyst.substrate.scheduler import MetabolicScheduler
from qatalyst.substrate.spectrahedron import SpectrahedronGeometryEngine
from qatalyst.agents.godel_cortex import GodelAgent
from qatalyst.agents.meta_critic import GodelMetaCritic
from qatalyst.governance.sovereign_vault import SimulatedSovereignVault
from qatalyst.governance.ledger import CognitiveLedger

substrate, hypermesh = HCA1_Substrate(), HyperMeshEngine()
scheduler, vault = MetabolicScheduler(), SimulatedSovereignVault()
cortex, critic = GodelAgent(), GodelMetaCritic()
spectra, ledger = SpectrahedronGeometryEngine(), CognitiveLedger()


def run_qatalyst_tick(temp: float, tension: float):
    temp_norm = temp / 100.0
    telemetry = {
        "T_norm": temp_norm,
        "E": tension,
        "policy": tension,
        "trust": 0.5,
        "latency": 0.1,
        "cost": temp_norm,
    }
    substrate.upsert_telemetry(0, [0.1, 0.5, 0.1, 0.1, tension, temp_norm])
    hyper_state = hypermesh.build_triads(telemetry)
    raw_proposal = cortex.synthesize_routing(hyper_state)
    proposal_adjusted, proposal_var = critic.critique(raw_proposal)
    law_strictness = scheduler.compute_law_strictness(temp_norm, tension)
    is_safe, proof, action_hash, total_energy, dynamic_bound = (
        vault.generate_stability_proof(
            proposal_adjusted, temp_norm, tension, law_strictness
        )
    )
    region, margin = spectra.classify(total_energy, dynamic_bound)

    if is_safe:
        status = "🟢 EXECUTED"
        verdict = "STABLE CORE"
        action_code = "EXECUTE_WITHIN_BOUNDARY"
    else:
        status = "🔴 ANNIHILATED"
        verdict = "NULL SPACE"
        action_code = "ROLLBACK_TO_ANCHOR_M1"

    ledger.record({
        "status": status,
        "verdict": verdict,
        "action_code": action_code,
        "phi": total_energy,
        "region": region,
    })

    return (
        f"Status: {status} ({verdict}) | "
        f"Energy: {total_energy:.4f} | "
        f"Region: {region} | "
        f"Action Code: `{action_code}`"
    )
