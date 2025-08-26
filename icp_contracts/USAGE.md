# Dokumentasi Penggunaan Canister ICP (database.mo)

## Struktur Data
- User
- Job
- Chat
- Agent

## Fungsi CRUD

### User
- `addUser(nama, email, profesionalBG, pengalamanKerja, jurusanSekolah, jobReferensi)` → UserId
- `getUser(id)` → ?User
- `listUsers()` → [User]

### Job
- `addJob(namaJob, url, source)` → JobId
- `getJob(id)` → ?Job
- `listJobs()` → [Job]

### Chat
- `addChat(userId, pesan, timestamp)` → ChatId
- `getChat(id)` → ?Chat
- `listChats()` → [Chat]

### Agent
- `addAgent(nama, email, role, createdAt)` → AgentId
- `getAgent(id)` → ?Agent
- `listAgents()` → [Agent]

## Contoh Penggunaan

### Menambah User
```motoko
let userId = await Database.addUser(
    "Budi", "budi@email.com", "Web Developer", "3 tahun", "Teknik Informatika", null
);
```

### Mendapatkan User
```motoko
let user = await Database.getUser(userId);
```

### Menambah Job
```motoko
let jobId = await Database.addJob(
    "Frontend Developer", "https://example.com/job/123", #Scraping("Upwork")
);
```

### Mendapatkan Job
```motoko
let job = await Database.getJob(jobId);
```

### Menambah Chat
```motoko
let chatId = await Database.addChat(userId, "Halo, saya tertarik!", 1692619200);
```

### Mendapatkan Chat
```motoko
let chat = await Database.getChat(chatId);
```

### Menambah Agent
```motoko
let agentId = await Database.addAgent("Admin", "admin@email.com", "admin", 1692619200);
```

### Mendapatkan Agent
```motoko
let agent = await Database.getAgent(agentId);
```

## Deploy & Testing
1. Jalankan DFX:
   ```bash
   dfx start --background
   dfx deploy
   ```
2. Panggil fungsi-fungsi di atas via Motoko Playground, candid UI, atau frontend ICP.

## Integrasi
- Backend bisa panggil fungsi canister via ICP SDK (lihat `backend_agent/api/icp_integration.py`).
- Frontend bisa fetch data via candid interface.

---
Untuk detail API dan flow, lihat README.md utama.
