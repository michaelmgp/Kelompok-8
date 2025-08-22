import HashMap "mo:base/HashMap";
import Nat "mo:base/Nat";
import Nat32 "mo:base/Nat32";
import Text "mo:base/Text";
import Time "mo:base/Time";
import Iter "mo:base/Iter";
import Error "mo:base/Error";
import Hash "mo:base/Hash";

type AgentId = Nat;
type AgentRecord = {
    id: AgentId;
    nama: Text;
    email: Text;
    role: Text;
    createdAt: Int;
};

actor AgentContract {
    var nextAgentId: Nat = 1;
    var agentList: [(AgentId, AgentRecord)] = [];

    // Hash function custom untuk Nat (ID kecil, cukup gunakan nilai Nat itu sendiri)
    func natHash(n: Nat) : Hash.Hash { Nat32.fromNat(n) }

    private var agents: HashMap.HashMap<AgentId, AgentRecord> = HashMap.HashMap<AgentId, AgentRecord>(100, Nat.equal, natHash);

    system func preupgrade() {
        agentList := Iter.toArray(agents.entries());
    };

    system func postupgrade() {
        agents := HashMap.HashMap<AgentId, AgentRecord>(100, Nat.equal, natHash);
        for ((id, record) in agentList.vals()) {
            agents.put(id, record);
        };
    };

    public shared(msg) func addAgent(nama: Text, email: Text, role: Text) : async AgentId {
        if (Text.size(nama) == 0 or Text.size(email) == 0 or Text.size(role) == 0) {
            throw Error.reject("Nama, email, dan role tidak boleh kosong");
        };

        let id = nextAgentId;
        nextAgentId += 1;

        let agent: AgentRecord = {
            id = id;
            nama = nama;
            email = email;
            role = role;
            createdAt = Time.now();
        };

        agents.put(id, agent);
        id
    };

    public query func getAgent(id: AgentId) : async ?AgentRecord {
        agents.get(id)
    };

    public query func listAgents() : async [AgentRecord] {
        Iter.toArray(agents.vals())
    };

    public shared(msg) func updateAgent(id: AgentId, nama: Text, email: Text, role: Text) : async Bool {
        switch (agents.get(id)) {
            case (?existing) {
                let updated: AgentRecord = {
                    id = id;
                    nama = nama;
                    email = email;
                    role = role;
                    createdAt = existing.createdAt;
                };
                agents.put(id, updated);
                true
            };
            case (_) false
        }
    };

    public shared(msg) func deleteAgent(id: AgentId) : async Bool {
        switch (agents.remove(id)) {
            case (?_) true;
            case (_) false
        }
    };
}