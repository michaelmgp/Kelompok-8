import type { Principal } from '@dfinity/principal';
import type { ActorMethod } from '@dfinity/agent';
import type { IDL } from '@dfinity/candid';

export interface ReputationEntry {
  'id' : string,
  'review' : string,
  'user_principal' : Principal,
  'created_at' : bigint,
  'job_id' : string,
  'rating' : number,
  'reviewer' : Principal,
}
export type Result = { 'ok' : string } |
  { 'err' : string };
export interface UserProfile {
  'bio' : string,
  'updated_at' : bigint,
  'principal' : Principal,
  'portfolio_url' : string,
  'name' : string,
  'created_at' : bigint,
  'email' : string,
  'verification_status' : VerificationStatus,
  'experience_level' : string,
  'skills' : Array<string>,
  'location' : string,
  'reputation_score' : number,
}
export interface VerificationRecord {
  'id' : string,
  'status' : VerificationStatus,
  'user_principal' : Principal,
  'verifier' : [] | [Principal],
  'verification_data' : string,
  'verified_at' : [] | [bigint],
  'verification_type' : string,
  'expires_at' : [] | [bigint],
}
export type VerificationStatus = { 'Rejected' : null } |
  { 'Verified' : null } |
  { 'Expired' : null } |
  { 'Pending' : null };
export interface _SERVICE {
  'addReputation' : ActorMethod<[Principal, string, number, string], Result>,
  'getAllProfiles' : ActorMethod<[], Array<UserProfile>>,
  'getAllUsers' : ActorMethod<[], Array<UserProfile>>,
  'getContractStats' : ActorMethod<
    [],
    {
      'averageReputation' : number,
      'totalVerifications' : bigint,
      'totalProfiles' : bigint,
      'totalReputations' : bigint,
      'verifiedProfiles' : bigint,
    }
  >,
  'getMyProfile' : ActorMethod<[], [] | [UserProfile]>,
  'getPendingVerifications' : ActorMethod<[], Array<VerificationRecord>>,
  'getUserProfile' : ActorMethod<[Principal], [] | [UserProfile]>,
  'getUserReputations' : ActorMethod<[Principal], Array<ReputationEntry>>,
  'getUserVerifications' : ActorMethod<[Principal], Array<VerificationRecord>>,
  'getVerification' : ActorMethod<[string], [] | [VerificationRecord]>,
  'processVerification' : ActorMethod<[string, boolean, [] | [bigint]], Result>,
  'searchProfilesBySkills' : ActorMethod<[Array<string>], Array<UserProfile>>,
  'submitVerification' : ActorMethod<[string, string], Result>,
  'updateProfile' : ActorMethod<
    [string, string, string, Array<string>, string, string, string],
    Result
  >,
}
export declare const idlFactory: IDL.InterfaceFactory;
export declare const init: (args: { IDL: typeof IDL }) => IDL.Type[];
