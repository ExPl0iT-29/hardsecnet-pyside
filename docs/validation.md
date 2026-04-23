# HardSecNet PySide6 Validation

Date: 2026-04-23
Workspace: `E:\T\hardsecnet\hardsecnet-pyside`
Environment: Windows, Python 3.12, project venv at `E:\T\hardsecnet\hardsecnet-pyside\.venv`

## Verification Performed

1. Installed runtime and dev dependencies
   - `python -m venv .venv`
   - `.venv\Scripts\python.exe -m pip install -e .[dev]`

2. Compiled source tree
   - `.venv\Scripts\python.exe -m compileall src\hardsecnet_pyside`
   - Final verification command: `python -m compileall src tests`

3. Ran test suite
   - `.venv\Scripts\python.exe -m pytest -q tests`
   - Result after final local-baseline polish: `14 passed`
   - Final verification result after dashboard, device, report, and harden fixes: `16 passed`

4. Ran UI smoke check in offscreen mode
   - Created `QApplication`
   - Built main window
   - Refreshed pages
   - Verified navigation count and status bar output

5. Ran service smoke check
   - Bootstrapped `HardSecNetService`
   - Executed `run_profile(...)`
   - Verified run/report artifact creation

6. Ran final runtime bootstrap verification
   - Bootstrapped a fresh local workspace
   - Verified current device creation
   - Verified seeded benchmark documents and controls
   - Verified 3 curated ready scripts
   - Verified guarded dry-run artifact creation
   - Verified local baseline report JSON, HTML, and PDF creation

7. Verified final project artifacts
   - Recreated Blackbook PDF exists, is readable, unencrypted, and has 45 pages
   - Recreated Blackbook DOCX and Markdown companion files exist
   - Removed fleet/control-plane/web-dashboard directories are absent
   - Active `src` and `tests` Python scan found no runtime fleet/control-plane implementation references

8. Verified dashboard/device/report/hardening fixes
   - Dashboard metrics use explicit labels and captions
   - UI smoke verifies Add Device, Harden Ready Script, and Harden Selected Script actions
   - Controller tests verify adding and switching local devices
   - Controller tests verify harden execution is blocked unless `HARDSECNET_ALLOW_SCRIPT_EXECUTION=1`
   - Controller tests verify run reports include every benchmark item in the selected device OS scope
   - Runtime verification on the real workspace generated a report with 1,951 findings and no missing benchmark IDs in HTML
   - Runtime PDF verification passed with a readable, unencrypted, multi-page report PDF

9. Ran whole-app PySide workflow verification in offscreen mode
   - Launched the real `MainWindow` through `build_window(...)`
   - Captured screenshots for Dashboard, Hardening, Reports, and Benchmarks
   - Added a Linux local device through the Hardening page controls
   - Ran the selected profile through the Hardening page
   - Verified generated findings matched all benchmark controls for the selected device OS
   - Verified report HTML contained every expected benchmark ID and PDF artifact existed
   - Exercised Benchmark dry-run and Harden Selected Script actions through page methods
   - Verified harden execution records a blocked evidence artifact unless `HARDSECNET_ALLOW_SCRIPT_EXECUTION=1`
   - Final app workflow result: `APP_E2E_OK`
   - Final screenshot directory: `C:\Users\tusha\AppData\Local\Temp\hardsecnet_app_e2e_fyp_l6io\hardsecnet-pyside\runtime\verification_screenshots`

10. Ran alternate UI style verification
   - Replaced the dark-only shell with a light command-center style: dark navigation rail, light workspace, white cards, pale tables, and stronger action buttons
   - Verified dashboard metrics no longer overlap the device panel
   - Verified Hardening, Reports, and Benchmarks pages render with readable text and stable controls
   - UI smoke now asserts the active light style is loaded
   - Final style workflow result: `STYLE_E2E_OK`
   - Final style screenshot directory: `C:\Users\tusha\AppData\Local\Temp\hardsecnet_style_final_nwvrlydz\hardsecnet-pyside\runtime\style_screenshots`

11. Ran dashboard posture cleanup verification
   - Replaced dashboard AI-facing metrics with system-admin posture metrics
   - Verified cards show compliance score, open findings, ready actions, last run, drift changes, and reports ready
   - Removed AI wording from dashboard subtitle, current-device panel, and status bar
   - Verified populated dashboard after a local profile run
   - Final dashboard workflow result: `DASHBOARD_CLEAN_OK`
   - Final dashboard screenshot directory: `C:\Users\tusha\AppData\Local\Temp\hardsecnet_dashboard_clean_3vjs78a1\hardsecnet-pyside\runtime\dashboard_clean_screenshots`

12. Ran demo UI simplification verification
   - Removed the Network tab from the demo navigation
   - Added Dashboard profile selection before running local profile audit
   - Simplified Hardening into a Run Center without add-device controls
   - Reworked Benchmarks into Profile Builder with save-selected-controls workflow
   - Added visible Ollama connection/model status to AI Advisor
   - Changed AI Advisor from internal agent-task rows to finding-level risk/remediation explanations
   - Added report detail output and Open HTML/Open PDF actions
   - Final demo workflow result: `FINAL_DEMO_UI_OK`
   - Final demo screenshot directory: `C:\Users\tusha\AppData\Local\Temp\hardsecnet_final_demo_ui_tzkp2265\hardsecnet-pyside\runtime\final_demo_ui_screenshots`

## Observed Results

- App window builds successfully with 7 navigation sections and Dashboard first
- Dashboard status message renders correctly
- JSON, HTML, and PDF report paths are produced and exist on disk
- Runtime artifact directories are created
- Benchmark import, report export payload, and seeded profile access work under test
- Script readiness classification and guarded dry-run artifacts work under test
- Curated ready script candidates are generated for built-in local benchmark controls
- AI settings and deterministic fallback behavior work under test for optional Ollama mode
- UI smoke verifies final "Run Local Baseline" wording
- UI smoke verifies Add Device and harden controls are present
- Reports now include all benchmark findings for the current device OS instead of only profile-listed benchmark IDs
- Real workspace runtime report check passed with 1,951 findings and `missing_in_html=0`
- Report PDF pagination verified; the checked PDF had 455 pages and was readable/unencrypted
- Whole-app PySide workflow passed with add-device, profile run, report generation, dry-run, and harden-gate coverage
- Visual screenshot review verified readable app fonts and consistent light command-center table/header/scrollbar rendering
- Alternate UI style verification passed for Dashboard, Hardening, Reports, and Benchmarks
- Dashboard now reads as an operator posture view rather than an AI summary view
- Demo UI now follows a clearer sequence: build/select profile, run audit, review findings, inspect AI explanations, open report artifacts
- Fresh runtime verification passed with 2 benchmark documents, 4 built-in controls, 3 ready scripts, a dry-run artifact, and generated report artifacts
- Blackbook recreation output verified: PDF, DOCX, and Markdown exist; PDF is readable, unencrypted, and 45 pages
- Source scan found no remote/fleet implementation references in active `src` or `tests` Python files
- Existing runtime SQLite state had stale remote/fleet tables dropped
- Dashboard smoke verified first-page metrics and local benchmark-control count

## Known Limits

- Hardening execution remains guarded; dry-run artifacts are default, and live PowerShell/Bash execution requires `HARDSECNET_ALLOW_SCRIPT_EXECUTION=1`
- Live hardening was not executed against the host machine during validation; the app-level check verified the gated command path and blocked evidence artifact.
- Benchmark control extraction is heuristic for imported text/PDF content
- Live Ollama calls are wired behind `HARDSECNET_OLLAMA_LIVE=1`; deterministic fallback remains the default
- Remote control plane, device agents, fleet dashboard, campaigns, and multi-device control were removed from project scope
- Imported CIS PDF-derived scripts can still be review-required; the built-in curated examples prove the ready-script path.

## BMAD Final Checkpoint

- Role: `tester/reviewer`
- Phase: `validation`
- Workflow: `plan-code-review`
- Artifact updated: `docs/validation.md`
- Blockers: no hydrated local `_bmad` runtime config; validation performed directly against repo state and working code
- Decisions:
  - accept the implementation as a verified v1 scaffold
  - keep remaining gaps explicit rather than overstating completeness
- Handoff target: `complete`
- Completion state: `done`

## Windows CIS Script/Profile Verification - 2026-04-23

- Verified source PDF export: `doc-0bec44c02877`, CIS Microsoft Windows 11 Stand-alone Benchmark v4.0.0.
- Verified extracted Windows PDF controls: `477`.
- Verified exported Windows PowerShell scripts: `477`.
- Ran PowerShell parser validation over all 477 exported `.ps1` files: `ParseErrorCount=0`.
- Fixed two malformed generated placeholder scripts by converting extracted remediation prose into comments:
  - `18.6.19.2.1.ps1`
  - `18.9.26.2.ps1`
- Runtime readiness for the 477 PDF-derived scripts: `477 review_required`, `0 missing`.
- Added benchmark-based Windows profiles:
  - Full Benchmark: `477` controls
  - Account Policies: `11` controls
  - Local Policies: `98` controls
  - Firewall: `16` controls
  - Audit Policy: `27` controls
  - Administrative Templates: `325` controls
- Added guarded deharden/rollback command path using `-Rollback` for PowerShell scripts.
- Added tests for benchmark profile coverage and rollback gating.
- Validation commands:
  - `python -m pytest -q tests`: `18 passed`
  - `python -m compileall src tests`: passed

Known limit: the 477 Windows PDF scripts are syntactically valid and loadable as review-required script candidates. They are not all safe-live-ready remediation scripts. Live hardening/dehardening remains approval-gated and requires `HARDSECNET_ALLOW_SCRIPT_EXECUTION=1`.

## Demo Readiness Cleanup - 2026-04-23

- Cleaned the visible Windows profile list by hiding legacy duplicate imported-baseline profiles and old sample profiles from demo-facing profile selectors.
- Final visible Windows profiles:
  - `Audit Only`
  - `CIS Windows 11 Account Policies`
  - `CIS Windows 11 Administrative Templates`
  - `CIS Windows 11 Audit Policy`
  - `CIS Windows 11 Firewall`
  - `CIS Windows 11 Full Benchmark`
  - `CIS Windows 11 Local Policies`
- Scoped built-in `cis_windows_11_*` profile runs to verified document `doc-0bec44c02877` so old duplicate imports cannot inflate report counts.
- Generated a fresh demo report from `CIS Windows 11 Full Benchmark`:
  - Run: `run-467a69d85c3f`
  - Findings: `477`
  - Scope: `profile_selected_controls`
  - JSON: `E:\T\hardsecnet\hardsecnet-pyside\runtime\reports\report-fd451058cad5.json`
  - HTML: `E:\T\hardsecnet\hardsecnet-pyside\runtime\reports\report-fd451058cad5.html`
  - PDF: `E:\T\hardsecnet\hardsecnet-pyside\runtime\reports\report-fd451058cad5.pdf`
- Validation command: `python -m pytest -q tests`: `19 passed`.

## Ubuntu CIS Demo Readiness Cleanup - 2026-04-23

- Verified source PDF export: `doc-d0e7eed31013`, CIS Ubuntu Linux 24.04 LTS Benchmark v1.0.0.
- Verified extracted Ubuntu controls: `312`.
- Verified generated Ubuntu shell script candidates: `312`.
- Fixed script readiness resolution so Ubuntu controls infer `benchmark_id.sh` from the document `generated_script_dir` when item-level `script_path` is empty.
- Runtime readiness for the 312 Ubuntu PDF-derived scripts: `312 review_required`, `0 missing`.
- Added benchmark-based Ubuntu profiles:
  - Full Benchmark: `312` controls
  - Initial Setup: `66` controls
  - Services: `43` controls
  - Network: `47` controls
  - Access And Authentication: `71` controls
  - Logging And Audit: `62` controls
  - System Maintenance: `23` controls
- Cleaned visible Linux profile list by hiding duplicate imported-baseline profiles and the old `Default Ubuntu Desktop` sample profile.
- Scoped built-in `cis_ubuntu_2404_*` profile runs to verified document `doc-d0e7eed31013`.
- Made PDF report generation more defensive by sanitizing PDF text and truncating the PDF finding list for readability; JSON and HTML retain the full finding set.
- Generated a fresh demo report from `CIS Ubuntu 24.04 Full Benchmark`:
  - Run: `run-d8ac712b4122`
  - Findings: `312`
  - Scope: `profile_selected_controls`
  - JSON: `E:\T\hardsecnet\hardsecnet-pyside\runtime\reports\report-866b3d7a59b6.json`
  - HTML: `E:\T\hardsecnet\hardsecnet-pyside\runtime\reports\report-866b3d7a59b6.html`
  - PDF: `E:\T\hardsecnet\hardsecnet-pyside\runtime\reports\report-866b3d7a59b6.pdf`
- Validation command: `python -m pytest -q tests`: `21 passed`.

Known limit: the 312 Ubuntu PDF scripts are loadable review-required candidates. Live hardening is still limited to curated ready scripts and remains gated by `HARDSECNET_ALLOW_SCRIPT_EXECUTION=1`.

## Supervisor UI Polish Pass - 2026-04-23

- Reviewed the PySide desktop UI from a demo-supervisor perspective.
- Polished the app shell with:
  - clearer window title
  - stronger dark navigation rail
  - cleaner selected-navigation treatment
  - distinct primary and secondary sidebar actions
  - refined page headings, cards, tables, inputs, scrollbars, and focus states
- Reworked dashboard metric cards into one horizontal row to prevent clipping and overlap in the 1360x900 demo viewport.
- Improved table readability with taller headers, stable row height, elided long text, and better section spacing.
- Improved Profile Builder control usability by widening the profile-name field.
- Generated screenshot artifacts for visual inspection:
  - `runtime/ui_supervisor_screenshots/01-dashboard.png`
  - `runtime/ui_supervisor_screenshots/02-hardening.png`
  - `runtime/ui_supervisor_screenshots/03-ai-advisor.png`
  - `runtime/ui_supervisor_screenshots/04-reports.png`
  - `runtime/ui_supervisor_screenshots/05-profile-builder.png`
  - `runtime/ui_supervisor_screenshots/06-settings.png`
- Validation command: `python -m pytest -q tests`: `21 passed`.

## Live Before/After Hardening Demo Path - 2026-04-23

- Added concrete Windows before/after demo paths for multiple curated ready scripts.
- The script now checks and changes the current-user secure screen saver lock setting:
  - Registry: `HKCU:\Control Panel\Desktop\ScreenSaverIsSecure`
  - OFF state: `ScreenSaverIsSecure=0`
  - ON state: `ScreenSaverIsSecure=1`
  - Supporting values: `ScreenSaveActive=1`, `ScreenSaveTimeOut=60`
- Added `Check Ready Setting` in Run Center so the app can display the current setting state before and after hardening.
- Demo flow verified:
  - Select `Demo Windows Workstation Hardening`
  - Deharden Ready Script -> three settings report `Status: OFF`
  - Check Ready Setting -> confirms current setting states
  - Harden Ready Script -> three settings report `Status: ON`
  - Check Ready Setting -> confirms current setting states
- Benefit shown in app output: requires the user's password after inactivity, reducing unattended-session access risk.
- Logical demo profiles now visible:
  - `Demo Windows Workstation Hardening`: 3 ready settings
  - `Demo Windows Inactivity Lock`: 2 ready settings
  - `Demo Windows Session Security`: 1 ready setting
- Validation command: `python -m pytest -q tests`: `23 passed`.

## Broader Workstation Hardening Profile - 2026-04-23

- Expanded `Windows Workstation Hardening` from a 3-setting demo path into a credible workstation baseline scope.
- Runtime workspace inventory:
  - Profile controls: `131`
  - Ready reversible settings in profile: `6`
  - Account-policy controls included: `11`
  - Firewall controls included: `16`
  - Audit/admin-template controls included through selected CIS sections.
- Ready reversible settings now covered:
  - Secure screen saver lock
  - Screen saver activation
  - Inactivity timeout
  - Show file extensions
  - Disable AutoRun for removable media
  - Preserve downloaded-file zone information
- Password policy and firewall policy are included in the profile/report scope as admin-review controls. They are not silently applied as user-level registry edits because real local password and Defender Firewall policy changes require administrative policy execution.
- Runtime status check completed for all 6 ready settings with no live-execution gate required.
- Run Center buttons were renamed to `Check Ready Settings`, `Harden Ready Settings`, and `Deharden Ready Settings`.
- Validation command: `python -m pytest -q tests`: `23 passed`.

## Windows CIS Review Batch - Section 2 - 2026-04-23

- Reviewed Windows CIS section `2.*` with a conservative conversion pass.
- Section inventory:
  - Total section `2.*` controls: `98`
  - User-rights assignment controls in `2.2.*`: left non-ready in this batch
  - Security-options controls in `2.3.*`: reviewed for explicit registry-backed remediation
- Converted `38` registry-backed `2.3.*` controls from generated stubs into executable PowerShell scripts with:
  - `-Status`
  - `-Apply`
  - `-Rollback`
  - human-readable output
- Left `60` controls as `review_required` because they still require deeper manual/admin validation, primarily:
  - `2.2.*` user-rights assignment policy edits
  - configurable text/value controls
  - ambiguous multi-choice controls where the benchmark text allows multiple compliant settings
- Runtime readiness after the batch:
  - `38 ready`
  - `60 review_required`
- Sample live status checks completed successfully for:
  - `2.3.17.6` UAC Admin Approval Mode
  - `2.3.10.2` Restrict anonymous enumeration of SAM accounts
- Added bootstrap synchronization so benchmark item `script_state` reflects reviewed readiness from actual script content instead of remaining permanently `candidate`.
- Validation command: `python -m pytest -q tests`: `23 passed`.

## Windows CIS Review Batch - Section 17 - 2026-04-23

- Reviewed Windows CIS section `17.*` advanced audit policy controls.
- Section inventory:
  - Total section `17.*` controls: `27`
  - Controls converted in this batch: `27`
- Converted all `27` generated stubs into executable `auditpol`-based PowerShell scripts with:
  - `-Status`
  - `-Apply`
  - `-Rollback`
  - human-readable output for current audit posture
- Runtime readiness after the batch:
  - `27 ready`
  - `0 review_required`
- Validation:
  - PowerShell parser over section `17.*` scripts: `SECTION17_PARSE_OK`
- Live `-Status` execution requires elevated privileges on this machine; non-elevated checks failed with Windows privilege error `0x00000522`
- App readiness classification still correctly marks the scripts `ready` because the reviewed script logic is present and parse-valid
- `python -m pytest -q tests`: `23 passed`

## Windows CIS Review Batch - Section 9 - 2026-04-23

- Reviewed Windows CIS section `9.*` firewall profile controls.
- Section inventory:
  - Total section `9.*` controls: `16`
  - Controls converted in this batch: `16`
- Converted all `16` generated stubs into executable registry-backed firewall policy scripts with:
  - `-Status`
  - `-Apply`
  - `-Rollback`
  - human-readable output
- Runtime readiness after the batch:
  - `16 ready`
  - `0 review_required`
- Validation:
- PowerShell parser over section `9.*` scripts: `SECTION9_PARSE_OK`
- Live `-Status` checks succeeded for `9.3.1` and `9.3.5`
- `python -m pytest -q tests`: `23 passed`

## Windows CIS Review Batch - Section 18 - 2026-04-23

- Reviewed Windows CIS section `18.*` administrative-template controls with a selective exact-value conversion pass.
- Section inventory:
  - Total section `18.*` controls: `312`
  - Controls converted in this batch: `217`
  - Controls intentionally left under review: `95`
- Converted `217` exact-value registry-backed stubs into executable PowerShell scripts with:
  - `-Status`
  - `-Apply`
  - `-Rollback`
  - human-readable output
- Left `95` controls as `review_required` because they still require deeper manual validation, including:
  - wrapped benchmark text that broke exact key/value reconstruction
  - blank-value or not-configured policy semantics
  - ambiguous/range/multi-choice expectations
- Runtime readiness after the batch:
  - `217 ready`
  - `95 review_required`
- Validation:
- PowerShell parser over section `18.*` scripts: `SECTION18_PARSE_OK`
- Sample live `-Status` check succeeded for `18.1.1.1`
- `python -m pytest -q tests`: `23 passed`

## Windows CIS Review Batch - Section 19 - 2026-04-23

- Reviewed Windows CIS section `19.*` current-user policy controls.
- Section inventory:
  - Total section `19.*` controls: `13`
  - Controls converted in this batch: `13`
- Converted all `13` current-user `HKU\[USER SID]` stubs into executable `HKCU` PowerShell scripts for the active local user with:
  - `-Status`
  - `-Apply`
  - `-Rollback`
  - human-readable output
- Runtime readiness after the batch:
  - `13 ready`
  - `0 review_required`
- Validation:
  - PowerShell parser over section `19.*` scripts: `SECTION19_PARSE_OK`
  - Live `-Status` check succeeded for `19.7.40.1`
  - `python -m pytest -q tests`: `23 passed`

## Hardening Page Profile Refresh Fix - 2026-04-23

- Fixed the Run Center/Hardening profile selector so switching profiles updates the page immediately.
- Changes:
  - wired the profile combo box change event to refresh profile-scoped data
  - preserved the selected profile across page refreshes
  - refreshed the "What This Profile Runs" table when the selected profile changes
  - updated the details pane to show selected profile summary when no run is selected
- Validation:
  - `python -m pytest -q tests\\test_ui_smoke.py`: `2 passed`
  - `python -m pytest -q tests`: `24 passed`

## Profile Builder Selection Workflow Fix - 2026-04-23

- Fixed the Profile Builder so controls can be explicitly added to and removed from a profile selection before saving.
- Changes:
  - added `Add Selected Controls`, `Remove Highlighted`, and `Clear Profile Selection` actions
  - added a dedicated `Controls In Profile` table so the selected benchmark set is visible
  - changed profile save behavior to require the explicit selected-controls list instead of implicit table selection/all-controls fallback
  - updated details messaging to show current selection count
- Validation:
  - `python -m pytest -q tests\\test_ui_smoke.py`: `3 passed`
  - `python -m pytest -q tests`: `25 passed`

## Demo Profile Addition - Password Expiry And Public Firewall - 2026-04-23

- Added a built-in Windows demo profile combining one password-expiry control with the public firewall lockdown controls.
- Profile:
  - `demo_windows_password_expiry_public_firewall`
  - display name: `Password Expiry And Public Firewall`
- Scope:
  - password expiry control `1.1.2`
  - public firewall controls `9.3.1` through `9.3.9`
  - audit signal `17.7.4`
- Validation:
  - `python -m pytest -q tests\\test_controller.py`: `15 passed`
  - `python -m pytest -q tests`: `26 passed`

## Script Execution Reliability Pass - 2026-04-23

- Fixed the Windows password-age script `1.1.2` so it uses a working `net accounts` implementation for status/apply/rollback.
- Fixed the reviewed Windows `1.*` scripts so `param(...)` appears before executable statements in PowerShell script mode.
- Fixed duplicate-document leakage so OS-level benchmark item/readiness queries use the canonical reviewed benchmark document instead of hidden stale generated duplicates.
- Added execution preflight for admin-required scripts:
  - scripts using `auditpol`, `secedit`, or `net accounts` now return a clean blocked message in non-elevated sessions
  - raw privilege stack traces are no longer surfaced as the primary UX for these checks
- Validation:
  - direct `1.1.2 -Status` check succeeded
  - `1.1.2` readiness resolves to `ready`
  - `17.7.4` readiness resolves to `ready`
  - non-elevated status checks for admin-required controls return a clean `blocked` state with an elevated-session message
  - `python -m pytest -q tests`: `27 passed`

## Hardening Output Clarity Pass - 2026-04-23

- Updated Run Center execution formatting so admin-only controls and noncompliant status checks read clearly during demos.
- Changes:
  - `blocked` + elevated-session prerequisite now displays as `Admin Required`
  - raw admin-prerequisite error text is replaced with a concise operator instruction
  - status-check output lines showing `Status: OFF` now display as `Status: Not Hardened Yet`
- Validation:
  - `python -m pytest -q tests\\test_ui_smoke.py`: `4 passed`
  - `python -m pytest -q tests`: `28 passed`

## Demo Profile Addition - Private And Public Firewall On - 2026-04-23

- Added a minimal built-in Windows demo profile containing only the two CIS controls that ensure the private and public firewall profiles are enabled.
- Profile:
  - `demo_windows_private_public_firewall_on`
  - display name: `Private And Public Firewall On`
- Scope:
  - `9.2.1` private firewall state on
  - `9.3.1` public firewall state on
- Validation:
  - `python -m pytest -q tests\\test_controller.py`: `17 passed`
  - `python -m pytest -q tests`: `29 passed`
