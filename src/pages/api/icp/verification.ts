import type { NextApiRequest, NextApiResponse } from 'next';

// Dummy handler for verification CRUD
let verifications: any[] = [];

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Simulate get verifications
    res.status(200).json(verifications);
  } else if (req.method === 'POST') {
    // Simulate submit verification
    const { verificationType, verificationData } = req.body;
    const newVer = {
      id: `ver_${verifications.length + 1}`,
      verification_type: verificationType,
      verification_data: verificationData,
      status: "Pending",
      created_at: Date.now()
    };
    verifications.push(newVer);
    res.status(200).json({ message: "Verification submitted!" });
  } else {
    res.status(405).end();
  }
}
