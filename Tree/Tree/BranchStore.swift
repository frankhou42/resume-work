//
//  BranchStore.swift
//  Tree
//
//  Persists chats and their saved ("Permanent") branches to disk as JSON in
//  Application Support, so branches survive relaunches. This is what makes the
//  "saved branches / reusable context paths" idea real rather than in-memory.
//

import Foundation

final class BranchStore {
    static let shared = BranchStore()

    private let fileURL: URL

    init() {
        let base = FileManager.default.urls(for: .applicationSupportDirectory,
                                            in: .userDomainMask)[0]
        let dir = base.appendingPathComponent("Tree", isDirectory: true)
        try? FileManager.default.createDirectory(at: dir,
                                                 withIntermediateDirectories: true)
        fileURL = dir.appendingPathComponent("chats.json")
    }

    /// Load persisted chats, or nil if nothing has been saved yet.
    func load() -> [Chat]? {
        guard let data = try? Data(contentsOf: fileURL) else { return nil }
        return try? JSONDecoder().decode([Chat].self, from: data)
    }

    /// Persist the full chat list (including saved branches). Best-effort:
    /// a failed write should never crash the UI.
    func save(_ chats: [Chat]) {
        guard let data = try? JSONEncoder().encode(chats) else { return }
        try? data.write(to: fileURL, options: .atomic)
    }
}
