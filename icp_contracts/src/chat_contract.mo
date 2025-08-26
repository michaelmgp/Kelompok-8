/**
 * Chat Contract - ICP Smart Contract for Chat Bot History
 * Menyimpan riwayat chat antara user dan bot
 */

import HashMap "mo:base/HashMap";
import Text "mo:base/Text";
import Time "mo:base/Time";
import Nat "mo:base/Nat";
import Principal "mo:base/Principal";
import Array "mo:base/Array";
import Hash "mo:base/Hash";

actor ChatContract {
    public type ChatId = Nat;
    public type ChatRecord = {
        id: ChatId;
        user: Principal;
        pesan: Text;
        timestamp: Int;
    };

    private transient var nextChatId: Nat = 1;
    private transient var chats = HashMap.HashMap<ChatId, ChatRecord>(100, Nat.equal, Hash.hash);
    private transient var userChats = HashMap.HashMap<Principal, [ChatId]>(10, Principal.equal, Principal.hash);

    // Tambah chat baru
    public shared(msg) func addChat(pesan: Text) : async ChatId {
        let id = nextChatId;
        nextChatId += 1;
        let chat: ChatRecord = {
            id = id;
            user = msg.caller;
            pesan = pesan;
            timestamp = Time.now();
        };
        chats.put(id, chat);
        switch (userChats.get(msg.caller)) {
            case (null) { userChats.put(msg.caller, [id]) };
            case (?existing) {
                let newArr = Array.append(existing, [id]);
                userChats.put(msg.caller, newArr);
            };
        };
        id
    };

    // Ambil chat user
    public query func getUserChats(user: Principal) : async [ChatRecord] {
        switch (userChats.get(user)) {
            case (null) { [] };
            case (?ids) {
                Array.map<ChatId, ChatRecord>(ids, func(id: ChatId) : ChatRecord {
                    switch (chats.get(id)) {
                        case (null) { assert false; { id = 0; user = user; pesan = ""; timestamp = 0 } };
                        case (?chat) { chat };
                    }
                })
            };
        }
    };
}
