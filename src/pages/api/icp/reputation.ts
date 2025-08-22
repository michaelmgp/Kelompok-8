import type { NextApiRequest, NextApiResponse } from 'next';

// Dummy handler for reputation CRUD
let reputations: any[] = [];

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Simulate get reputations
    res.status(200).json(reputations);
  } else if (req.method === 'POST') {
    // Simulate add reputation
    const { userPrincipal, jobId, rating, review } = req.body;
    const newRep = {
      id: `rep_${reputations.length + 1}`,
      user_principal: userPrincipal,
      job_id: jobId,
      rating,
      review,
      reviewer: "aaaa-bbbb-cccc-dddd",
      created_at: Date.now()
    };
    reputations.push(newRep);
    res.status(200).json({ message: "Reputation added!" });
  } else {
    res.status(405).end();
  }
}
