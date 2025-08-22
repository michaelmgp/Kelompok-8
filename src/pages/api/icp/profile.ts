import type { NextApiRequest, NextApiResponse } from 'next';
import { getIdentityActor } from '../../../lib/icpClient';
import { Principal } from '@dfinity/principal';

// Dummy handler for profile CRUD
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const actor = await getIdentityActor();

  function serializeBigInt(obj: any): any {
    return JSON.parse(
      JSON.stringify(obj, (key, value) =>
        typeof value === 'bigint' ? value.toString() : value
      )
    );
  }

  if (req.method === 'GET') {
    if (req.query.all === 'true') {
      // Get all profiles
      try {
        const result = await actor.getAllUsers();
        res.status(200).json(serializeBigInt(result));
      } catch (err) {
        res.status(500).json({ error: String(err) });
      }
      return;
    }
    // Gunakan principal default jika input tidak valid
    let principalId = req.query.principal as string;
    let principal: Principal;
    try {
      principal = Principal.fromText(principalId);
    } catch {
      // fallback principal ICP lokal
      principal = Principal.fromText('aaaaa-aa');
    }
    try {
      const result = await actor.getUserProfile(principal);
      res.status(200).json(serializeBigInt(result));
    } catch (err) {
      res.status(500).json({ error: String(err) });
    }
  } else if (req.method === 'POST') {
    // Update profile
    const { name, email, bio, skills, portfolioUrl, location, experienceLevel } = req.body;
    try {
      const result = await actor.updateProfile(
        name,
        email,
        bio,
        skills.split(',').map((s: string) => s.trim()),
        portfolioUrl,
        location,
        experienceLevel
      );
      res.status(200).json(result);
    } catch (err) {
      res.status(500).json({ error: String(err) });
    }
  } else {
    res.status(405).end();
  }
}
