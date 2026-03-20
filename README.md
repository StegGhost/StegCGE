# StegCGE

**This is the layer that makes AI-generated code trustworthy.**

StegCGE is a repo bootstrap for governed AI-assisted software construction. It provides a starting structure for proposal intake, repo-state hashing, patch verification, receipt emission, and CI validation.

## Included

- base package layout
- starter GitHub Actions validation workflow
- starter tests
- proposal and receipt folders
- docs and architecture notes
- repo hygiene defaults

## Suggested first moves

1. Create the GitHub repo as **Public**
2. Add this bundle
3. Commit to `main`
4. Run the validation workflow
5. Start wiring in CGE modules incrementally

## Initial scope

StegCGE should begin as:
- proposal governance layer
- state hashing layer
- receipt and replay layer
- multi-LLM patch adjudication layer

## Long-term direction

- trust-weighted model selection
- patch consensus across models
- dependency-closure checks
- deterministic replay of code evolution
- signed proposal lineage
