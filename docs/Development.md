# Development

- Engine: Godot 4.7, GDScript, Mobile renderer.
- Tests: headless GDScript test scripts cover core gameplay, active abilities, endless mode and performance (benchmarks and old-vs-new equivalence checks for optimised hot paths).
- Performance work: wall-mask early-outs, no-copy stat reads, spatial hashing for targeting, render culling with baked textures, crowd LOD, incremental flow fields.
- Promo assets: `tools/make_trailer.py` reproduces the trailer, GIF and screenshots from two raw recordings (hub/story take + endless take).

> TODO: add a short "what I designed vs. what AI assisted" section, as in the reference showcase, before publishing.
