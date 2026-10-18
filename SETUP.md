# Setup (5 minutes)

1. Copy everything in this folder into your profile repo: `Jagadish-s-naik/Jagadish-S-Naik` (the repo named exactly like your username). Make sure its default branch is `main`.
2. **Private contributions on your graph:** GitHub > Profile > Contributions graph dropdown > tick *Private contributions*. The snake reads the graph, so it needs this.
3. **Private contributions in the stats card:** create a classic Personal Access Token with scopes `read:user` and `repo`, then add it to the profile repo as an Actions secret named `PROFILE_STATS_TOKEN`.
4. Repo > Actions > run **Profile stats** once, then **Contribution snake** once (this creates the `output` branch). Both then refresh every 12 hours.
5. Optional: tweak the chess game by editing `GAME` in `scripts/build_assets.py` and running `python scripts/build_assets.py` (needs `pip install chess`).
