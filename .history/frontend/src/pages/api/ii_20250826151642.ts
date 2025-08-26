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

  let finalUrl = `https://identity.ic0.app/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
  if (iiCanister) {
    // If local env detected and the caller did not explicitly request the public provider,
    // force a 127.0.0.1 gateway-style URL so popups point to the local gateway rather than
    // the public identity provider.
    if (localDetected && usePublic !== '1') {
      // If the local dfx HTTP server is being used (default dev port 4943), prefer
      // the canister-host style so Internet Identity's static UI loads correctly
      // (e.g. http://u6s2n-....localhost:4943/#authorize?...). This avoids the
      // gateway returning the Candid UI for some canisters.
      const useCanisterHost = envDfxHost.includes('4943') || envDfxHost.includes('.localhost:4943') || process.env.NEXT_PUBLIC_II_USE_CANISTER_HOST === '1';
      if (useCanisterHost) {
        const portMatch = (envDfxHost.match(/:(\d+)/) || [])[1] || '4943';
        finalUrl = `http://${iiCanister}.localhost:${portMatch}/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
      } else if (gatewayFull) {
        const sep = gatewayFull.includes('id=') ? '' : (gatewayFull.endsWith('&') || gatewayFull.endsWith('?') ? 'id=' : '&id=');
        finalUrl = `${gatewayFull}${sep}${iiCanister}#authorize?canisterId=${canister}${originParam}${redirectParam}`;
      } else if (gatewayCanister) {
        finalUrl = `http://${iiCanister}.localhost:${portMatch}/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
      } else {
        finalUrl = `http://127.0.0.1:8000/?canisterId=${iiCanister}&id=${iiCanister}#authorize?canisterId=${canister}${originParam}${redirectParam}`;
      }
    } else {
      // Non-local or explicit public request: use previous behavior (prefer gateway when available, probe and fall back)
      if (gatewayFull) {
        const sep = gatewayFull.includes('id=') ? '' : (gatewayFull.endsWith('&') || gatewayFull.endsWith('?') ? 'id=' : '&id=');
        finalUrl = `${gatewayFull}${sep}${iiCanister}#authorize?canisterId=${canister}${originParam}${redirectParam}`;
        try {
          const probeUrl = `${gatewayFull}${sep}${iiCanister}`.split('#')[0];
          const probeResp = await fetch(probeUrl, { method: 'HEAD' });
          if (probeResp && probeResp.status === 404) {
            console.warn(`/api/ii: gateway entry ${probeUrl} returned 404, falling back to identity.ic0.app`);
            finalUrl = `https://identity.ic0.app/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
          }
        } catch (e) {
          console.warn(`/api/ii: gateway probe failed for ${gatewayFull} - ${String(e)}; falling back to identity.ic0.app`);
          finalUrl = `https://identity.ic0.app/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
        }
      } else if (gatewayCanister) {
        finalUrl = `http://127.0.0.1:8000/?canisterId=${gatewayCanister}&id=${iiCanister}#authorize?canisterId=${canister}${originParam}${redirectParam}`;
        try {
          const probeUrl = `http://127.0.0.1:8000/?canisterId=${gatewayCanister}&id=${iiCanister}`;
          const probeResp = await fetch(probeUrl, { method: 'HEAD' });
          if (probeResp && probeResp.status === 404) {
            console.warn(`/api/ii: gateway entry ${probeUrl} returned 404, falling back to identity.ic0.app`);
            finalUrl = `https://identity.ic0.app/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
          }
        } catch (e) {
          console.warn(`/api/ii: gateway probe failed for ${gatewayCanister} - ${String(e)}; falling back to identity.ic0.app`);
          finalUrl = `https://identity.ic0.app/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
        }
      } else {
        finalUrl = `http://${iiCanister}.localhost:4943/#authorize?canisterId=${canister}${originParam}${redirectParam}`;
      }
    }
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
