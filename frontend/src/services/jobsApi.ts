
import axios from 'axios';

const API_URL = 'https://938ae06e-6014-4e80-9745-477479b16f17.mock.pstmn.io/api/jobs/search';
const API_KEY = process.env.NEXT_PUBLIC_POSTMAN_API_KEY;

export const fetchJobs = async () => {
  try {
    const response = await axios.get(API_URL, {
      headers: {
        'x-api-key': API_KEY,
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching jobs:', error);
    throw error;
  }
};
