import { NextApiRequest, NextApiResponse } from 'next';

// Server-side redirect to Internet Identity authorize page.
// This hides the canisterId from the browser URL because the browser first visits /api/ii.
export default function handler(req: NextApiRequest, res: NextApiResponse) {
  // Allow overriding the canister via query param: /api/ii?canister=xxxx
  const queryCanister = Array.isArray(req.query.canister) ? req.query.canister[0] : (req.query.canister as string | undefined);
  // Default to the application canister ID (the canister the frontend wants a delegation for).
  // Using the Identity canister here made Internet Identity show "manage" instead of "connect".
  // Prefer the app canister (the canister the frontend delegates to). If not set, fall back
  // to NEXT_PUBLIC_IDENTITY_CANISTER_ID to avoid an empty canisterId in the authorize URL.
  const canister = queryCanister || process.env.NEXT_PUBLIC_APP_CANISTER_ID || process.env.NEXT_PUBLIC_IDENTITY_CANISTER_ID || '';

  // Allow overriding origin via query param: /api/ii?origin=http://localhost:5000
  const queryOrigin = Array.isArray(req.query.origin) ? req.query.origin[0] : (req.query.origin as string | undefined);
  // Force localhost:5000 for local development to ensure proper redirect
  const envDfxHost = process.env.NEXT_PUBLIC_DFX_HOST || '';
  const isLocalDev = envDfxHost.includes('127.0.0.1:8000') || envDfxHost.includes('localhost:8000');
  
  let origin: string;
  if (queryOrigin) {
    origin = queryOrigin;
  } else if (isLocalDev) {
    // Force localhost:5000 for local development
    origin = 'http://localhost:5000';
  } else {
    // Derive default origin from request headers if not provided
    const proto = (req.headers['x-forwarded-proto'] as string) || 'http';
    origin = req.headers.host ? `${proto}://${req.headers.host}` : '';
  }

  // optional redirect path (client-side route), e.g. /ii-callback
  const queryRedirect = Array.isArray(req.query.redirect) ? req.query.redirect[0] : (req.query.redirect as string | undefined) || '';
  // Set default redirect to /ii-callback if not specified
  const redirectPath = queryRedirect || '/ii-callback';
  const redirectParam = `&redirect_uri=${encodeURIComponent((origin || '') + redirectPath)}`;
  
  // If an environment variable with the II canister id is provided, prefer a local address.
  const iiCanister = process.env.NEXT_PUBLIC_INTERNET_IDENTITY_ID || '';
  const gatewayFull = process.env.NEXT_PUBLIC_II_GATEWAY_URL || '';
  const gatewayCanister = process.env.NEXT_PUBLIC_II_GATEWAY_CANISTER_ID || process.env.NEXT_PUBLIC_GATEWAY_CANISTER_ID || '';
  const localDetected = Boolean(envDfxHost.includes('127.0.0.1') || envDfxHost.includes('localhost') || gatewayFull || gatewayCanister);

  // Build the authorize URL. If we're running the local dfx HTTP server on port 8000
  // and an II canister is configured, prefer the canister-host form so the local
  // II static UI is used (e.g. http://<ii>.localhost:8000/#authorize?canisterId=<gateway>...)
  let finalUrl = `https://identity.ic0.app/#authorize?canisterId=${canister}&origin=${encodeURIComponent(origin)}${redirectParam}`;

  const prefersLocalCanisterHost = Boolean(iiCanister && (envDfxHost.includes('localhost:8000') || envDfxHost.includes('127.0.0.1:8000')));
  if (prefersLocalCanisterHost) {
    // Use the application canister id (the canister we want a delegation for) so
    // Internet Identity displays the Connect flow (not Manage). Fall back to the
    // computed `canister` if APP canister env is not set.
    const appCanister = process.env.NEXT_PUBLIC_APP_CANISTER_ID || process.env.NEXT_PUBLIC_IDENTITY_CANISTER_ID || '';
    const authCanister = appCanister || canister;
    
    // For local development, ALWAYS use port 8000 for II (dfx replica)
    // Example: http://umunu-...localhost:8000/#authorize?canisterId=uzt4z-...&origin=http://localhost:5000&redirect_uri=http://localhost:5000/ii-callback
    finalUrl = `http://${iiCanister}.localhost:8000/#authorize?canisterId=${canister}&origin=${encodeURIComponent(origin)}${redirectParam}`;
  }
  // Server-side debug log
  /* eslint-disable no-console */
    console.log("/api/ii redirecting to:", finalUrl, { 
      queryCanister, 
      usedCanister: canister, 
      iiCanister, 
      envAppCanister: process.env.NEXT_PUBLIC_APP_CANISTER_ID, 
      envIdentityCanister: process.env.NEXT_PUBLIC_IDENTITY_CANISTER_ID,
      origin,
      redirectParam,
      envDfxHost,
      isLocalDev
    });
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
