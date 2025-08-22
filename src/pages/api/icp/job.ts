import type { NextApiRequest, NextApiResponse } from 'next';

// Dummy handler for jobs CRUD
let jobs: any[] = [];

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'GET') {
    // Simulate get jobs
    res.status(200).json(jobs);
  } else if (req.method === 'POST') {
    // Simulate add job
    const { title, description, skills, budget } = req.body;
    const newJob = {
      id: `job_${jobs.length + 1}`,
      title,
      description,
      skills: skills.split(",").map((s: string) => s.trim()),
      budget,
      created_at: Date.now()
    };
    jobs.push(newJob);
    res.status(200).json({ message: "Job added!" });
  } else {
    res.status(405).end();
  }
}
