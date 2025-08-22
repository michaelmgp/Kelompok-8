export const idlFactory = ({ IDL }) => {
  const Result = IDL.Variant({ 'ok' : IDL.Text, 'err' : IDL.Text });
  const JobStatus = IDL.Variant({
    'Open' : IDL.Null,
    'Cancelled' : IDL.Null,
    'InProgress' : IDL.Null,
    'Completed' : IDL.Null,
  });
  const JobRecord = IDL.Record({
    'id' : IDL.Text,
    'status' : JobStatus,
    'client' : IDL.Principal,
    'selected_freelancer' : IDL.Opt(IDL.Principal),
    'title' : IDL.Text,
    'description' : IDL.Text,
    'deadline' : IDL.Opt(IDL.Int),
    'created_at' : IDL.Int,
    'budget' : IDL.Text,
    'skills' : IDL.Vec(IDL.Text),
  });
  const ApplicationStatus = IDL.Variant({
    'UnderReview' : IDL.Null,
    'Withdrawn' : IDL.Null,
    'Rejected' : IDL.Null,
    'Accepted' : IDL.Null,
    'Submitted' : IDL.Null,
  });
  const ApplicationRecord = IDL.Record({
    'id' : IDL.Text,
    'status' : ApplicationStatus,
    'applicant' : IDL.Principal,
    'applied_at' : IDL.Int,
    'reviewed_at' : IDL.Opt(IDL.Int),
    'job_id' : IDL.Text,
    'cover_letter' : IDL.Text,
    'proposed_budget' : IDL.Text,
  });
  return IDL.Service({
    'acceptApplication' : IDL.Func([IDL.Text], [Result], []),
    'completeJob' : IDL.Func([IDL.Text], [Result], []),
    'createJob' : IDL.Func(
        [IDL.Text, IDL.Text, IDL.Text, IDL.Vec(IDL.Text), IDL.Opt(IDL.Int)],
        [Result],
        [],
      ),
    'getAllJobs' : IDL.Func([], [IDL.Vec(JobRecord)], ['query']),
    'getApplication' : IDL.Func(
        [IDL.Text],
        [IDL.Opt(ApplicationRecord)],
        ['query'],
      ),
    'getContractStats' : IDL.Func(
        [],
        [
          IDL.Record({
            'completedJobs' : IDL.Nat,
            'totalJobs' : IDL.Nat,
            'openJobs' : IDL.Nat,
            'totalApplications' : IDL.Nat,
          }),
        ],
        ['query'],
      ),
    'getJob' : IDL.Func([IDL.Text], [IDL.Opt(JobRecord)], ['query']),
    'getJobApplications' : IDL.Func(
        [IDL.Text],
        [IDL.Vec(ApplicationRecord)],
        ['query'],
      ),
    'getMyApplications' : IDL.Func([], [IDL.Vec(ApplicationRecord)], []),
    'getMyJobs' : IDL.Func([], [IDL.Vec(JobRecord)], []),
    'submitApplication' : IDL.Func(
        [IDL.Text, IDL.Text, IDL.Text],
        [Result],
        [],
      ),
  });
};
export const init = ({ IDL }) => { return []; };
