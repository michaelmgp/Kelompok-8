/**
 * Identity Contract - ICP Smart Contract for User Identity Management
 * Handles user profiles, verification, and reputation on Internet Computer
 */

import Debug "mo:base/Debug";
import HashMap "mo:base/HashMap";
import Text "mo:base/Text";
import Time "mo:base/Time";
import Array "mo:base/Array";
import Result "mo:base/Result";
import Principal "mo:base/Principal";
import Float "mo:base/Float";
import Nat "mo:base/Nat";
import Iter "mo:base/Iter";

actor IdentityContract {

  // ----------------------------
  // Type Definitions
  // ----------------------------

  public type VerificationStatus = {
    #Pending;
    #Verified;
    #Rejected;
    #Expired;
  };

  public type UserProfile = {
    principal: Principal;
    name: Text;
    email: Text;
    bio: Text;
    skills: [Text];
    portfolio_url: Text;
    location: Text;
    experience_level: Text;
    verification_status: VerificationStatus;
    reputation_score: Float;
    created_at: Int;
    updated_at: Int;
  };

  public type VerificationRecord = {
    id: Text;
    user_principal: Principal;
    verification_type: Text; // "email", "identity", "skills", "portfolio"
    verification_data: Text;
    status: VerificationStatus;
    verified_at: ?Int;
    expires_at: ?Int;
    verifier: ?Principal;
  };

  public type ReputationEntry = {
    id: Text;
    user_principal: Principal;
    job_id: Text;
    rating: Float; // 1.0 to 5.0
    review: Text;
    reviewer: Principal;
    created_at: Int;
  };

  // ----------------------------
  // Stable State (persists across upgrades)
  // ----------------------------

  // Counters
  stable var nextVerificationId : Nat = 1;
  stable var nextReputationId   : Nat = 1;

  // Snapshots for maps (since HashMap itself cannot be stable)
  stable var profilesStore           : [(Principal, UserProfile)] = [];
  stable var verificationsStore      : [(Text, VerificationRecord)] = [];
  stable var userVerificationsStore  : [(Principal, [Text])] = [];
  stable var reputationsStore        : [(Text, ReputationEntry)] = [];
  stable var userReputationsStore    : [(Principal, [Text])] = [];

  // ----------------------------
  // In-memory Maps
  // ----------------------------

  var profiles = HashMap.HashMap<Principal, UserProfile>(10, Principal.equal, Principal.hash);
  var verifications = HashMap.HashMap<Text, VerificationRecord>(50, Text.equal, Text.hash);
  var userVerifications = HashMap.HashMap<Principal, [Text]>(10, Principal.equal, Principal.hash);
  var reputations = HashMap.HashMap<Text, ReputationEntry>(100, Text.equal, Text.hash);
  var userReputations = HashMap.HashMap<Principal, [Text]>(10, Principal.equal, Principal.hash);

  // ----------------------------
  // Upgrade Hooks
  // ----------------------------

  system func preupgrade() {
    profilesStore := Iter.toArray(profiles.entries());
    verificationsStore := Iter.toArray(verifications.entries());
    userVerificationsStore := Iter.toArray(userVerifications.entries());
    reputationsStore := Iter.toArray(reputations.entries());
    userReputationsStore := Iter.toArray(userReputations.entries());
  };

  system func postupgrade() {
    // Rehydrate all maps from their stable snapshots
    profiles := HashMap.HashMap<Principal, UserProfile>(Nat.max(10, profilesStore.size() * 2), Principal.equal, Principal.hash);
    for ((k, v) in profilesStore.vals()) { profiles.put(k, v) };

    verifications := HashMap.HashMap<Text, VerificationRecord>(Nat.max(50, verificationsStore.size() * 2), Text.equal, Text.hash);
    for ((k, v) in verificationsStore.vals()) { verifications.put(k, v) };

    userVerifications := HashMap.HashMap<Principal, [Text]>(Nat.max(10, userVerificationsStore.size() * 2), Principal.equal, Principal.hash);
    for ((k, v) in userVerificationsStore.vals()) { userVerifications.put(k, v) };

    reputations := HashMap.HashMap<Text, ReputationEntry>(Nat.max(100, reputationsStore.size() * 2), Text.equal, Text.hash);
    for ((k, v) in reputationsStore.vals()) { reputations.put(k, v) };

    userReputations := HashMap.HashMap<Principal, [Text]>(Nat.max(10, userReputationsStore.size() * 2), Principal.equal, Principal.hash);
    for ((k, v) in userReputationsStore.vals()) { userReputations.put(k, v) };
  };

  // ----------------------------
  // Queries (Reads)
  // ----------------------------

  // Ambil semua user profile
  public query func getAllUsers() : async [UserProfile] {
    Iter.toArray(profiles.vals())
  };

   public query func getAllProfiles() : async [UserProfile] {
    Iter.toArray(profiles.vals());
};
  // Get user profile
  public query func getUserProfile(userPrincipal: Principal) : async ?UserProfile {
    profiles.get(userPrincipal)
  };

  // Get verification by ID
  public query func getVerification(verificationId: Text) : async ?VerificationRecord {
    verifications.get(verificationId)
  };

  // Get user verifications
  public query func getUserVerifications(userPrincipal: Principal) : async [VerificationRecord] {
    switch (userVerifications.get(userPrincipal)) {
      case (null) { [] };
      case (?verIds) {
        Array.mapFilter<Text, VerificationRecord>(
          verIds,
          func (verId: Text) : ?VerificationRecord { verifications.get(verId) }
        )
      };
    }
  };

  // Get user reputation entries
  public query func getUserReputations(userPrincipal: Principal) : async [ReputationEntry] {
    switch (userReputations.get(userPrincipal)) {
      case (null) { [] };
      case (?repIds) {
        Array.mapFilter<Text, ReputationEntry>(
          repIds,
          func (repId: Text) : ?ReputationEntry { reputations.get(repId) }
        )
      };
    }
  };

  // Get my profile
  public shared(msg) func getMyProfile() : async ?UserProfile {
    profiles.get(msg.caller)
  };

  // Get pending verifications (admin/reporting)
  public query func getPendingVerifications() : async [VerificationRecord] {
    let allVerifications = Iter.toArray(verifications.vals());
    Array.filter<VerificationRecord>(
      allVerifications,
      func (ver: VerificationRecord) : Bool { ver.status == #Pending }
    )
  };

  // Search profiles by skills (case-insensitive ANY-match)
  public query func searchProfilesBySkills(searchSkills: [Text]) : async [UserProfile] {
    let allProfiles = Iter.toArray(profiles.vals());
    Array.filter<UserProfile>(
      allProfiles,
      func (profile: UserProfile) : Bool {
        Array.find<Text>(
          searchSkills,
          func (searchSkill: Text) : Bool {
            Array.find<Text>(
              profile.skills,
              func (userSkill: Text) : Bool {
                Text.equal(Text.toLowercase(userSkill), Text.toLowercase(searchSkill))
              }
            ) != null
          }
        ) != null
      }
    )
  };

  // Get contract statistics
  public query func getContractStats() : async {
    totalProfiles: Nat;
    verifiedProfiles: Nat;
    totalVerifications: Nat;
    totalReputations: Nat;
    averageReputation: Float;
  } {
    let allProfiles = Iter.toArray(profiles.vals());
    let verifiedProfilesCount = Array.filter<UserProfile>(
      allProfiles,
      func (p: UserProfile) : Bool { p.verification_status == #Verified }
    ).size();

    let allReps = Iter.toArray(reputations.vals());
    let totalRating = Array.foldLeft<ReputationEntry, Float>(
      allReps,
      0.0,
      func (acc: Float, r: ReputationEntry) : Float { acc + r.rating }
    );
    let avgReputation = if (allReps.size() > 0) {
      totalRating / Float.fromInt(allReps.size())
    } else { 0.0 };

    {
      totalProfiles = profiles.size();
      verifiedProfiles = verifiedProfilesCount;
      totalVerifications = verifications.size();
      totalReputations = userReputations.size(); // jumlah entri reputasi per user map
      averageReputation = avgReputation;
    }
  };

  // ----------------------------
  // Updates (Writes)
  // ----------------------------

  // Create or update user profile
  public shared(msg) func updateProfile(
    name: Text,
    email: Text,
    bio: Text,
    skills: [Text],
    portfolioUrl: Text,
    location: Text,
    experienceLevel: Text
  ) : async Result.Result<Text, Text> {
    let userPrincipal = msg.caller;
    let currentTime = Time.now();

    let profile : UserProfile = switch (profiles.get(userPrincipal)) {
      case (null) {
        {
          principal = userPrincipal;
          name = name;
          email = email;
          bio = bio;
          skills = skills;
          portfolio_url = portfolioUrl;
          location = location;
          experience_level = experienceLevel;
          verification_status = #Pending;
          reputation_score = 0.0;
          created_at = currentTime;
          updated_at = currentTime;
        }
      };
      case (?existing) {
        {
          existing with
          name = name;
          email = email;
          bio = bio;
          skills = skills;
          portfolio_url = portfolioUrl;
          location = location;
          experience_level = experienceLevel;
          updated_at = currentTime;
        }
      };
    };

    profiles.put(userPrincipal, profile);
    Debug.print("Profile updated for: " # Principal.toText(userPrincipal));
    #ok("Profile updated successfully")
  };

  // Submit verification request
  public shared(msg) func submitVerification(
    verificationType: Text,
    verificationData: Text
  ) : async Result.Result<Text, Text> {
    let userPrincipal = msg.caller;
    let verificationId = "ver_" # Nat.toText(nextVerificationId);
    nextVerificationId += 1;

    let verification: VerificationRecord = {
      id = verificationId;
      user_principal = userPrincipal;
      verification_type = verificationType;
      verification_data = verificationData;
      status = #Pending;
      verified_at = null;
      expires_at = null;
      verifier = null;
    };

    verifications.put(verificationId, verification);

    // Add to user verifications list
    switch (userVerifications.get(userPrincipal)) {
      case (null) { userVerifications.put(userPrincipal, [verificationId]) };
      case (?existing) {
        let newer = Array.append<Text>(existing, [verificationId]);
        userVerifications.put(userPrincipal, newer);
      };
    };

    Debug.print("Verification submitted: " # verificationId);
    #ok(verificationId)
  };

  // Process verification (admin function – add role check in production)
  public shared(msg) func processVerification(
    verificationId: Text,
    approved: Bool,
    expiresAt: ?Int
  ) : async Result.Result<Text, Text> {
    switch (verifications.get(verificationId)) {
      case (null) { #err("Verification not found") };
      case (?verification) {
        let newStatus = if (approved) { #Verified } else { #Rejected };
        let verifiedAt = if (approved) { ?Time.now() } else { null };

        let updatedVerification: VerificationRecord = {
          verification with
          status = newStatus;
          verified_at = verifiedAt;
          expires_at = expiresAt;
          verifier = ?msg.caller;
        };
        verifications.put(verificationId, updatedVerification);

        // If identity verification approved, mark profile as Verified
        if (verification.verification_type == "identity" and approved) {
          switch (profiles.get(verification.user_principal)) {
            case (null) {};
            case (?profile) {
              let updatedProfile: UserProfile = {
                profile with
                verification_status = #Verified;
                updated_at = Time.now();
              };
              profiles.put(verification.user_principal, updatedProfile);
            };
          };
        };

        Debug.print("Verification processed: " # verificationId);
        #ok("Verification processed successfully")
      };
    }
  };

  // Add reputation/review
  public shared(msg) func addReputation(
    userPrincipal: Principal,
    jobId: Text,
    rating: Float,
    review: Text
  ) : async Result.Result<Text, Text> {
    if (rating < 1.0 or rating > 5.0) {
      return #err("Rating must be between 1.0 and 5.0");
    };

    let reputationId = "rep_" # Nat.toText(nextReputationId);
    nextReputationId += 1;

    let reputationEntry: ReputationEntry = {
      id = reputationId;
      user_principal = userPrincipal;
      job_id = jobId;
      rating = rating;
      review = review;
      reviewer = msg.caller;
      created_at = Time.now();
    };

    reputations.put(reputationId, reputationEntry);

    // Add to user reputation list
    switch (userReputations.get(userPrincipal)) {
      case (null) { userReputations.put(userPrincipal, [reputationId]) };
      case (?existing) {
        let newer = Array.append<Text>(existing, [reputationId]);
        userReputations.put(userPrincipal, newer);
      };
    };

    // Update user's reputation score
    await updateUserReputationScore(userPrincipal);

    Debug.print("Reputation added: " # reputationId);
    #ok(reputationId)
  };

  // ----------------------------
  // Internal helpers
  // ----------------------------

  private func updateUserReputationScore(userPrincipal: Principal) : async () {
    switch (userReputations.get(userPrincipal)) {
      case (null) {};
      case (?repIds) {
        var totalRating : Float = 0.0;
        var ratingCount : Nat = 0;

        for (repId in repIds.vals()) {
          switch (reputations.get(repId)) {
            case (null) {};
            case (?rep) {
              totalRating += rep.rating;
              ratingCount += 1;
            };
          };
        };

        if (ratingCount > 0) {
          let averageRating = totalRating / Float.fromInt(ratingCount);
          switch (profiles.get(userPrincipal)) {
            case (null) {};
            case (?profile) {
              let updatedProfile: UserProfile = {
                profile with
                reputation_score = averageRating;
                updated_at = Time.now();
              };
              profiles.put(userPrincipal, updatedProfile);
            };
          };
        };
      };
    };
  };
}

/**
 * Identity Contract - ICP Smart Contract for User Identity Management
 * Handles user profiles, verification, and reputation on Internet Computer
 */

import Debug "mo:base/Debug";
import HashMap "mo:base/HashMap";
import Text "mo:base/Text";
import Time "mo:base/Time";
import Array "mo:base/Array";
import Result "mo:base/Result";
import Principal "mo:base/Principal";
import Float "mo:base/Float";
import Nat "mo:base/Nat";
import Iter "mo:base/Iter";

actor IdentityContract {

  // ----------------------------
  // Type Definitions
  // ----------------------------

  public type VerificationStatus = {
    #Pending;
    #Verified;
    #Rejected;
    #Expired;
  };

  public type UserProfile = {
    principal: Principal;
    name: Text;
    email: Text;
    bio: Text;
    skills: [Text];
    portfolio_url: Text;
    location: Text;
    experience_level: Text;
    verification_status: VerificationStatus;
    reputation_score: Float;
    created_at: Int;
    updated_at: Int;
  };

  public type VerificationRecord = {
    id: Text;
    user_principal: Principal;
    verification_type: Text; // "email", "identity", "skills", "portfolio"
    verification_data: Text;
    status: VerificationStatus;
    verified_at: ?Int;
    expires_at: ?Int;
    verifier: ?Principal;
  };

  public type ReputationEntry = {
    id: Text;
    user_principal: Principal;
    job_id: Text;
    rating: Float; // 1.0 to 5.0
    review: Text;
    reviewer: Principal;
    created_at: Int;
  };

  // ----------------------------
  // Stable State (persists across upgrades)
  // ----------------------------

  // Counters
  stable var nextVerificationId : Nat = 1;
  stable var nextReputationId   : Nat = 1;

  // Snapshots for maps (since HashMap itself cannot be stable)
  stable var profilesStore           : [(Principal, UserProfile)] = [];
  stable var verificationsStore      : [(Text, VerificationRecord)] = [];
  stable var userVerificationsStore  : [(Principal, [Text])] = [];
  stable var reputationsStore        : [(Text, ReputationEntry)] = [];
  stable var userReputationsStore    : [(Principal, [Text])] = [];

  // ----------------------------
  // In-memory Maps
  // ----------------------------

  var profiles = HashMap.HashMap<Principal, UserProfile>(10, Principal.equal, Principal.hash);
  var verifications = HashMap.HashMap<Text, VerificationRecord>(50, Text.equal, Text.hash);
  var userVerifications = HashMap.HashMap<Principal, [Text]>(10, Principal.equal, Principal.hash);
  var reputations = HashMap.HashMap<Text, ReputationEntry>(100, Text.equal, Text.hash);
  var userReputations = HashMap.HashMap<Principal, [Text]>(10, Principal.equal, Principal.hash);

  // ----------------------------
  // Upgrade Hooks
  // ----------------------------

  system func preupgrade() {
    profilesStore := Iter.toArray(profiles.entries());
    verificationsStore := Iter.toArray(verifications.entries());
    userVerificationsStore := Iter.toArray(userVerifications.entries());
    reputationsStore := Iter.toArray(reputations.entries());
    userReputationsStore := Iter.toArray(userReputations.entries());
  };

  system func postupgrade() {
    // Rehydrate all maps from their stable snapshots
    profiles := HashMap.HashMap<Principal, UserProfile>(Nat.max(10, profilesStore.size() * 2), Principal.equal, Principal.hash);
    for ((k, v) in profilesStore.vals()) { profiles.put(k, v) };

    verifications := HashMap.HashMap<Text, VerificationRecord>(Nat.max(50, verificationsStore.size() * 2), Text.equal, Text.hash);
    for ((k, v) in verificationsStore.vals()) { verifications.put(k, v) };

    userVerifications := HashMap.HashMap<Principal, [Text]>(Nat.max(10, userVerificationsStore.size() * 2), Principal.equal, Principal.hash);
    for ((k, v) in userVerificationsStore.vals()) { userVerifications.put(k, v) };

    reputations := HashMap.HashMap<Text, ReputationEntry>(Nat.max(100, reputationsStore.size() * 2), Text.equal, Text.hash);
    for ((k, v) in reputationsStore.vals()) { reputations.put(k, v) };

    userReputations := HashMap.HashMap<Principal, [Text]>(Nat.max(10, userReputationsStore.size() * 2), Principal.equal, Principal.hash);
    for ((k, v) in userReputationsStore.vals()) { userReputations.put(k, v) };
  };

  // ----------------------------
  // Queries (Reads)
  // ----------------------------

  // Get all user profiles
  public query func getAllProfiles() : async [UserProfile] {
    Iter.toArray(profiles.vals())
  };
  // Get user profile
  public query func getUserProfile(userPrincipal: Principal) : async ?UserProfile {
    profiles.get(userPrincipal)
  };

  // Get verification by ID
  public query func getVerification(verificationId: Text) : async ?VerificationRecord {
    verifications.get(verificationId)
  };

  // Get user verifications
  public query func getUserVerifications(userPrincipal: Principal) : async [VerificationRecord] {
    switch (userVerifications.get(userPrincipal)) {
      case (null) { [] };
      case (?verIds) {
        Array.mapFilter<Text, VerificationRecord>(
          verIds,
          func (verId: Text) : ?VerificationRecord { verifications.get(verId) }
        )
      };
    }
  };

  // Get user reputation entries
  public query func getUserReputations(userPrincipal: Principal) : async [ReputationEntry] {
    switch (userReputations.get(userPrincipal)) {
      case (null) { [] };
      case (?repIds) {
        Array.mapFilter<Text, ReputationEntry>(
          repIds,
          func (repId: Text) : ?ReputationEntry { reputations.get(repId) }
        )
      };
    }
  };

  // Get my profile
  public shared(msg) func getMyProfile() : async ?UserProfile {
    profiles.get(msg.caller)
  };

  // Get pending verifications (admin/reporting)
  public query func getPendingVerifications() : async [VerificationRecord] {
    let allVerifications = Iter.toArray(verifications.vals());
    Array.filter<VerificationRecord>(
      allVerifications,
      func (ver: VerificationRecord) : Bool { ver.status == #Pending }
    )
  };

  // Search profiles by skills (case-insensitive ANY-match)
  public query func searchProfilesBySkills(searchSkills: [Text]) : async [UserProfile] {
    let allProfiles = Iter.toArray(profiles.vals());
    Array.filter<UserProfile>(
      allProfiles,
      func (profile: UserProfile) : Bool {
        Array.find<Text>(
          searchSkills,
          func (searchSkill: Text) : Bool {
            Array.find<Text>(
              profile.skills,
              func (userSkill: Text) : Bool {
                Text.equal(Text.toLowercase(userSkill), Text.toLowercase(searchSkill))
              }
            ) != null
          }
        ) != null
      }
    )
  };

  // Get contract statistics
  public query func getContractStats() : async {
    totalProfiles: Nat;
    verifiedProfiles: Nat;
    totalVerifications: Nat;
    totalReputations: Nat;
    averageReputation: Float;
  } {
    let allProfiles = Iter.toArray(profiles.vals());
    let verifiedProfilesCount = Array.filter<UserProfile>(
      allProfiles,
      func (p: UserProfile) : Bool { p.verification_status == #Verified }
    ).size();

    let allReps = Iter.toArray(reputations.vals());
    let totalRating = Array.foldLeft<ReputationEntry, Float>(
      allReps,
      0.0,
      func (acc: Float, r: ReputationEntry) : Float { acc + r.rating }
    );
    let avgReputation = if (allReps.size() > 0) {
      totalRating / Float.fromInt(allReps.size())
    } else { 0.0 };

    {
      totalProfiles = profiles.size();
      verifiedProfiles = verifiedProfilesCount;
      totalVerifications = verifications.size();
      totalReputations = userReputations.size(); // jumlah entri reputasi per user map
      averageReputation = avgReputation;
    }
  };

  // ----------------------------
  // Updates (Writes)
  // ----------------------------

  // Create or update user profile
  public shared(msg) func updateProfile(
    name: Text,
    email: Text,
    bio: Text,
    skills: [Text],
    portfolioUrl: Text,
    location: Text,
    experienceLevel: Text
  ) : async Result.Result<Text, Text> {
    let userPrincipal = msg.caller;
    let currentTime = Time.now();

    let profile : UserProfile = switch (profiles.get(userPrincipal)) {
      case (null) {
        {
          principal = userPrincipal;
          name = name;
          email = email;
          bio = bio;
          skills = skills;
          portfolio_url = portfolioUrl;
          location = location;
          experience_level = experienceLevel;
          verification_status = #Pending;
          reputation_score = 0.0;
          created_at = currentTime;
          updated_at = currentTime;
        }
      };
      case (?existing) {
        {
          existing with
          name = name;
          email = email;
          bio = bio;
          skills = skills;
          portfolio_url = portfolioUrl;
          location = location;
          experience_level = experienceLevel;
          updated_at = currentTime;
        }
      };
    };

    profiles.put(userPrincipal, profile);
    Debug.print("Profile updated for: " # Principal.toText(userPrincipal));
    #ok("Profile updated successfully")
  };

  // Submit verification request
  public shared(msg) func submitVerification(
    verificationType: Text,
    verificationData: Text
  ) : async Result.Result<Text, Text> {
    let userPrincipal = msg.caller;
    let verificationId = "ver_" # Nat.toText(nextVerificationId);
    nextVerificationId += 1;

    let verification: VerificationRecord = {
      id = verificationId;
      user_principal = userPrincipal;
      verification_type = verificationType;
      verification_data = verificationData;
      status = #Pending;
      verified_at = null;
      expires_at = null;
      verifier = null;
    };

    verifications.put(verificationId, verification);

    // Add to user verifications list
    switch (userVerifications.get(userPrincipal)) {
      case (null) { userVerifications.put(userPrincipal, [verificationId]) };
      case (?existing) {
        let newer = Array.append<Text>(existing, [verificationId]);
        userVerifications.put(userPrincipal, newer);
      };
    };

    Debug.print("Verification submitted: " # verificationId);
    #ok(verificationId)
  };

  // Process verification (admin function – add role check in production)
  public shared(msg) func processVerification(
    verificationId: Text,
    approved: Bool,
    expiresAt: ?Int
  ) : async Result.Result<Text, Text> {
    switch (verifications.get(verificationId)) {
      case (null) { #err("Verification not found") };
      case (?verification) {
        let newStatus = if (approved) { #Verified } else { #Rejected };
        let verifiedAt = if (approved) { ?Time.now() } else { null };

        let updatedVerification: VerificationRecord = {
          verification with
          status = newStatus;
          verified_at = verifiedAt;
          expires_at = expiresAt;
          verifier = ?msg.caller;
        };
        verifications.put(verificationId, updatedVerification);

        // If identity verification approved, mark profile as Verified
        if (verification.verification_type == "identity" and approved) {
          switch (profiles.get(verification.user_principal)) {
            case (null) {};
            case (?profile) {
              let updatedProfile: UserProfile = {
                profile with
                verification_status = #Verified;
                updated_at = Time.now();
              };
              profiles.put(verification.user_principal, updatedProfile);
            };
          };
        };

        Debug.print("Verification processed: " # verificationId);
        #ok("Verification processed successfully")
      };
    }
  };

  // Add reputation/review
  public shared(msg) func addReputation(
    userPrincipal: Principal,
    jobId: Text,
    rating: Float,
    review: Text
  ) : async Result.Result<Text, Text> {
    if (rating < 1.0 or rating > 5.0) {
      return #err("Rating must be between 1.0 and 5.0");
    };

    let reputationId = "rep_" # Nat.toText(nextReputationId);
    nextReputationId += 1;

    let reputationEntry: ReputationEntry = {
      id = reputationId;
      user_principal = userPrincipal;
      job_id = jobId;
      rating = rating;
      review = review;
      reviewer = msg.caller;
      created_at = Time.now();
    };

    reputations.put(reputationId, reputationEntry);

    // Add to user reputation list
    switch (userReputations.get(userPrincipal)) {
      case (null) { userReputations.put(userPrincipal, [reputationId]) };
      case (?existing) {
        let newer = Array.append<Text>(existing, [reputationId]);
        userReputations.put(userPrincipal, newer);
      };
    };

    // Update user's reputation score
    await updateUserReputationScore(userPrincipal);

    Debug.print("Reputation added: " # reputationId);
    #ok(reputationId)
  };

  // ----------------------------
  // Internal helpers
  // ----------------------------

  private func updateUserReputationScore(userPrincipal: Principal) : async () {
    switch (userReputations.get(userPrincipal)) {
      case (null) {};
      case (?repIds) {
        var totalRating : Float = 0.0;
        var ratingCount : Nat = 0;

        for (repId in repIds.vals()) {
          switch (reputations.get(repId)) {
            case (null) {};
            case (?rep) {
              totalRating += rep.rating;
              ratingCount += 1;
            };
          };
        };

        if (ratingCount > 0) {
          let averageRating = totalRating / Float.fromInt(ratingCount);
          switch (profiles.get(userPrincipal)) {
            case (null) {};
            case (?profile) {
              let updatedProfile: UserProfile = {
                profile with
                reputation_score = averageRating;
                updated_at = Time.now();
              };
              profiles.put(userPrincipal, updatedProfile);
            };
          };
        };
      };
    };
  };
}
