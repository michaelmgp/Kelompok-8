export const idlFactory = ({ IDL }) => {
  const Result = IDL.Variant({ 'ok' : IDL.Text, 'err' : IDL.Text });
  const VerificationStatus = IDL.Variant({
    'Rejected' : IDL.Null,
    'Verified' : IDL.Null,
    'Expired' : IDL.Null,
    'Pending' : IDL.Null,
  });
  const UserProfile = IDL.Record({
    'bio' : IDL.Text,
    'updated_at' : IDL.Int,
    'principal' : IDL.Principal,
    'portfolio_url' : IDL.Text,
    'name' : IDL.Text,
    'created_at' : IDL.Int,
    'email' : IDL.Text,
    'verification_status' : VerificationStatus,
    'experience_level' : IDL.Text,
    'skills' : IDL.Vec(IDL.Text),
    'location' : IDL.Text,
    'reputation_score' : IDL.Float64,
  });
  const VerificationRecord = IDL.Record({
    'id' : IDL.Text,
    'status' : VerificationStatus,
    'user_principal' : IDL.Principal,
    'verifier' : IDL.Opt(IDL.Principal),
    'verification_data' : IDL.Text,
    'verified_at' : IDL.Opt(IDL.Int),
    'verification_type' : IDL.Text,
    'expires_at' : IDL.Opt(IDL.Int),
  });
  const ReputationEntry = IDL.Record({
    'id' : IDL.Text,
    'review' : IDL.Text,
    'user_principal' : IDL.Principal,
    'created_at' : IDL.Int,
    'job_id' : IDL.Text,
    'rating' : IDL.Float64,
    'reviewer' : IDL.Principal,
  });
  return IDL.Service({
    'addReputation' : IDL.Func(
        [IDL.Principal, IDL.Text, IDL.Float64, IDL.Text],
        [Result],
        [],
      ),
    'getAllProfiles' : IDL.Func([], [IDL.Vec(UserProfile)], ['query']),
    'getAllUsers' : IDL.Func([], [IDL.Vec(UserProfile)], ['query']),
    'getContractStats' : IDL.Func(
        [],
        [
          IDL.Record({
            'averageReputation' : IDL.Float64,
            'totalVerifications' : IDL.Nat,
            'totalProfiles' : IDL.Nat,
            'totalReputations' : IDL.Nat,
            'verifiedProfiles' : IDL.Nat,
          }),
        ],
        ['query'],
      ),
    'getMyProfile' : IDL.Func([], [IDL.Opt(UserProfile)], []),
    'getPendingVerifications' : IDL.Func(
        [],
        [IDL.Vec(VerificationRecord)],
        ['query'],
      ),
    'getUserProfile' : IDL.Func(
        [IDL.Principal],
        [IDL.Opt(UserProfile)],
        ['query'],
      ),
    'getUserReputations' : IDL.Func(
        [IDL.Principal],
        [IDL.Vec(ReputationEntry)],
        ['query'],
      ),
    'getUserVerifications' : IDL.Func(
        [IDL.Principal],
        [IDL.Vec(VerificationRecord)],
        ['query'],
      ),
    'getVerification' : IDL.Func(
        [IDL.Text],
        [IDL.Opt(VerificationRecord)],
        ['query'],
      ),
    'processVerification' : IDL.Func(
        [IDL.Text, IDL.Bool, IDL.Opt(IDL.Int)],
        [Result],
        [],
      ),
    'searchProfilesBySkills' : IDL.Func(
        [IDL.Vec(IDL.Text)],
        [IDL.Vec(UserProfile)],
        ['query'],
      ),
    'submitVerification' : IDL.Func([IDL.Text, IDL.Text], [Result], []),
    'updateProfile' : IDL.Func(
        [
          IDL.Text,
          IDL.Text,
          IDL.Text,
          IDL.Vec(IDL.Text),
          IDL.Text,
          IDL.Text,
          IDL.Text,
        ],
        [Result],
        [],
      ),
  });
};
export const init = ({ IDL }) => { return []; };
