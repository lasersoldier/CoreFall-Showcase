# Architecture

CoreFall is a Godot 4 project written in GDScript. High-level layout (source not included in this showcase):

- **Hub scene** – walkable base. Facilities (Archive, Ability Center, Blueprint Workshop, Supply Station, Tower Connection Hub, Settings) open as panels hosted by a responsive panel host with hover-detail components.
- **Battle scene** – real-time loop built from separate systems: enemies, towers, combos, waves, barriers, printing, entropy, ice trails and visual effects. Enemy lookups use a spatial hash; seeker enemies use incremental heap-based flow fields; crowds use an AI level-of-detail.
- **Data layer** – campaign, tower, enemy and wave configs are JSON-driven and editable in the in-game **Dev Lab**. Autoloads handle text (zh/en), meta progression, settings, music and SFX.
- **Endless Mode** – a wave director scales spawn rate, roster, enemy tier and HP with elapsed time; a hard population cap keeps frame time bounded (an 8-minute simulated run with ~565 enemies stays under ~28 ms worst tick).
