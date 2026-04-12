# CGE v1

Code Governance Engine v1 is a minimal reference implementation for deterministic, verifiable code evolution at the commit boundary.

This is not a framework.  
This is the smallest working example of admitting change instead of assuming it.

---

## What it demonstrates

- Multi-proposal intake (competing candidate changes)
- Proposal normalization and fingerprinting
- Deterministic repository state hashing
- Test-based selection against a shared state
- Admission of exactly one transition
- Receipt generation for the admitted change
- Explicit non-selection of all other candidates

---

## What this actually proves

CGE v1 reduces governance to a single boundary:

> multiple possible changes → one admitted transition

Each candidate:
- is evaluated against the same state  
- produces observable outcomes  
- competes under the same conditions  

Only one crosses the boundary.

Everything else is rejected by construction, not ignored.

---

## Why this matters

Most systems:
- suggest changes  
- apply changes  
- log what happened  

CGE v1 does something different:

> it decides what is allowed to become real, and proves why.

This is the minimal form of:
- execution-time governance  
- admissibility at the point of mutation  
- receipt-backed state transition  

---

## The invariant

No change becomes durable unless:
- it is evaluated against current state
- it satisfies the selection criteria
- it is admitted through the boundary
- a receipt is produced as evidence

---

## Quick start

pip install -r requirements.txt  
python -m pytest -q  
python run_demo.py

---

## What this is not (yet)

- Not a full policy system  
- Not a sandbox runtime  
- Not multi-node verified  
- Not integrated with external execution pipelines  

Those come later.

---

## What this is

The smallest possible system that proves code change can be governed, not just executed.
