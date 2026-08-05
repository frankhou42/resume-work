# Copilot instructions for Tree

## Project overview
- This is a small SwiftUI macOS app with a single entry point in [Tree/TreeApp.swift](Tree/TreeApp.swift).
- The primary UI is implemented in [Tree/ContentView.swift](Tree/ContentView.swift), which defines all subviews and UI state.

## UI structure & patterns
- `ContentView` is the main screen and holds view state (`@State`) for UI toggles and input.
- Subviews are organized in a private extension on `ContentView` (`mainChatColumn`, `branchPanel`, etc.). Follow this pattern when adding new subviews.
- UI composition uses `HStack` at the root with a conditional side panel (`if showBranch { ... }`) and a `.transition(.move(edge: .trailing))` for the panel.
- Reusable UI bits are implemented as `func` returning `some View` (e.g., `messageRow(_:)`, `branchTypeButton(...)`). Add new reusable components in the same style.

## State & interactions
- `showBranch` controls whether the right-side branch panel is visible; `selectedBranchType` changes button styling and hint text; `branchMessage` backs the text field.
- State updates are used to trigger UI re-rendering; keep new state local to `ContentView` unless it needs to be shared.

## Assets & resources
- Image assets and app icons live under [Tree/Assets.xcassets](Tree/Assets.xcassets).

## Workflows
- Build/run/debug is typically done via Xcode for the `Tree.xcodeproj` project. No custom build scripts or tests were found in the repository.
