# P10 — SAST & Secrets summary

## Semgrep
- Profile `p/ci` + custom rule pack `security/semgrep/rules.yml`.
- Findings: 1 warning (`studyplanner-hardcoded-admin-password`), 1 note (`studyplanner-inmemory-token-store`).
- Action: default admin bootstrap + token storage will be moved into a management command backed by the DB/secrets store (tracked in backlog task SEC-17).

## Gitleaks
- Config: `security/.gitleaks.toml` (focused rules + allowlist for dummy credentials in tests).
- Findings: no real secrets detected in working tree.
- Action: keep the allowlist narrow and rotate secrets via env vars only.
