# CARA_PENGGUNAAN.md

## ICP Identity Contract - Cara CRUD & Get Data

### 1. Update/Create Profile
- Fungsi: `updateProfile`
- Tipe: `shared`
- Cara panggil (Candid UI / frontend):
  - Params: `name: Text, email: Text, bio: Text, skills: [Text], portfolioUrl: Text, location: Text, experienceLevel: Text`
  - Contoh:
    ```
    call updateProfile("Aliyya", "ali@example.com", "Bio", ["Motoko", "JS"], "https://portfolio.com", "Jakarta", "Senior")
    ```

### 2. Get Profile
- Fungsi: `getUserProfile`
- Tipe: `query`
- Params: `userPrincipal: Principal`
- Contoh:
    ```
    call getUserProfile("<PRINCIPAL_ID>")
    ```

### 3. Get My Profile
- Fungsi: `getMyProfile`
- Tipe: `shared`
- Params: none
- Contoh:
    ```
    call getMyProfile()
    ```

### 4. Submit Verification
- Fungsi: `submitVerification`
- Tipe: `shared`
- Params: `verificationType: Text, verificationData: Text`
- Contoh:
    ```
    call submitVerification("email", "ali@example.com")
    ```

### 5. Process Verification (Admin)
- Fungsi: `processVerification`
- Tipe: `shared`
- Params: `verificationId: Text, approved: Bool, expiresAt: ?Int`
- Contoh:
    ```
    call processVerification("ver_1", true, null)
    ```

### 6. Get User Verifications
- Fungsi: `getUserVerifications`
- Tipe: `query`
- Params: `userPrincipal: Principal`
- Contoh:
    ```
    call getUserVerifications("<PRINCIPAL_ID>")
    ```

### 7. Add Reputation/Review
- Fungsi: `addReputation`
- Tipe: `shared`
- Params: `userPrincipal: Principal, jobId: Text, rating: Float, review: Text`
- Contoh:
    ```
    call addReputation("<PRINCIPAL_ID>", "job_1", 5.0, "Kerja bagus!")
    ```

### 8. Get User Reputations
- Fungsi: `getUserReputations`
- Tipe: `query`
- Params: `userPrincipal: Principal`
- Contoh:
    ```
    call getUserReputations("<PRINCIPAL_ID>")
    ```

### 9. Get Contract Stats
- Fungsi: `getContractStats`
- Tipe: `query`
- Params: none
- Contoh:
    ```
    call getContractStats()
    ```

### 10. Search Profiles by Skills
- Fungsi: `searchProfilesBySkills`
- Tipe: `query`
- Params: `searchSkills: [Text]`
- Contoh:
    ```
    call searchProfilesBySkills(["Motoko", "JS"])
    ```

---

## ENV

Pastikan .env frontend/backend berisi:
```
NEXT_PUBLIC_IDENTITY_CANISTER_ID=uxrrr-q7777-77774-qaaaq-cai
NEXT_PUBLIC_JOB_CANISTER_ID=u6s2n-gx777-77774-qaaba-cai
```

Ganti sesuai hasil deploy di terminal.

---

## Testing CRUD
- Gunakan Candid UI (http://127.0.0.1:8000/?canisterId=...) untuk test manual.
- Untuk frontend, panggil endpoint sesuai dokumentasi di atas.

Jika butuh contoh request dari frontend (fetch/axios), bisa minta lagi!
