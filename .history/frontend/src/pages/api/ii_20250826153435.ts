import { NextApiRequest, NextApiResponse } from 'next';

// Server-side redirect to Internet Identity authorize page.
// This hides the canisterId from the browser URL because the browser first visits /api/ii.
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Allow overriding the canister via query param: /api/ii?canister=xxxx
  const queryCanister = Array.isArray(req.query.canister) ? req.query.canister[0] : (req.query.canister as string | undefined);
  // Default to the application canister ID (the canister the frontend wants a delegation for).
  // Using the Identity canister here made Internet Identity show "manage" instead of "connect".
  // Prefer the app canister (the canister the frontend delegates to). If not set, fall back
  // to NEXT_PUBLIC_IDENTITY_CANISTER_ID to avoid an empty canisterId in the authorize URL.
  const canister = queryCanister || process.env.NEXT_PUBLIC_APP_CANISTER_ID || process.env.NEXT_PUBLIC_IDENTITY_CANISTER_ID || '';

  // Allow overriding origin via query param: /api/ii?origin=http://localhost:5000
  const queryOrigin = Array.isArray(req.query.origin) ? req.query.origin[0] : (req.query.origin as string | undefined);
  // Derive default origin from request headers if not provided
  const proto = (req.headers['x-forwarded-proto'] as string) || 'http';
  const defaultOrigin = req.headers.host ? `${proto}://${req.headers.host}` : '';
  const origin = queryOrigin || defaultOrigin || '';

  // optional redirect path (client-side route), e.g. /ii-callback
  const queryRedirect = Array.isArray(req.query.redirect) ? req.query.redirect[0] : (req.query.redirect as string | undefined) || '';
  // Always redirect to Internet Identity public endpoint. Redirecting to the local replica
  // root (`NEXT_PUBLIC_DFX_HOST`) can return a 503 for canister HTTP root paths, so avoid that.
  // Include origin so Internet Identity shows the correct returning origin (frontend)
  const originParam = origin ? `&origin=${encodeURIComponent(origin)}` : '';
  const redirectParam = queryRedirect ? `&redirect_uri=${encodeURIComponent((origin || '') + queryRedirect)}` : '';
  const idUrl = `http://<ii-canister-id>.localhost:4943/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
  // If an environment variable with the II canister id is provided, prefer a local address.
  // Prefer returning a gateway-style URL when a gateway canister id or full gateway URL is configured
  const iiCanister = process.env.NEXT_PUBLIC_II_CANISTER_ID || '';
  const gatewayFull = process.env.NEXT_PUBLIC_II_GATEWAY_URL || ''; // optional full base like http://127.0.0.1:8000/?canisterId=ulvla...&id=
  // Support either specific II gateway canister env or a generic gateway canister env
  const gatewayCanister = process.env.NEXT_PUBLIC_II_GATEWAY_CANISTER_ID || process.env.NEXT_PUBLIC_GATEWAY_CANISTER_ID || ''; // optional gateway canister id to build gateway URL
  // Detect if we're running in a local dev environment where the gateway should be used.
  const envDfxHost = process.env.NEXT_PUBLIC_DFX_HOST || '';
  const localDetected = Boolean(envDfxHost.includes('127.0.0.1') || envDfxHost.includes('localhost') || gatewayFull || gatewayCanister);
  const usePublic = Array.isArray(req.query.use_public) ? req.query.use_public[0] : (req.query.use_public as string | undefined);

  // Build the authorize URL. If we're running the local dfx HTTP server on port 8000
  // and an II canister is configured, prefer the canister-host form so the local
  // II static UI is used (e.g. http://<ii>.localhost:8000/#authorize?canisterId=<gateway>...)
  let finalUrl = `https://identity.ic0.app/#authorize?canisterId=${canister}${originParam}${redirectParam}`;

  const prefersLocalCanisterHost = Boolean(iiCanister && (envDfxHost.includes('localhost:8000') || envDfxHost.includes('127.0.0.1:8000')));
  if (prefersLocalCanisterHost) {
    // Use the gateway canister id for the canisterId query param when available.
    const gw = gatewayCanister || process.env.NEXT_PUBLIC_II_GATEWAY_CANISTER_ID || '';
    // Example: http://uxrrr-...localhost:8000/#authorize?canisterId=ucwa4-...
    finalUrl = `http://${iiCanister}.localhost:8000/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
  }
  // Server-side debug log
  /* eslint-disable no-console */
    console.log("/api/ii redirecting to:", finalUrl, { queryCanister, usedCanister: canister, iiCanister, envAppCanister: process.env.NEXT_PUBLIC_APP_CANISTER_ID, envIdentityCanister: process.env.NEXT_PUBLIC_IDENTITY_CANISTER_ID });
  /* eslint-enable no-console */
 

  // If client explicitly requests no redirect, return the final URL as JSON so the
  // frontend can open it in a popup/tab and avoid navigating the current window.
  const noRedirectParam = Array.isArray(req.query.no_redirect) ? req.query.no_redirect[0] : (req.query.no_redirect as string | undefined);
  if (noRedirectParam === 'true' || noRedirectParam === '1') {
    res.setHeader('Content-Type', 'application/json');
    return res.status(200).json({ url: finalUrl });
  }

  res.redirect(302, finalUrl);
}
