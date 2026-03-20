# StegCGE Architecture

## Core idea

Treat AI-generated code changes as governed proposals rather than informal suggestions.

## Flow

1. Hash current repo state
2. Record per-model proposal receipts
3. Compare and verify proposals
4. Select accepted patch
5. Emit accepted-change receipt
6. Reconstruct repo evolution deterministically
