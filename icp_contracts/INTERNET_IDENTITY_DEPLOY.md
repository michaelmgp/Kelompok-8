Goal

Provide step-by-step instructions to build and deploy a local Internet Identity (II) canister, update `dfx.json` so `dfx deploy internet_identity` works, and configure the frontend to use the local II canister.

Checklist

- [ ] Clone and build the Internet Identity source
- [ ] Locate the built wasm + candid (or let dfx build it)
- [ ] Add an `internet_identity` canister entry (or reference built artifacts) to `icp_contracts/dfx.json`
- [ ] Start the local dfx replica and deploy
- [ ] Set `NEXT_PUBLIC_II_CANISTER_ID` in `frontend/.env` and restart the frontend dev server

Important notes

- Building Internet Identity requires the internet-identity repository and the toolchain it expects (Rust + wasm target, Node.js, dfx if building via canister config). See the upstream README for exact build steps.
- This document shows safe, conservative steps. Do not attempt to deploy until the wasm/candid artifacts exist or until you configure `dfx.json` to build the canister from source.

Steps (PowerShell)

1) Clone the official Internet Identity repository and read its README

```powershell
cd $env:USERPROFILE\Documents\kelompok
git clone https://github.com/dfinity/internet-identity.git internet-identity-src
cd internet-identity-src
# Read README.md and follow the repo-specific build steps.
# Typical preparatory steps (on Windows you may use WSL or follow Windows-specific guidance):
# - Install Rust and add wasm target:
#   rustup default stable
#   rustup target add wasm32-unknown-unknown
# - Install Node.js and npm
# - Install dfx (if not installed) and ensure it's on PATH
```

2) Build according to the repo README

The internet-identity repo may provide a script or instructions. A generic sequence is:

```powershell
npm ci
npm run build
# or as the repo README instructs
```

After a successful build, locate the canister artifacts (the exact paths differ by repo/build method). Common locations:

- `internet-identity-src/.dfx/local/canisters/internet_identity/` — contains `.wasm` and `.did` files when built with `dfx`.
- or a `dist/` or `build/` folder per the repo's build script.

3) Add the canister entry to `icp_contracts/dfx.json`

Option A — reference built artifacts (recommended if you built the repo and have artifacts)

Open `icp_contracts/dfx.json` and add the following inside the `"canisters"` object. Update the `wasm` and `candid` paths to match your build output paths (relative to `icp_contracts`):

```json
"internet_identity": {
  "type": "custom",
  "wasm": "../internet-identity-src/.dfx/local/canisters/internet_identity/internet_identity.wasm",
  "candid": "../internet-identity-src/.dfx/local/canisters/internet_identity/internet_identity.did"
}
```

Option B — configure to build internet-identity via dfx (advanced)

If you prefer `dfx` to build the canister from the internet-identity source directly, you'll need to add a `package` style entry that points to the source and `dfx` build instructions — consult the upstream repo or paste the repo's `dfx.json` snippet into yours.

4) Start the local replica and deploy

From the `icp_contracts` folder (where `dfx.json` lives):

```powershell
cd c:\Users\User.DESKTOP-T74KNS1\Documents\kelompok\icp_contracts
dfx start --background
dfx deploy internet_identity
```

If `dfx deploy` fails with an artifact not found, confirm the paths you used in `dfx.json` point to actual files.

5) Record the deployed canister id and wire the frontend

After a successful `dfx deploy internet_identity` the canister id will be printed and stored in `.dfx/local/canister_ids.json`.

- Locate the canister id for `internet_identity` in `.dfx/local/canister_ids.json`.
- Add it to your frontend environment: edit `frontend/.env` (you said you edited it) and add:

```
NEXT_PUBLIC_II_CANISTER_ID=<your-internet-identity-canister-id>
```

Then restart the frontend dev server:

```powershell
cd c:\Users\User.DESKTOP-T74KNS1\Documents\kelompok\frontend
# stop any running dev server, then:
npm run dev
```

6) Verify

- In your app, trigger the II flow (Sign In). The server `/api/ii` will prefer `NEXT_PUBLIC_II_CANISTER_ID` and produce a local II URL like `http://<ii-canister>.localhost:4943/#authorize?...` that opens in a popup.
- Confirm the popup navigates to the local II and that the main tab is not redirected.

Troubleshooting

- If `dfx deploy internet_identity` still fails: check `dfx.json` paths and ensure the wasm/did files exist and are readable by dfx.
- If you prefer not to run a local II, remove/leave `NEXT_PUBLIC_II_CANISTER_ID` empty so the app uses `https://identity.ic0.app`.

If you want, I can:

- Edit `icp_contracts/dfx.json` to include the `internet_identity` snippet pointing to a placeholder path (you will replace the path with the actual artifact path after building), or
- Edit `frontend/.env` to set `NEXT_PUBLIC_II_CANISTER_ID` after you share the canister id printed by `dfx deploy`.

Tell me which one you want me to do next (add template to `dfx.json`, add `frontend/.env` entry, or walk you through the build step-by-step).
