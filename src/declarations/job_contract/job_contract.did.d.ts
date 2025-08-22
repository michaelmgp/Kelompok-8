import type { Principal } from '@dfinity/principal';
import type { ActorMethod } from '@dfinity/agent';
import type { IDL } from '@dfinity/candid';

export interface ApplicationRecord {
  'id' : string,
  'status' : ApplicationStatus,
  'applicant' : Principal,
  'applied_at' : bigint,
  'reviewed_at' : [] | [bigint],
  'job_id' : string,
  'cover_letter' : string,
  'proposed_budget' : string,
}
export type ApplicationStatus = { 'UnderReview' : null } |
  { 'Withdrawn' : null } |
  { 'Rejected' : null } |
  { 'Accepted' : null } |
  { 'Submitted' : null };
export interface JobRecord {
  'id' : string,
  'status' : JobStatus,
  'client' : Principal,
  'selected_freelancer' : [] | [Principal],
  'title' : string,
  'description' : string,
  'deadline' : [] | [bigint],
  'created_at' : bigint,
  'budget' : string,
  'skills' : Array<string>,
}
export type JobStatus = { 'Open' : null } |
  { 'Cancelled' : null } |
  { 'InProgress' : null } |
  { 'Completed' : null };
export type Result = { 'ok' : string } |
  { 'err' : string };
export interface _SERVICE {
  'acceptApplication' : ActorMethod<[string], Result>,
  'completeJob' : ActorMethod<[string], Result>,
  'createJob' : ActorMethod<
    [string, string, string, Array<string>, [] | [bigint]],
    Result
  >,
  'getAllJobs' : ActorMethod<[], Array<JobRecord>>,
  'getApplication' : ActorMethod<[string], [] | [ApplicationRecord]>,
  'getContractStats' : ActorMethod<
    [],
    {
      'completedJobs' : bigint,
      'totalJobs' : bigint,
      'openJobs' : bigint,
      'totalApplications' : bigint,
    }
  >,
  'getJob' : ActorMethod<[string], [] | [JobRecord]>,
  'getJobApplications' : ActorMethod<[string], Array<ApplicationRecord>>,
  'getMyApplications' : ActorMethod<[], Array<ApplicationRecord>>,
  'getMyJobs' : ActorMethod<[], Array<JobRecord>>,
  'submitApplication' : ActorMethod<[string, string, string], Result>,
}
export declare const idlFactory: IDL.InterfaceFactory;
export declare const init: (args: { IDL: typeof IDL }) => IDL.Type[];
