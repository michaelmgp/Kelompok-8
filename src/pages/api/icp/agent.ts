import type { NextApiRequest, NextApiResponse } from 'next';

// Dummy handler for agent CRUD
let agents: any[] = [];

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Simulate get agents
    res.status(200).json(agents);
  } else if (req.method === 'POST') {
    // Simulate add agent
    const { nama, email, role } = req.body;
    const newAgent = {
      id: agents.length + 1,
      nama,
      email,
      role,
      createdAt: Date.now()
    };
    agents.push(newAgent);
    res.status(200).json({ message: "Agent added!" });
  } else {
    res.status(405).end();
  }
}
