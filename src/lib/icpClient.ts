import { HttpAgent, Actor } from '@dfinity/agent';
import { IDL } from '@dfinity/candid';

const identityCanisterId = process.env.NEXT_PUBLIC_IDENTITY_CANISTER_ID;
const jobCanisterId = process.env.NEXT_PUBLIC_JOB_CANISTER_ID;

// Example: Minimal candid interface for profile CRUD
const identityIdlFactory = ({ IDL }) => {
  return IDL.Service({
    getUserProfile: IDL.Func([IDL.Principal], [IDL.Opt(IDL.Record({
      principal: IDL.Principal,
      name: IDL.Text,
      email: IDL.Text,
      bio: IDL.Text,
      skills: IDL.Vec(IDL.Text),
      portfolio_url: IDL.Text,
      location: IDL.Text,
      experience_level: IDL.Text,
      verification_status: IDL.Variant({
        Pending: IDL.Null,
        Verified: IDL.Null,
        Rejected: IDL.Null,
        Expired: IDL.Null
      }),
      reputation_score: IDL.Float64,
      created_at: IDL.Int,
      updated_at: IDL.Int
    }))], ['query']),
    updateProfile: IDL.Func([
      IDL.Text, IDL.Text, IDL.Text, IDL.Vec(IDL.Text), IDL.Text, IDL.Text, IDL.Text
    ], [IDL.Record({ ok: IDL.Text, err: IDL.Text })], ['update']),
    getAllUsers: IDL.Func([], [IDL.Vec(IDL.Record({
      principal: IDL.Principal,
      name: IDL.Text,
      email: IDL.Text,
      bio: IDL.Text,
      skills: IDL.Vec(IDL.Text),
      portfolio_url: IDL.Text,
      location: IDL.Text,
      experience_level: IDL.Text,
      verification_status: IDL.Variant({
        Pending: IDL.Null,
        Verified: IDL.Null,
        Rejected: IDL.Null,
        Expired: IDL.Null
      }),
      reputation_score: IDL.Float64,
      created_at: IDL.Int,
      updated_at: IDL.Int
    }))], ['query'])
  });
};

export async function getIdentityActor() {
  const agent = new HttpAgent({ host: 'http://127.0.0.1:8000' });
  if (process.env.NODE_ENV === 'development') {
    await agent.fetchRootKey();
  }
  return Actor.createActor(identityIdlFactory, {
    agent,
    canisterId: identityCanisterId || "uxrrr-q7777-77774-qaaaq-cai"
  });
}

// Add similar factory for job, agent, etc. as needed
