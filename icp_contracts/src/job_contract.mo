/**
 * Job Contract - ICP Smart Contract for Job Management
 * Handles job listings, applications, and payments on Internet Computer
 */

import Debug "mo:base/Debug";
import HashMap "mo:base/HashMap";
import Text "mo:base/Text";
import Time "mo:base/Time";
import Array "mo:base/Array";
import Option "mo:base/Option";
import Result "mo:base/Result";
import Principal "mo:base/Principal";
import Nat "mo:base/Nat";
import Iter "mo:base/Iter";

persistent actor JobContract {
    
    // Job status types
    public type JobStatus = {
        #Open;
        #InProgress;
        #Completed;
        #Cancelled;
    };
    
    // Application status types
    public type ApplicationStatus = {
        #Submitted;
        #UnderReview;
        #Accepted;
        #Rejected;
        #Withdrawn;
    };
    
    // Job record structure
    public type JobRecord = {
        id: Text;
        title: Text;
        description: Text;
        budget: Text;
        skills: [Text];
        client: Principal;
        status: JobStatus;
        created_at: Int;
        deadline: ?Int;
        selected_freelancer: ?Principal;
    };
    
    // Application record structure
    public type ApplicationRecord = {
        id: Text;
        job_id: Text;
        applicant: Principal;
        cover_letter: Text;
        proposed_budget: Text;
        status: ApplicationStatus;
        applied_at: Int;
        reviewed_at: ?Int;
    };
    
    // Contract state
    private stable var nextJobId: Nat = 1;
    private stable var nextApplicationId: Nat = 1;
    
    private transient var jobs = HashMap.HashMap<Text, JobRecord>(10, Text.equal, Text.hash);
    private transient var applications = HashMap.HashMap<Text, ApplicationRecord>(50, Text.equal, Text.hash);
    private transient var jobApplications = HashMap.HashMap<Text, [Text]>(10, Text.equal, Text.hash);
    
    // Create a new job listing
    public shared(msg) func createJob(
        title: Text,
        description: Text,
        budget: Text,
        skills: [Text],
        deadline: ?Int
    ) : async Result.Result<Text, Text> {
        
        let jobId = "job_" # Nat.toText(nextJobId);
        nextJobId += 1;
        
        let job: JobRecord = {
            id = jobId;
            title = title;
            description = description;
            budget = budget;
            skills = skills;
            client = msg.caller;
            status = #Open;
            created_at = Time.now();
            deadline = deadline;
            selected_freelancer = null;
        };
        
        jobs.put(jobId, job);
        jobApplications.put(jobId, []);
        
        Debug.print("Job created: " # jobId);
        #ok(jobId)
    };
    
    // Submit job application
    public shared(msg) func submitApplication(
        jobId: Text,
        coverLetter: Text,
        proposedBudget: Text
    ) : async Result.Result<Text, Text> {
        
        switch (jobs.get(jobId)) {
            case (null) { #err("Job not found") };
            case (?job) {
                if (job.status != #Open) {
                    return #err("Job is not open for applications");
                };
                
                let applicationId = "app_" # Nat.toText(nextApplicationId);
                nextApplicationId += 1;
                
                let application: ApplicationRecord = {
                    id = applicationId;
                    job_id = jobId;
                    applicant = msg.caller;
                    cover_letter = coverLetter;
                    proposed_budget = proposedBudget;
                    status = #Submitted;
                    applied_at = Time.now();
                    reviewed_at = null;
                };
                
                applications.put(applicationId, application);
                
                // Add to job applications list
                switch (jobApplications.get(jobId)) {
                    case (null) { jobApplications.put(jobId, [applicationId]) };
                    case (?existingApps) { 
                        let newApps = Array.append(existingApps, [applicationId]);
                        jobApplications.put(jobId, newApps);
                    };
                };
                
                Debug.print("Application submitted: " # applicationId);
                #ok(applicationId)
            };
        }
    };
    
    // Accept application and start job
    public shared(msg) func acceptApplication(
        applicationId: Text
    ) : async Result.Result<Text, Text> {
        
        switch (applications.get(applicationId)) {
            case (null) { #err("Application not found") };
            case (?application) {
                switch (jobs.get(application.job_id)) {
                    case (null) { #err("Job not found") };
                    case (?job) {
                        if (job.client != msg.caller) {
                            return #err("Only job client can accept applications");
                        };
                        
                        if (job.status != #Open) {
                            return #err("Job is not open");
                        };
                        
                        // Update application status
                        let updatedApplication: ApplicationRecord = {
                            application with 
                            status = #Accepted;
                            reviewed_at = ?Time.now();
                        };
                        applications.put(applicationId, updatedApplication);
                        
                        // Update job status and assign freelancer
                        let updatedJob: JobRecord = {
                            job with 
                            status = #InProgress;
                            selected_freelancer = ?application.applicant;
                        };
                        jobs.put(application.job_id, updatedJob);
                        
                        // Reject other applications for this job
                        switch (jobApplications.get(application.job_id)) {
                            case (null) {};
                            case (?appIds) {
                                for (appId in appIds.vals()) {
                                    if (appId != applicationId) {
                                        switch (applications.get(appId)) {
                                            case (null) {};
                                            case (?otherApp) {
                                                if (otherApp.status == #Submitted or otherApp.status == #UnderReview) {
                                                    let rejectedApp: ApplicationRecord = {
                                                        otherApp with 
                                                        status = #Rejected;
                                                        reviewed_at = ?Time.now();
                                                    };
                                                    applications.put(appId, rejectedApp);
                                                };
                                            };
                                        };
                                    };
                                };
                            };
                        };
                        
                        Debug.print("Application accepted: " # applicationId);
                        #ok("Application accepted and job started")
                    };
                };
            };
        }
    };
    
    // Complete job
    public shared(msg) func completeJob(
        jobId: Text
    ) : async Result.Result<Text, Text> {
        
        switch (jobs.get(jobId)) {
            case (null) { #err("Job not found") };
            case (?job) {
                if (job.client != msg.caller) {
                    return #err("Only job client can complete jobs");
                };
                
                if (job.status != #InProgress) {
                    return #err("Job is not in progress");
                };
                
                let completedJob: JobRecord = {
                    job with status = #Completed;
                };
                jobs.put(jobId, completedJob);
                
                Debug.print("Job completed: " # jobId);
                #ok("Job marked as completed")
            };
        }
    };
    
    // Get job details
    public query func getJob(jobId: Text) : async ?JobRecord {
        jobs.get(jobId)
    };
    
    // Get application details
    public query func getApplication(applicationId: Text) : async ?ApplicationRecord {
        applications.get(applicationId)
    };
    
    // Get all jobs (limited to recent ones)
    public query func getAllJobs() : async [JobRecord] {
        let jobArray = jobs.vals();
        Iter.toArray(jobArray)
    };
    
    // Get applications for a specific job
    public query func getJobApplications(jobId: Text) : async [ApplicationRecord] {
        switch (jobApplications.get(jobId)) {
            case (null) { [] };
            case (?appIds) {
                let applicationsArray = Array.mapFilter<Text, ApplicationRecord>(
                    appIds, 
                    func(appId: Text) : ?ApplicationRecord {
                        applications.get(appId)
                    }
                );
                applicationsArray
            };
        }
    };
    
    // Get user's applications
    public shared(msg) func getMyApplications() : async [ApplicationRecord] {
        let userPrincipal = msg.caller;
        let allApplications = applications.vals();
        let userApplications = Array.filter<ApplicationRecord>(
            Iter.toArray(allApplications),
            func(app: ApplicationRecord) : Bool {
                app.applicant == userPrincipal
            }
        );
        userApplications
    };
    
    // Get user's jobs (as client)
    public shared(msg) func getMyJobs() : async [JobRecord] {
        let userPrincipal = msg.caller;
        let allJobs = jobs.vals();
        let userJobs = Array.filter<JobRecord>(
            Iter.toArray(allJobs),
            func(job: JobRecord) : Bool {
                job.client == userPrincipal
            }
        );
        userJobs
    };
    
    // Get contract statistics
    public query func getContractStats() : async {
        totalJobs: Nat;
        totalApplications: Nat;
        openJobs: Nat;
        completedJobs: Nat;
    } {
        let allJobs = Iter.toArray(jobs.vals());
        let openJobsCount = Array.filter<JobRecord>(allJobs, func(job: JobRecord) : Bool {
            job.status == #Open
        }).size();
        let completedJobsCount = Array.filter<JobRecord>(allJobs, func(job: JobRecord) : Bool {
            job.status == #Completed
        }).size();
        {
            totalJobs = jobs.size();
            totalApplications = applications.size();
            openJobs = openJobsCount;
            completedJobs = completedJobsCount;
        }
    };
}