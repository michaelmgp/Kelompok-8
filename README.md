# Next.js Motoko CRUD Example

This app demonstrates CRUD operations for ICP Motoko canisters (profile, verification, reputation) using Next.js 14 App Router, TypeScript, and TailwindCSS.

## Features
- Create, Read, Update, Delete user profile
- Submit and process verification
- Add and view reputation
- Connect to ICP canisters via Candid interface

## Setup
1. Copy your canister IDs to `.env.local`:
   ```env
   NEXT_PUBLIC_IDENTITY_CANISTER_ID=
   NEXT_PUBLIC_JOB_CANISTER_ID=
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the app:
   ```bash
   npm run dev
   ```

## Usage
- Access the app at `http://localhost:3000`
- Use the navigation to test CRUD for profile, verification, and reputation

## ICP Integration
- All API calls use fetch to the local ICP replica or mainnet (adjust endpoint as needed)
- See example code in `/src/app/profile`, `/src/app/verification`, `/src/app/reputation`

## Customization
- Update canister IDs in `.env.local` as needed
- Extend pages/components for more features

---

For more details, see CARA_PENGGUNAAN.md in your canister folder.
