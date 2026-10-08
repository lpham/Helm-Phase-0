# 04 — Chatwoot support, funding path (direct vs Paymenture) and compliance applicability

- **Project:** Helm Phase 0 (Cyclone for AlphaWave)
- **Verification date:** 2026-10-08 (all "Verified capability" rows below were read on this date unless the row cites an earlier discovery note)
- **Scope:** Part A Chatwoot minimum integration; Part B Wallet Funding vs integrated purchase via Paymenture; Part C compliance applicability and responsibility matrix on the confirmed stack.
- **Not legal advice.** Jurisdiction, operating entity and custody model are unconfirmed. This note maps where controls *would* sit and who would own them; applicability is for qualified counsel.

**Evidence labels**
- **Verified capability** — read on the provider's own page (URL given), 2026-10-08. Discovery-note findings reused with their original URL and the discovery research date (2026-10-06).
- **Provider correspondence** — from `inputs/Business.md`; not independently verified.
- **Recommended design** — Cyclone's proposal.
- **Assumption/TBD** — not evidenced; needs confirmation.

Glossary terms used: Member, Sponsor, Sponsor Edge, Genealogy, Referral Request, Wallet Funding, Vault Deposit, Redemption, Vault Position, Commission, Points, Yield Product, Helm Web App, Cyclone. The discovery notes used older terms ("Deposit", "Sponsor Tree"); they are mapped here to Wallet Funding / Vault Deposit and Genealogy.

---

## 1. Summary

1. **Chatwoot can deliver the Phase 0 support requirement with configuration plus a small backend piece.** The website live-chat widget is embedded with a script; the Helm backend computes an HMAC-SHA256 of the Member's identifier with the inbox's identity-validation token, and the widget passes it as `identifier_hash` via `window.$chatwoot.setUser`. Chatwoot can be set to "Require identity validation for all conversations", which rejects requests without a valid token. Use the stable **Helm member ID** as the identifier and send only non-sensitive custom attributes. (Verified capability, §A.2.)
2. **Recommended Phase 0 deployment: Chatwoot Cloud, Startups or Business plan** (USD 19 or 39 per agent per month as listed), one website inbox, administrator/agent roles only. SSO/SAML and audit logs require Enterprise (USD 99 per agent per month, cloud or self-hosted). Chatwoot Cloud runs on AWS in the United States; if data-residency rules require otherwise, self-hosting is the alternative and adds infrastructure and operations work. (Verified capability, §A.5.) Platform APIs are self-hosted only and are not needed for Phase 0.
3. **Paymenture is not needed for the MVP, and cannot be recommended yet.** Its public pages describe a broad financial-infrastructure API (payouts, cards, digital assets, compliance) offered by Paymenture, LLC (Utah) through unnamed third-party "Service Providers". Supported assets, networks, jurisdictions, fees and an on-ramp/purchase flow are **not published**; the developer docs site is JavaScript-rendered and could not be read. Its terms do not name MLM, but prohibit "pyramid schemes; Ponzi schemes; deceptive investment schemes" and "unlawful digital asset activity", and the underlying sponsor banks/VASPs are unnamed, so business-model acceptance needs written confirmation. Direct crypto Wallet Funding remains the fastest path. (§B.)
4. **No confirmed provider supplies KYC, sanctions screening or transaction monitoring that Helm can rely on for this business model.** Privy's KYC runs through Bridge, whose terms prohibit MLM (discovery notes 02/06). Chatwoot and PillarsHub have no KYC capability evidenced. Onyx depositor allowlisting is a dependency for the Onyx analyst. If counsel concludes controls apply, a dedicated screening/IDV vendor integrated by Cyclone is needed; that is a Business decision, not a stack change. **Minimum before real funds regardless of outcome:** sanctions screening of the Member's funding source and Redemption destination addresses, geographic eligibility attestation, Member terms and privacy notice, and a counsel decision on KYC tier. (§C.)

---

## Part A — Chatwoot

### A.1 Minimum embedded support flow (Recommended design)

```mermaid
sequenceDiagram
  participant M as Member (Helm Web App)
  participant B as Helm backend
  participant W as Chatwoot widget
  participant C as Chatwoot (Cloud)
  participant A as Support agent
  M->>B: Authenticated session (Privy)
  B-->>M: helm_member_id + identifier_hash (HMAC-SHA256, inbox token)
  M->>W: setUser(helm_member_id, {name, email, identifier_hash})
  M->>W: setCustomAttributes({member_status, funding_status, ...})
  W->>C: Contact verified; conversation created
  C->>A: Conversation with verified contact
  C-->>B: Webhook conversation_created / message_created (signed)
  B->>B: Verify X-Chatwoot-Signature, log, link to member record
  A->>C: Reply / resolve (no fund-moving action)
  M->>W: Logout -> $chatwoot.reset()
```

1. Create one **Website** inbox in Chatwoot; enable identity validation and "Require identity validation for all conversations".
2. Embed the widget script in the Helm Web App for authenticated pages only (support for unauthenticated visitors can use a public form or be deferred).
3. Helm backend endpoint returns `identifier_hash` for the logged-in Member; the HMAC token stays server-side.
4. On login call `setUser`; on logout call `reset()` so the next user on the device does not inherit the session.
5. Helm backend subscribes to Chatwoot webhooks and verifies the signature; Phase 0 uses them only for logging and linking, not for workflow.
6. Agents see verified contact plus a small set of custom attributes; for deeper lookups agents use the Helm admin view (read-only), not Chatwoot.
7. Support actions never move funds, change Sponsor Edges or award Points. Changes go through Helm admin with its own permissions and audit trail.

### A.2 Identity mapping and impersonation prevention

| Item | Finding | Label |
|---|---|---|
| Widget SDK `setUser` | `window.$chatwoot.setUser("<unique-identifier>", { email, name, avatar_url, phone_number, identifier_hash, description, country_code, city, company_name, social_profiles })` | Verified capability — [SDK user info](https://www.chatwoot.com/hc/user-guide/articles/1677587234-how-to-send-additional-user-information-to-chatwoot-using-sdk), 2026-10-08 |
| Custom attributes, labels, reset | `setCustomAttributes({...})`, `deleteCustomAttribute(key)`, `setLabel`/`removeLabel`, `setLocale`, `reset()` (logout); events `chatwoot:ready`, `chatwoot:on-message`, `chatwoot:error`. Page notes HMAC "will allow chat history to persist across sessions" | Verified capability — same URL |
| HMAC | "Identity validation can be enabled by generating an HMAC." Key is per web widget, copied from "Inboxes -> Settings -> Configuration -> Identity Validation"; message is the `<identifier>`; examples use `sha256` hex digest, server-side | Verified capability — [Identity validation](https://www.chatwoot.com/hc/user-guide/articles/1677587479-how-to-enable-identity-validation-in-chatwoot), 2026-10-08 |
| Enforcement | With "Require identity validation for all conversations", "visitors must provide a valid identity token before they can start conversations. Requests without valid tokens will be rejected." Without validation, "Someone could type another customer's email address into a public chat form"; agents see an unverified warning | Verified capability — [Contact identity](https://www.chatwoot.com/hc/user-guide/articles/1782283175-understanding-contact-identity-and-identity-validation-in-chatwoot), 2026-10-08 |
| Contact API | `POST /api/v1/accounts/{account_id}/contacts` with `inbox_id` (required), `identifier` ("A unique identifier for the contact in external system"), `custom_attributes` ("requiring valid definitions"), `additional_attributes`, `blocked`. Bearer token (v4.19.0+) or legacy `api_access_token` | Verified capability — [Create contact](https://developers.chatwoot.com/api-reference/contacts/create-contact.md), 2026-10-08 |
| Custom attribute definitions | Account-level definitions managed via API (list/add/update/remove) | Verified capability — [Custom attributes API](https://developers.chatwoot.com/api-reference/custom-attributes/add-a-new-custom-attribute.md), 2026-10-08 |
| Contact merge | Merge Contacts endpoint exists | Verified capability — [Merge contacts](https://developers.chatwoot.com/api-reference/contacts/merge-contacts.md) (listed in docs index), 2026-10-08 |

**Recommended design — identity and data minimisation**
- `identifier` = Helm member ID (stable, opaque). Never the wallet address, Privy user ID or email (emails can change; wallet addresses link the person to on-chain activity).
- Allowed custom attributes (define in Chatwoot first): `helm_member_id`, `member_status` (pending/active/restricted), `funding_status` (none/pending/confirmed), `has_vault_position` (yes/no), `kyc_tier` (only if a tier exists), `support_tier`/locale. Optional: truncated wallet address (first 6/last 4) only if support needs it — Assumption/TBD with Business.
- **Never send:** private keys, seed phrases, Privy auth tokens, API keys, full identity documents, KYC results detail, balances in a form that becomes a financial record. Add a widget pre-message warning: "Helm support will never ask for your seed phrase or private key."
- Helm keeps the mapping `helm_member_id ↔ chatwoot_contact_id` (from webhook payload) in the member record.

### A.3 APIs and webhooks

| API | Purpose / auth | Availability | Phase 0 use | Label |
|---|---|---|---|---|
| Application API | Agent/admin perspective; user `access_token` from Profile Settings | Cloud and self-hosted | Optional: backend creates/updates contacts, reads conversations | Verified capability — [API intro](https://developers.chatwoot.com/api-reference/introduction.md), 2026-10-08 |
| Client API | Custom chat interfaces; `inbox_identifier` + `contact_identifier` | Cloud and self-hosted | Not needed (widget suffices) | Verified capability — same |
| Platform API | Installation-level users/accounts/roles; token from Super Admin "Platform App"; "cannot access accounts or users created via the Chatwoot UI, or by other API keys" | "available only on self-hosted Chatwoot installations" | Not needed | Verified capability — same; [Platform APIs](https://developers.chatwoot.com/contributing-guide/chatwoot-platform-apis.md) |
| Webhooks | Subscriptions: `conversation_created`, `conversation_status_changed`, `conversation_updated`, `message_created`, `message_updated`, `contact_created`, `contact_updated`, `webwidget_triggered`, `conversation_typing_on`, `conversation_typing_off`. Signed: `X-Chatwoot-Timestamp`, `X-Chatwoot-Signature` = `sha256=` HMAC-SHA256 of `{timestamp}.{raw_request_body}` with the webhook secret; `X-Chatwoot-Delivery` when available | Account level | Log + link contacts; dedupe on `X-Chatwoot-Delivery` | Verified capability — [Add a webhook](https://developers.chatwoot.com/api-reference/webhooks/add-a-webhook.md), [Webhooks guide](https://www.chatwoot.com/hc/user-guide/articles/1677693021-how-to-use-webhooks), 2026-10-08 |
| Webhook retries / ordering | Not specified in docs read | — | Do not depend on webhooks for anything critical; reconcile via Application API if needed | Assumption/TBD |
| Audit logs API | "only available in Enterprise editions and requires the audit_logs feature to be enabled" | Enterprise | Post-MVP | Verified capability — [Audit logs API](https://developers.chatwoot.com/api-reference/audit-logs/list-audit-logs-in-account.md), 2026-10-08 |

### A.4 Roles and permissions

| Item | Finding | Label |
|---|---|---|
| Administrator | "Full access. Can change account settings, manage agents, configure inboxes, build automations, view all conversations." | Verified capability — [Adding agents](https://www.chatwoot.com/hc/user-guide/articles/1677482414-adding-agents), 2026-10-08 |
| Agent | "Can handle conversations on inboxes they're a member of, but cannot change account settings or manage other agents." | Verified capability — same |
| Agent API | `role` is `"agent"` or `"administrator"`; response includes `custom_role_id` | Verified capability — [Add agent](https://developers.chatwoot.com/api-reference/agents/add-a-new-agent.md), 2026-10-08 |
| Custom roles | Settings > Custom Roles with permissions: Manage All Conversations; Manage Unassigned & Own Conversations; Manage Participating Conversations; Manage Contacts; Manage Reports; Manage Knowledge Base | Verified capability — [Role-based permissions](https://www.chatwoot.com/hc/user-guide/articles/1741923706-manage-team-access-control-with-flexible-role_based-permissions), 2026-10-08 |
| Custom roles plan | Self-hosted: "Roles & permissions" in Premium Support (USD 19) and Enterprise (USD 99), not Community. Cloud plan availability not stated on the cloud pricing page | Verified (self-hosted) — [Self-hosted plans](https://www.chatwoot.com/pricing/self-hosted-plans); Cloud = Assumption/TBD |
| SSO/SAML | Cloud: Enterprise plan. Self-hosted: Enterprise edition. Once enabled, "users won't be able to access Chatwoot with their password" | Verified capability — [Pricing](https://www.chatwoot.com/pricing), [Self-hosted plans](https://www.chatwoot.com/pricing/self-hosted-plans), [SAML](https://www.chatwoot.com/hc/user-guide/articles/1758635327-setting-up-saml), 2026-10-08 |
| MFA | MFA guide exists (user guide and self-hosted config) | Verified (page exists) — [MFA](https://www.chatwoot.com/hc/user-guide/articles/1758558189-multi_factor-authentication-mfa-in-chatwoot); plan coverage TBD |
| Audit logs | "Audit Logs is an Enterprise feature." Logs sign-ins, role changes, settings, inboxes, webhooks, automation, teams | Verified capability — [Audit logs](https://www.chatwoot.com/hc/user-guide/articles/1692251809-how-to-use-audit-logs), 2026-10-08 |

**Recommended design:** 1–2 administrators (Helm operations lead + Cyclone during setup, removed at handover), all others Agent. Require MFA for all Chatwoot users (Assumption: available on the chosen plan). Restrict the Application API token to a dedicated service user. Revisit custom roles/SSO/audit logs if Business requires them for its control environment.

### A.5 Deployment, data residency and pricing

| Option | Price (as published, per agent per month) | Includes | Label |
|---|---|---|---|
| Cloud Hacker | USD 0; up to 2 agents; 500 conversations/month; live chat only; 30-day retention | — | Verified capability — [Pricing](https://www.chatwoot.com/pricing), 2026-10-08 |
| Cloud Startups | USD 19; all channels; 1-year retention; 300 Captain AI credits | Help center | Verified — same |
| Cloud Business | USD 39; teams, automation rules; 2-year retention; 500 credits | — | Verified — same |
| Cloud Enterprise | USD 99; SSO/SAML, audit logs; 3-year retention; 800 credits | — | Verified — same |
| Self-hosted Community | USD 0 | No roles & permissions, SSO, SLA, Captain AI | Verified — [Self-hosted plans](https://www.chatwoot.com/pricing/self-hosted-plans) |
| Self-hosted Premium Support | USD 19 | Roles & permissions, agent capacity, branding, priority email support; no SSO/SLA | Verified — same |
| Self-hosted Enterprise | USD 99 | Adds SSO/SAML, SLA policies, phone support | Verified — same; enterprise features (whitelabel, SLA, audit logs, agent capacity) per [Enterprise edition](https://developers.chatwoot.com/self-hosted/enterprise-edition.md) |
| Self-hosted infrastructure | Ruby 3.2+, PostgreSQL (only DB), Redis 7+; "4 cores is the recommended minimum" and "4GB RAM" for up to 10,000 conversations/day; Ubuntu 20.04 | Plus hosting, backups, patching, monitoring (cost TBD) | Verified — [Requirements](https://developers.chatwoot.com/self-hosted/deployment/requirements.md) |
| Data residency (Cloud) | "Chatwoot Cloud runs on AWS with servers located in the United States" | GDPR/SOC 2 questions directed to Chatwoot | Verified — [Pricing](https://www.chatwoot.com/pricing) FAQ, 2026-10-08 |
| Annual billing / discounts / taxes | Not stated | — | TBD |
| Captain AI | AI features use credits; extra credits USD 20 per 1,000 | Data-processing implications (conversation content to an AI service) not reviewed | Verified price; data handling TBD |

**Phase 0 cost illustration (Recommended design, not a quote):** 3 agents on Cloud Startups = 3 × USD 19 = USD 57/month; on Business = USD 117/month; Enterprise = USD 297/month. Hacker (free, 2 agents, 30-day retention, 500 conversations) is acceptable only for internal test, because retention is likely too short for a financial-product support record (Assumption, counsel to set retention).

### A.6 Channels

Telegram, WhatsApp (embedded signup, manual, Twilio), Facebook, Instagram, Email, SMS, Line, TikTok and API channel inboxes are documented ([Help center index](https://www.chatwoot.com/hc/user-guide/en); [Telegram](https://www.chatwoot.com/hc/user-guide/articles/1677838569-how-to-setup-a-telegram-channel) requires a BotFather token; Business-mode bots have a "24-hour reply window"). Verified capability, 2026-10-08. Cloud Hacker is live chat only; paid plans list "all channels". **Phase 0 recommendation: website live chat only.** Telegram/WhatsApp contacts cannot carry the HMAC-verified Helm member ID, so agents must not act on account-specific requests there without re-verification in the Helm Web App.

### A.7 Phase 0 minimum (Recommended design)

| Item | Phase 0 | Post-MVP |
|---|---|---|
| Deployment | Chatwoot Cloud, Startups or Business plan (Business if automation/teams wanted) | Self-host or Enterprise only if residency, SSO or audit requirements demand |
| Channel | One Website inbox in the authenticated Helm Web App | Email, Telegram/WhatsApp with verification procedure |
| Identity | HMAC identity validation, enforced; identifier = Helm member ID; `reset()` on logout | — |
| Context | 4–6 custom attributes, no secrets | Helm admin deep-link from contact |
| Integration | Backend HMAC endpoint + signed webhook receiver (log/link) | Conversation tagging into Helm reporting |
| Roles | Administrator / Agent; MFA | Custom roles, SSO, audit logs |
| Cyclone effort | Assumption: ~2–4 developer-days (HMAC endpoint, widget wiring, attributes, webhook receiver, tests) | — |

---

## Part B — Funding: direct Wallet Funding vs integrated purchase via Paymenture

### B.1 Direct crypto Wallet Funding (base case)

- **Recommended design:** Member transfers the one supported asset on the one supported network from an exchange or external wallet to their Privy wallet address. Helm shows the address, network and asset with warnings; observes chain confirmations; shows pending/confirmed/failed; screens the source address (see Part C). Wallet Funding creates no Vault Position and no Commission eligibility (Glossary).
- **Reused finding:** every major on-ramp whose terms were readable restricts MLM; a crypto-direct Release 1 "depends on no on-ramp partner's approval" and "does not remove KYC/AML obligations". Verified on 2026-10-06 in `inputs/discovery/notes-03-fiat-onramp.md` §1, §5 (e.g. [Stripe list](https://stripe.com/legal/restricted-businesses), [Bridge legal](https://www.bridge.xyz/legal), [Coinbase prohibited use](https://www.coinbase.com/legal/prohibited_use), [Transak AUP](https://transak.com/acceptable-use-policy)).
- **Privy funding features to avoid:** fiat deposits, payouts and custodial wallets run on Bridge; Bridge prohibits "multi-level marketing" — Verified 2026-10-06 in `notes-02-wallets-custody.md` ([Bridge Developer Agreement](https://www.bridge.xyz/legal/developer-agreement), [Privy fiat deposits](https://docs.privy.io/wallets/funding/fiat-deposits/overview)).

### B.2 Paymenture — what the public pages show

| Topic | Finding | Label |
|---|---|---|
| What it is | "provides the complete financial infrastructure for businesses to onboard users, payout globally to 200 countries in 145+ local currencies, issue debit cards, support digital assets, offer alternative payment methods and streamline compliance—all through a single integration." | Verified (self-description) — [paymenture.com](https://paymenture.com/), 2026-10-08 |
| Entity | Paymenture, LLC, 355 South 520 West, Suite 100, Lindon, Utah 84042, US; terms governed by "the laws of the State of Utah" | Verified — [Licensing disclosures](https://paymenture.com/legal/licensing-disclosures), [Business Platform Terms](https://paymenture.com/legal/business-platform-terms) |
| Regulatory status | "Paymenture is not a bank; Paymenture is not a deposit-taking institution; Paymenture is not a trustee; Paymenture is not a custodian; and Paymenture does not provide regulated financial services directly." Services via "sponsor banks; card issuers; electronic money institutions ("EMIs"); payment processors; virtual asset service providers ("VASPs"); custodians; payment institutions; or other regulated Service Providers" — **none named**. No licence or regulator listed | Verified — [Licensing disclosures](https://paymenture.com/legal/licensing-disclosures) |
| Jurisdictions | "Availability varies by: jurisdiction; product; provider; and regulatory requirements." No country list. Consumers must "not be located in a prohibited jurisdiction" (list not published) | Verified (absence of list) — same; [Consumer Terms](https://paymenture.com/legal/consumer-terms) |
| Assets / networks | Not specified. Paymenture "may add, remove, suspend, restrict, or prohibit support for any blockchain; token; stablecoin; protocol; wallet; exchange; jurisdiction; or Digital Asset Service at any time without notice." | Verified (absence) — [Digital Asset Terms](https://paymenture.com/legal/digital-asset-terms) |
| Fiat→crypto purchase / on-ramp | Not described. Listed services: "cryptocurrency transfers; stablecoin settlement; blockchain wallet functionality; digital asset exchange or conversion" | Verified (absence of on-ramp description) — same |
| Integration model | Homepage: single API integration; links "API Docs" to [paymenture-docs.web.app/docs/mcp-ai-tools](https://paymenture-docs.web.app/docs/mcp-ai-tools). **The docs page rendered only a title (JavaScript app); no endpoints, widget, sandbox or webhook details could be read** | Unreadable — TBD |
| KYC | Consumers: "identity verification; sanctions screening; biometric verification; liveness checks; wallet ownership verification; enhanced due diligence; and ongoing compliance reviews". Businesses: "Paymenture and its Service Providers may require: identity verification, business verification, beneficial ownership verification, source of funds verification, sanctions screening, wallet ownership verification; and enhanced due diligence." Monitoring of "transactions, wallets, counterparties, blockchain activity…" and "Travel Rule obligations" referenced. Whether Helm may rely on Paymenture's KYC: not addressed | Verified — [Consumer Terms](https://paymenture.com/legal/consumer-terms), [AML/KYC disclosure](https://paymenture.com/legal/aml-kyc-disclosure) |
| Contracting model | Consumer Terms are "between you … and Paymenture, LLC", for "personal, family, or household purposes" — i.e. Members would contract with Paymenture directly | Verified — [Consumer Terms](https://paymenture.com/legal/consumer-terms) |
| Merchant onboarding | Business must be "validly organized and in good standing"; ongoing KYB | Verified — [Business Platform Terms](https://paymenture.com/legal/business-platform-terms) |
| Prohibited (AUP, updated May 22, 2026) | Section 02 Prohibited Business Models: "pyramid schemes; Ponzi schemes; deceptive investment schemes". Section 01: "prohibited gambling", "prohibited digital asset activity". Words "multi-level", "MLM", "network marketing", "referral", "affiliate", "staking", "yield": **not present** | Verified — [AUP](https://paymenture.com/legal/acceptable-use-policy) |
| Prohibited (Business Platform Terms §05) | "You agree not to use the Services in connection with: money laundering; terrorist financing; fraud; sanctions evasion; shell banks; darknet marketplaces; gambling where prohibited; unlawful financial services; deceptive business practices; counterfeit goods; human trafficking; narcotics trafficking; prohibited weapons; Ponzi or pyramid schemes; privacy-enhancing technologies prohibited by Paymenture; mixers or tumblers; unauthorized money transmission; ransomware proceeds; unlawful digital asset activity; or any activity prohibited under applicable law or Paymenture policy." | Verified — [Business Platform Terms](https://paymenture.com/legal/business-platform-terms) |
| Suspension | May "suspend, restrict, or terminate access to the Services immediately where... required by law... suspicious activity is detected... sanctions concerns arise... fraud risk exists." | Verified — same |
| Fees | "platform fees... transaction fees... FX fees... blockchain/network fees... compliance fees... reserve obligations" — no amounts published | Verified (no public prices) — same |
| Deposit insurance | "Balances accessible through the Services are not insured by the FDIC." | Verified — [Licensing disclosures](https://paymenture.com/legal/licensing-disclosures) |

**Interpretation (analyst assessment, not legal advice):** Paymenture's own terms do not name MLM, unlike Stripe/Bridge/Coinbase/Transak. But (a) the regulated activity is performed by unnamed sponsor banks/VASPs whose policies are unknown and, per discovery note 03, the industry pattern is MLM restriction driven by card-network and bank rules; (b) "pyramid schemes" and "deceptive investment schemes" make acceptance depend on how counsel characterises the referral model and the Yield Product; (c) "any activity prohibited under … Paymenture policy" leaves discretion. Acceptance must come as written confirmation after full disclosure.

### B.3 Comparison and recommendation

| Dimension | Direct crypto Wallet Funding | Integrated purchase via Paymenture |
|---|---|---|
| Provider approval needed | None | KYB + business-model acceptance (TBD) |
| Evidence of assets/networks | Chosen by Helm (one asset, one network) | Not published |
| Evidence of an embeddable purchase flow | n/a | Not found on readable pages |
| KYC | Helm's own decision (Part C) | Paymenture runs consumer KYC; reliance TBD |
| Cyclone work | Address display, chain observer, status, screening hook | Plus API/widget integration, webhooks, reconciliation, Member terms with a third contracting party (all TBD; docs unreadable) |
| Schedule impact | On the critical path already | Adds unknown provider lead time; would become a launch dependency |
| Member friction | Member needs crypto already (exchange account) | Lower, if it works |

**Recommendation:** Do not include Paymenture in the MVP. Keep a provider-neutral funding seam (from discovery note 03). If Business requires integrated purchase at launch, it becomes a critical-path dependency with the questions in §5.2 answered in writing first; Cyclone cannot estimate integration until docs are accessible.

---

## Part C — Compliance applicability on the confirmed stack

### C.1 Background evidence reused (discovery note 06, verified 2026-10-06)

- FATF: a business with "control" over Members' virtual assets may be a VASP; CDD occasional-transaction threshold "USD/EUR 1 000"; Travel Rule applies; transfers with unhosted wallets are within monitoring and sanctions obligations ([FATF 2021 guidance](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html), paras 72–76, 146, 295–296).
- "Non-custodial" is a fact test: FinCEN four-factor test "regardless of the label" ([FIN-2019-G001](https://www.fincen.gov/sites/default/files/2019-05/FinCEN%20Guidance%20CVC%20FINAL%20508.pdf)); MiCA custody covers control of "the means of access" ([MiCA](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)); EU TFR applies to self-hosted transfers where a CASP is involved, self-hosted ownership check above EUR 1,000 ([TFR](https://eur-lex.europa.eu/eli/reg/2023/1113/oj)).
- MLM/securities questions are separate from AML: FTC MLM guidance (recruitment rewards unrelated to sales; earnings claims) ([FTC](https://www.ftc.gov/business-guidance/resources/business-guidance-concerning-multi-level-marketing)); Howey and SEC interpretation of 17 March 2026 ([SEC 2026-30](https://www.sec.gov/newsroom/press-releases/2026-30-sec-clarifies-application-federal-securities-laws-crypto-assets)).
- Free sanctions-address screening exists: Chainalysis sanctions oracle ([docs](https://go.chainalysis.com/chainalysis-oracle-docs.html)) and API; TRM Sanctions API ([docs](https://docs.trmlabs.com/guides/sanctions/introduction)). These cover only designated addresses, not indirect exposure.
- Privy KYC/KYB is via Bridge ([Privy KYC](https://docs.privy.io/kyc-kyb/overview.md)); Bridge prohibits MLM; no native sanctions/wallet screening in Privy docs; Privy policies can restrict wallet actions ([Policies](https://docs.privy.io/controls/policies/overview.md)).

These are examples, not applicability findings. Under Phase 0 rules (no Commission assumed, Points non-cash), some triggers are weaker than in the discovery scenario, but **the wallet signing model and the vault product, not the absence of Commissions, determine most AML/custody questions.**

### C.2 Where each control would sit in Phase 0 flows

| Control | Signup / Referral Request | Wallet Funding | Vault Deposit | Redemption | Ongoing |
|---|---|---|---|---|---|
| KYC / identity | Light tier (email, country, DOB attestation) or full KYC, per counsel; gate state on member record | Threshold trigger (cumulative funding) if tiered | Gate before first Vault Deposit if counsel requires | Gate before first Redemption if tiered | Re-verification on change of details; duplicate-person detection (also protects Genealogy) |
| Sanctions — persons | Name screening at signup if identity collected | — | — | Before release if payee identity collected | Ongoing list re-screening |
| Sanctions — wallet addresses | Screen Member wallet address on link | Screen source address of each inbound transfer | Vault contract and asset approved by Business (allowlist) | Screen destination address before Member signs | Re-screen held addresses on list updates |
| AML / transaction monitoring | Velocity limits on signups per device/IP | Thresholds, unusual patterns, indirect exposure (if KYT adopted) | Amount caps per Member (Onyx/Privy policy dependency) | Rapid in-out patterns | Case log, escalation, reporting duties per counsel |
| Geographic restrictions | Country attestation + IP check; block restricted countries | — | Same gate | — | Periodic IP/residency checks |
| Source of funds | — | Above threshold, if required | Above threshold, if required | — | EDD cases |
| Travel Rule | — | Applies only if an entity is a VASP/CASP and transfer involves a VASP | Same question | Same question (self-hosted ownership checks) | — |
| Privacy / disclosures | Terms, privacy notice, consent to data sharing with Privy, PillarsHub, Chatwoot, game service | Asset/network warnings, irreversible transfers | Vault terms, fees, risks, no guaranteed return | Redemption rules and stages | Retention, access requests, support data |
| Referral + Points model | Sponsor disclosure; no earnings claims; self-referral and cycle rejection | Wallet Funding creates no Commission eligibility | Whether Vault Deposit volume goes to PillarsHub only under approved rules | Volume adjustments on Redemption | Points rules: no cash value, not transferable; counsel review of Points ↔ Vault Deposit linkage and any Phase 1 Commissions |

### C.3 What each confirmed provider does or does not provide natively

| Provider | KYC | Sanctions (persons/addresses) | Monitoring | Relevant controls it does offer | Label |
|---|---|---|---|---|---|
| Privy | Only via Bridge (MLM-prohibited) — treat as unavailable | None found | None found | Policy engine to restrict wallet actions (e.g. allowlisted contracts, caps) — tier/plan TBD | Verified 2026-10-06 (notes 02/06) |
| Enzyme Onyx | Not assessed here | Not assessed here | Not assessed here | **Dependency:** whether Onyx supports depositor allowlists / transfer restrictions — Onyx analyst | TBD (see Onyx note) |
| PillarsHub | No KYC evidenced in this research | None evidenced | None | Genealogy record; volume events | Assumption/TBD (verify in PillarsHub note) |
| Chatwoot | None | None | None | HMAC identity validation (proves the chat user is the logged-in Member, not who the person is); contact `blocked` flag; audit logs (Enterprise) | Verified 2026-10-08 (§A) |
| Cyclone game/points | None | — | Abuse controls TBD | Points ledger; event dedupe TBD | TBD |
| Paymenture (if ever used) | Runs consumer KYC, sanctions, monitoring for its own services | Yes, per its disclosures | Yes, per its disclosures | Covers only flows through Paymenture; reliance by Helm not addressed | Verified 2026-10-08 (§B) |

**Conclusion:** within the confirmed stack, identity verification and screening are not provided natively. If counsel requires them, Helm/Business selects a compliance tooling vendor (discovery note 06 lists options with published prices) and Cyclone integrates it at the Helm backend as a gate read by funding, vault and Redemption flows. This adds a component, not a stack substitution.

### C.4 Responsibility matrix

Accountable functions are proposed, not assigned. "Before funds" = must be done before accepting real Member funds. "Blocker" = blocks start of the controlled launch decision itself.

| # | Control | Applicability question | Proposed accountable function | Cyclone work | Provider capability relied on | Evidence needed | Gap | Launch impact |
|---|---|---|---|---|---|---|---|---|
| 1 | Operating entity, custody/signing classification | Given the Privy wallet model and any app signer, does Helm/AlphaWave have "control" (VASP/CASP/MSB)? | Business + legal counsel | Document signing authority and key flows for counsel | Privy wallet architecture (Verified, note 02); final model TBD | Counsel memo per launch jurisdiction | Jurisdiction and wallet model unconfirmed | **Blocker** |
| 2 | KYC / identity tier | Is any no-KYC tier allowed; thresholds for funding, Vault Deposit, Redemption? | Business compliance owner (TBD) + counsel | Member `kyc_tier` state, gates in funding/vault/Redemption flows, pending/rejected UX; build seam now even if tier = none | None native (Privy KYC via Bridge unavailable); vendor TBD | Counsel decision; vendor contract if required | No IDV provider in stack | **Before funds** (seam: immediate) |
| 3 | Sanctions — wallet addresses | Which lists, which addresses, how often? | Business compliance owner | Screen Member wallet on link, inbound source addresses, Redemption destination; block/hold states; log results | Free Chainalysis/TRM sanctions tools (Verified, note 06) or commercial KYT | Screening logs; tested block path | Not in any confirmed provider | **Before funds** (recommended minimum regardless) |
| 4 | Sanctions — persons | Is name/PEP screening required at signup or Redemption? | Business compliance owner + counsel | Hook into identity tier; re-screen job | Vendor TBD | Counsel decision | Depends on #2 | Before funds if required |
| 5 | AML / transaction monitoring, SAR/escalation | What monitoring, reporting duties, MLRO? | Business (MLRO/compliance, TBD) | Thresholds, velocity rules, exception queue in Helm admin, case log | KYT vendor TBD; Privy policies for caps (plan TBD) | Written procedure; tested alerts | No monitoring in stack; authority to hold/refuse funds undefined | Before funds (minimum: thresholds + manual review); KYT post-MVP if allowed |
| 6 | Geographic restrictions | Which countries are excluded or targeted? | Business + counsel | Country attestation, IP check, block list config, marketing guidance | None native | Approved country list | Target markets unknown | **Blocker** for launch cohort definition |
| 7 | Source of funds | Required above which amounts? | Business compliance + counsel | Questionnaire step, document upload via vendor, EDD flag | Vendor TBD | Counsel threshold | — | Before funds if required; else post-MVP |
| 8 | Travel Rule / self-hosted address verification | Is any entity a VASP/CASP; do transfers involve VASPs? | Counsel | Address-ownership proof step (e.g. signed message) only if required | Vendor TBD | Counsel decision | — | Before funds if applicable |
| 9 | Vault eligibility / depositor restriction | Must only eligible Members deposit? Can Onyx enforce it? | Business + Enzyme | Gate in Helm; on-chain allowlist if supported | **Onyx depositor allowlist — dependency on Onyx analyst** | Onyx configuration evidence | TBD | Before funds |
| 10 | Product characterisation (Yield Product, vault terms, no guaranteed return) | Securities/collective-investment questions for the vault | Business + counsel | Terms/fee/risk screens with acceptance record | Onyx actual strategy/fees (Onyx note) | Approved terms text | Strategy unconfirmed | **Blocker** |
| 11 | Referral model, Genealogy, Points | Is the referral model, any Vault-Deposit-linked volume and Points lawful/disclosed correctly? Are Points a financial reward? | Business + counsel | Sponsor disclosure, self-referral/cycle checks, Points rules page, no earnings claims, keep Points separate from money | PillarsHub, game service (TBD) | Approved rules and disclosures | Phase 1 Commissions excluded; Points rules unapproved | Before funds (disclosures); Commission review before Phase 1 |
| 12 | Member terms, privacy, consent, retention | Which notices, data-sharing consents, retention periods? | Business (legal/DPO) | Consent capture with version; data map per provider; retention jobs; DSAR procedure | Chatwoot Cloud US-hosted (Verified); Privy/PillarsHub DPAs TBD | Published terms + privacy notice; DPAs | DPAs not reviewed | **Before funds** |
| 13 | Support data access and impersonation | Who can see Member data; can support be socially engineered? | Business operations | HMAC enforced, no secrets in attributes, `reset()` on logout, MFA, support script banning seed-phrase requests | Chatwoot identity validation, roles (Verified) | Config screenshots; test of unverified rejection | Audit logs Enterprise only | Before funds (config); audit logs post-MVP |
| 14 | Records and audit trail | What must be retained, how long? | Business + counsel | Immutable event log for identity decisions, screening, funding, vault, Redemption, Sponsor Edge corrections | Chain data; provider logs | Retention policy | — | Before funds |
| 15 | Provider terms compatibility | Do Privy, Enzyme, PillarsHub, Chatwoot (and any payment provider) accept the model on full disclosure? | Business | Avoid Bridge/Stripe-backed Privy features | Privy AUP has no MLM entry (Verified, note 03); others TBD | Written confirmations | Privy written confirmation outstanding (note 02) | Before funds |
| 16 | Flagged-user / flagged-transaction handling | What may Helm lawfully do (refuse, hold, report)? Can it freeze anything? | Counsel + Business | Pending/restricted states; Helm can refuse service in its app; cannot freeze self-custodied assets unless model gives that authority | Privy policies (scope TBD); Onyx controls (TBD) | Written escalation procedure | Fund-freezing authority undefined (do not assume) | Before funds |

### C.5 Prioritised actions

- **Start immediately (Cyclone):** member-record gate fields (`kyc_tier`, `screening_status`, `eligibility_status`); address-screening hook with free sanctions API; country attestation; consent capture; event log; Chatwoot HMAC integration.
- **Before real funds (Business + counsel):** items marked Blocker / Before funds in C.4; at minimum entity and custody classification, launch countries, KYC tier decision, vault terms, Member terms and privacy notice, escalation procedure, provider confirmations.
- **Post-MVP if counsel allows:** commercial KYT, Chatwoot audit logs/SSO, custom roles, additional support channels, integrated purchase provider.

---

## 5. Open questions

### 5.1 Chatwoot
1. Are custom roles, MFA and the "Require identity validation" setting available on Cloud Startups/Business, or only higher plans?
2. Webhook delivery: retry policy, timeouts, ordering, and whether `X-Chatwoot-Delivery` is always present?
3. Is an EU (or other non-US) Cloud region available, and is a DPA/subprocessor list available for Cloud?
4. Annual billing terms and whether Captain AI can be disabled per account (to keep conversation data out of AI processing).
5. Retention: can Cloud retention be extended beyond the plan default, and can contacts/conversations be deleted on request?

### 5.2 Paymenture (only if Business wants integrated purchase)
1. Will you accept, in writing, a platform whose Members join through a referral programme recorded in a Genealogy, with a vault product (Yield Product)? Does your "pyramid schemes; … deceptive investment schemes" clause, or any sponsor bank/VASP policy, exclude it?
2. Which regulated Service Providers (names, licences, jurisdictions) perform fiat-to-crypto purchase, and which countries are supported/prohibited?
3. Do you offer a fiat-to-crypto purchase that delivers to a Member's own (Privy) wallet address on a specified network, with locked address? Which assets and networks?
4. Integration: widget or API, sandbox, webhooks, idempotency; please provide readable API docs.
5. Who is merchant of record; who bears chargebacks; can Helm rely on your KYC for its own obligations?
6. Fees, minimums, reserve requirements, KYB documents and lead time.

### 5.3 Legal counsel
1. Launch jurisdictions and operating entity; are any regimes (VASP/CASP/MSB) triggered by the confirmed Privy wallet model and vault flow?
2. Is a no-KYC or light-KYC tier permissible for Wallet Funding, Vault Deposit and Redemption; at what thresholds?
3. Required sanctions screening (persons and addresses), lists and frequency; reporting and record-keeping duties; MLRO requirement.
4. Does the Travel Rule or self-hosted address verification apply to Redemption to external addresses?
5. Characterisation of the vault product and required disclosures.
6. Is the referral model plus Points lawful as designed for Phase 0, and what changes once Phase 1 Commissions are introduced? Do Points require any disclosure even with no cash value?
7. What lawful action can Helm take on a flagged Member or transfer (refuse service, hold, report) given self-custodied wallets?
8. Privacy: lawful basis, cross-border transfers (Chatwoot Cloud is US-hosted), retention periods for support and identity data.

---

## 6. Limitations

- WebSearch was unavailable; only official Chatwoot and Paymenture pages were fetched. Content was extracted through a summarising fetch tool, so quotes are as returned by that tool; exact wording should be re-checked before contractual use.
- `https://www.chatwoot.com/docs/product/channels/live-chat/sdk/setup` returned an unrelated WordPress installation article; the SDK methods were taken from the Chatwoot help-center article instead. Some help-center links redirect to `chatwoot.help`.
- The Chatwoot Cloud pricing page does not say which plan includes custom roles or MFA; webhook retry behaviour is undocumented in the pages read.
- Paymenture's developer docs (`paymenture-docs.web.app`) are a JavaScript app and could not be read; assets, networks, jurisdictions, fees and integration details are therefore unknown. Wallet, API, cardholder, privacy and DPA terms were not read.
- Enzyme Onyx and PillarsHub compliance-related capabilities were not researched here (dependencies on other notes). Discovery findings (notes 02, 03, 06) were reused without re-verification; their research date is 2026-10-06.
- No sign-up, login or provider contact was made. Nothing here is a legal conclusion.
