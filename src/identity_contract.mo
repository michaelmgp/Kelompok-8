/**
 * Identity Contract - ICP Smart Contract for User Identity Management
 * Handles user profiles, verification, and reputation on Internet Computer
 */

import Debug "mo:base/Debug";
import HashMap "mo:base/HashMap";
import Text "mo:base/Text";
import Time "mo:base/Time";
import Array "mo:base/Array";
import Option "mo:base/Option";
import Result "mo:base/Result";
import Principal "mo:base/Principal";
import Float "mo:base/Float";
import Nat "mo:base/Nat";
// import Char "mo:base/Char";
import Iter "mo:base/Iter";

persistent actor IdentityContract {
    
    // Verification status types
    public type VerificationStatus = {
        #Pending;
        #Verified;
        #Rejected;
        #Expired;
    };
    
    // User profile structure
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
    
    // Verification record structure
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
    
    // Reputation entry structure
    public type ReputationEntry = {
        id: Text;
        user_principal: Principal;
        job_id: Text;
        rating: Float; // 1.0 to 5.0
        review: Text;
        reviewer: Principal;
        created_at: Int;
    };
    
    // Contract state
private var nextVerificationId: Nat = 1;
private var nextReputationId: Nat = 1;
    
    private transient var profiles = HashMap.HashMap<Principal, UserProfile>(10, Principal.equal, Principal.hash);
    private transient var verifications = HashMap.HashMap<Text, VerificationRecord>(50, Text.equal, Text.hash);
    private transient var userVerifications = HashMap.HashMap<Principal, [Text]>(10, Principal.equal, Principal.hash);
    private transient var reputations = HashMap.HashMap<Text, ReputationEntry>(100, Text.equal, Text.hash);
    private transient var userReputations = HashMap.HashMap<Principal, [Text]>(10, Principal.equal, Principal.hash);
    
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
        
        let profile: UserProfile = switch (profiles.get(userPrincipal)) {
            case (null) {
                // Create new profile
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
            case (?existingProfile) {
                // Update existing profile
                {
                    existingProfile with
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
            case (?existingVers) { 
                let newVers = Array.append(existingVers, [verificationId]);
                userVerifications.put(userPrincipal, newVers);
            };
        };
        
        Debug.print("Verification submitted: " # verificationId);
        #ok(verificationId)
    };
    
    // Process verification (admin function)
    public shared(msg) func processVerification(
        verificationId: Text,
        approved: Bool,
        expiresAt: ?Int
    ) : async Result.Result<Text, Text> {
        
        // In production, add admin role check here
        
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
                
                // Update user profile verification status if identity verification
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
            case (?existingReps) { 
                let newReps = Array.append(existingReps, [reputationId]);
                userReputations.put(userPrincipal, newReps);
            };
        };
        
        // Update user's reputation score
        await updateUserReputationScore(userPrincipal);
        
        Debug.print("Reputation added: " # reputationId);
        #ok(reputationId)
    };
    
    // Update user reputation score
    private func updateUserReputationScore(userPrincipal: Principal) : async () {
        switch (userReputations.get(userPrincipal)) {
            case (null) {};
            case (?repIds) {
                var totalRating: Float = 0.0;
                var ratingCount: Nat = 0;
                
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
    
    // Get user profile
    public query func getUserProfile(userPrincipal: Principal) : async ?UserProfile {
        profiles.get(userPrincipal)
    };
    
    // Get user verifications
    public query func getUserVerifications(userPrincipal: Principal) : async [VerificationRecord] {
        switch (userVerifications.get(userPrincipal)) {
            case (null) { [] };
            case (?verIds) {
                let verificationsArray = Array.mapFilter<Text, VerificationRecord>(
                    verIds,
                    func(verId: Text) : ?VerificationRecord {
                        verifications.get(verId)
                    }
                );
                verificationsArray
            };
        }
    };
    
    // Get user reputation entries
    public query func getUserReputations(userPrincipal: Principal) : async [ReputationEntry] {
        switch (userReputations.get(userPrincipal)) {
            case (null) { [] };
            case (?repIds) {
                let reputationsArray = Array.mapFilter<Text, ReputationEntry>(
                    repIds,
                    func(repId: Text) : ?ReputationEntry {
                        reputations.get(repId)
                    }
                );
                reputationsArray
            };
        }
    };
    
    // Get my profile
    public shared(msg) func getMyProfile() : async ?UserProfile {
        profiles.get(msg.caller)
    };
    
    // Get verification by ID
    public query func getVerification(verificationId: Text) : async ?VerificationRecord {
        verifications.get(verificationId)
    };
    
    // Get pending verifications (admin function)
    public query func getPendingVerifications() : async [VerificationRecord] {
        let allVerifications = verifications.vals();
        let pendingVerifications = Array.filter<VerificationRecord>(
            Iter.toArray(allVerifications),
            func(ver: VerificationRecord) : Bool {
                ver.status == #Pending
            }
        );
        pendingVerifications
    };
    
    // Search profiles by skills
    public query func searchProfilesBySkills(searchSkills: [Text]) : async [UserProfile] {
        let allProfiles = profiles.vals();
        let matchingProfiles = Array.filter<UserProfile>(
            Iter.toArray(allProfiles),
            func(profile: UserProfile) : Bool {
                // Check if profile has any of the search skills
                Array.find<Text>(searchSkills, func(searchSkill: Text) : Bool {
                    Array.find<Text>(profile.skills, func(userSkill: Text) : Bool {
                        Text.equal(Text.toLowercase(userSkill), Text.toLowercase(searchSkill))
                    }) != null
                }) != null
            }
        );
        matchingProfiles
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
        let verifiedProfilesCount = Array.filter<UserProfile>(allProfiles, func(profile: UserProfile) : Bool {
            profile.verification_status == #Verified
        }).size();
        let allReputations = Iter.toArray(reputations.vals());
        let totalRating = Array.foldLeft<ReputationEntry, Float>(
            allReputations,
            0.0,
            func(acc: Float, rep: ReputationEntry) : Float {
                acc + rep.rating
            }
        );
        let avgReputation = if (allReputations.size() > 0) {
            totalRating / Float.fromInt(allReputations.size())
        } else { 0.0 };
        {
            totalProfiles = profiles.size();
            verifiedProfiles = verifiedProfilesCount;
            totalVerifications = verifications.size();
            totalReputations = reputations.size();
            averageReputation = avgReputation;
        }
    };
}