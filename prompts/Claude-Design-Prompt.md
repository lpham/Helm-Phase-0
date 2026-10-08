# Claude Design Prompt — Helm Phase 0 Pilot UI

Copy everything after the `---` separator into Claude (a design or prototyping session). Attach `outputs/Helm-Phase-0-Solution-2026-10-09.md` as the source of truth for scope, states and rules. Replace the bracketed **Inputs to confirm** if Business has decided them; otherwise leave the defaults.

**Inputs to confirm before running:**

- Brand: [no brand guide supplied → restrained fintech style, neutral palette, one accent colour; product name "Helm"].
- UI language: [English for the Pilot; layouts must tolerate Vietnamese text length].
- Network and asset: [USDC on Arbitrum One] (decision D1).
- Redemption service target shown to Members: [e.g. "usually within 5 business days, subject to liquidity"] (decision D4).
- Vault name, strategy description, fees and risk text: [placeholders — Business and counsel provide the final copy].

---

You are a senior product designer for a crypto fintech product used by a referral (MLM) community. Design the **Phase 0 Pilot** of **Helm**: a mobile-first responsive web app for Members and Builders, plus an internal admin console. The attached solution document is the source of truth for scope, data states and rules; do not add features outside it.

## Product in one paragraph

Members join through a Sponsor's invite link, log in with email or social login and automatically get a self-custodial wallet (Privy embedded wallet; only the Member can move funds). They fund the wallet by sending USDC on one network, then deposit into one approved vault (Enzyme Onyx). Deposits are requests processed at the vault's next valuation; Redemptions are queued and paid when liquidity is available. Builders (Members enrolled to refer others) share a referral link, see their direct team, and receive a simple three-level referral Commission paid in USDC to their Helm wallet in Finance-approved batches. Members can play an existing game (Tap Prediction) for Points with no cash value, and chat with support in the app.

## Build versus reuse (important)

PillarsHub is a specialist MLM platform with its own admin Portal and Builder back office. **Do not redesign what PillarsHub already provides.** Helm designs only the Member experience, the money flows (wallet, vault, payout execution) and the few admin screens PillarsHub cannot cover. Where a Builder or admin needs deep MLM detail, design a clear hand-off instead:

- **Builders:** Helm shows the essentials (referral link, direct team counts, earnings summary and payouts to wallet). A secondary action **"Open full back office"** opens PillarsHub's back office through single sign-on (Helm's backend mints a PillarsHub user token; PillarsHub opens `app.pillarshub.com?token=…`). Design the hand-off moment: explanation, new tab, returning to Helm.
- **Admins:** genealogy browsing, Sponsor and placement edits, plan configuration, bonus review, period close and bonus release are done in the **PillarsHub Portal**. Helm admin links to it (deep link by Member ID) and shows only Helm-owned data.
- If time is short, any Builder screen beyond the essentials above can be replaced by the back-office link without blocking launch.

## Users

- **Member (Customer):** non-technical, mostly on a phone, may be new to crypto.
- **Builder:** a Member who refers others; wants their link, team and earnings at a glance.
- **Preregistered person:** signed up before launch; keeps their referral but cannot deposit or earn yet.
- **Admin roles:** operations, Finance approver, support agent (read-only context), each with separate permissions.

## Screens to design — Member and Builder app (mobile 390 px first, then desktop 1440 px)

1. **Invite landing** — "Invited by @sponsor"; what Helm is in one line; Join button. Handle: invalid, expired or self-referral links.
2. **Sign up / log in** — Privy login (email, Google, Apple, passkey); country of residence; accept Member terms and privacy notice (versioned); restricted-country block screen.
3. **Preregistration home** — confirmation of referral, what happens next, launch status; no money actions.
4. **Home** — wallet balance; vault position with "value as of [date]"; pending items (funding, deposit, Redemption); Points; next-step card.
5. **Wallet / add funds** — one network and asset only, address and QR, prominent wrong-network warning, funding states (submitted, confirming N of M, credited, failed/unsupported); history; second login method prompt ("add a backup login so you never lose access").
6. **Vault detail** — strategy description, fees, risks, how deposits and Redemptions work, valuation date, no projected returns; accept vault terms (versioned) before first deposit; blocked state if not eligible.
7. **Deposit flow** — amount → review (fees, processing at next valuation) → sign approval → sign deposit request → "Requested — processing at next valuation" → executed with shares. Show cancel option only after the minimum time. Errors: reverted transaction, insufficient balance, not eligible.
8. **Position and activity** — shares, value with valuation timestamp, deposit/Redemption history with transaction links.
9. **Redemption flow** — choose shares → review (no guaranteed time; service target) → sign → stages: requested, awaiting liquidity, paid to wallet, cancelled.
10. **Become a Builder** — explain the role, accept Builder terms; Customer-only members are never pushed into it.
11. **Builder: referral and team** (essentials) — referral link and QR with share actions; direct team counts and a short list of recent joiners with "updated [time]"; **never** show anyone's balances, positions or support cases. Secondary action: "Open full back office" (PillarsHub SSO) for the full tree and reports.
12. **Builder: earnings** (essentials) — Commission summary by state (pending, held with reason, payable, paid); payouts received in the Helm wallet with USDC amount and transaction link; "Report a problem with this earning" (carries the earning ID). Detailed statements and bonus breakdowns: link to the PillarsHub back office.
13. **Points and game** — Points balance and history, rules and daily limits, "Points have no cash value"; entry to Tap Prediction.
14. **Support** — in-app chat (Chatwoot widget) and FAQ; banner: "Helm will never ask for your seed phrase or private key."
15. **Profile and security** — login methods, MFA, key export with strong warnings, agreements and versions, notification settings, log out.
16. **Notifications** — funding credited, deposit executed, Redemption paid, Commission paid, action required.

## Screens to design — Helm admin console (desktop, minimal)

Only Helm-owned data. Each Member and batch screen has an **"Open in PillarsHub Portal"** link for MLM detail.

1. Member search and detail: identity, Customer/Builder state, provider IDs, wallet, screening and allowlist status, agreements, audit trail; link to the Member in PillarsHub.
2. Referral and sync exceptions: referrals not yet accepted by PillarsHub, sync failures, reconciliation differences between Helm and the PillarsHub tree (fix happens in PillarsHub; Helm shows and tracks the case).
3. Alpha import runs: counts, edge reconciliation, exceptions, approve or roll back.
4. Funding and vault monitor: pending deposit and Redemption requests, stale items beyond target, valuation freshness.
5. Payout execution: batch received from PillarsHub (released there by Finance), holds with reasons, Finance approval of the treasury transfers, transaction status (proposed, signed, confirmed, failed), per-payment Success/Failure/Pending reported back.
6. Screening cases with owner, status and resolution.
7. Support agent context view (read-only): identity, status, earnings and payout state, case history; no action buttons for funds or genealogy.

**Not designed in Helm (use PillarsHub Portal):** genealogy tree browsing, Sponsor and placement changes, compensation plan, bonus review, period close, bonus release, MLM reports.

## Content and compliance rules (must follow)

- Never use "staking", "APY", "returns", "earn interest", "guaranteed", "passive income" or earnings claims. Say "vault", "deposit", "position", "value as of".
- Always distinguish **wallet funding** (money in your wallet), **vault deposit** (shares in the vault) and **Commission** (referral earnings); never add them into one "total earnings" number.
- Show values with their timestamp and source; pending items look clearly different from confirmed ones.
- Points are never shown with a currency symbol and never next to money totals.
- Risk, fee and terms text are placeholders marked for counsel review.
- No private keys, seed phrases or secrets anywhere in UI or support flows.

## Design requirements

- Mobile-first responsive web (no native app). WCAG 2.2 AA contrast, 44 px touch targets, readable at 200% zoom.
- Every screen includes loading, empty, pending, error and blocked states where relevant.
- Clear status language and a consistent status chip system (submitted, pending, processing, held, confirmed, paid, failed, cancelled).
- Copy is short, plain and calm; numbers right-aligned with currency and network shown.
- Tolerate 30% longer strings (Vietnamese) without breaking layouts.

## Deliverables

1. A small design system: colour and type tokens, spacing, status chips, cards, list rows, buttons, inputs, banners, stepper for multi-step flows, transaction row with link.
2. The screens above at mobile and desktop sizes, with key states.
3. Clickable prototype flows: (a) invite → signup → preregistration; (b) add funds → vault deposit → executed position; (c) Redemption to paid; (d) Builder earnings → payout paid → dispute, including the "Open full back office" hand-off; (e) admin payout execution after release in PillarsHub.
4. A short list of open content questions for Business and counsel.

Do not invent features, numbers or provider capabilities beyond the attached document; use clearly labelled placeholders instead.
