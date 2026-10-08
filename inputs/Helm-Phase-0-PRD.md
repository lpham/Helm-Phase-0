# Helm Phase 0 — High-Level PRD

**Status:** Implementation PRD draft for the confirmed stack. PillarsHub, Chatwoot, Enzyme Onyx, Privy, the custom Helm App, and reuse of Cyclone’s game/points are the implementation baseline. Configuration, integration feasibility, responsibilities, dates, budgets, and acceptance thresholds still require confirmation. Do not reopen provider selection.

## 1. Business objective

Launch the smallest usable Helm product that lets users join, fund their wallets with crypto, participate in an approved vault, and engage through existing gamification. Capture a reliable referral network from the first signup so Phase 1 can expand compensation without rebuilding or losing history.

Capital is waiting to be deployed. Reduce time to first approved deployment by reusing existing services, limiting custom development, and resolving the critical dependencies early. Do not promise returns or treat available capital as proof that the vault is ready to accept funds.

## 2. Confirmed platform stack and business solution

Users see one Helm experience. Existing providers supply the underlying capabilities:

| Business capability | Confirmed component | Implementation work to resolve |
| --- | --- | --- |
| Join Helm and use a wallet | Privy | Confirm wallet model and supported network |
| Record referral relationships and prepare compensation | PillarsHub | Validate configuration, PRD fit, and Phase 1 portability |
| Deposit into and redeem from a vault | Enzyme Onyx | Confirm actual strategy and deployment readiness |
| Receive customer support | Chatwoot | Define minimum support integration |
| Engage through games and points | Cyclone Tap Prediction and points system | Validate existing assets and integration readiness |
| Connect everything for users and operations | Custom Helm Web App and backend | Define minimum custom integration scope |

Onyx is vault infrastructure; calling the product a staking vault does not establish its yield strategy. Privy embedded wallets are not automatically smart contract wallets. Both choices must be explicit.

## 3. Users and journeys

- **Member:** Arrive through an invite or direct link → sign up → establish referral relationship → connect/create wallet → fund wallet → review vault terms → approve and deposit → view confirmed position → engage through games/points → request support or redeem.
- **Operations administrator:** Review onboarding and referral exceptions, reconcile deposits and vault positions, monitor integration failures, manage support, and use controlled administrative permissions.
- **Business reviewer:** View onboarding, funding, vault participation, referral growth, and engagement results to decide on expansion.

## 4. MVP requirements and acceptance outcomes

| Area | Phase 0 requirement | Acceptance outcome |
| --- | --- | --- |
| Onboarding | Authenticate users and create one stable Helm identity | Repeat login resolves to the same member; duplicate accounts are handled through an agreed process |
| Wallet | Link/create a supported wallet and explain signing responsibilities | User can access the wallet and authorize a supported transaction; recovery behavior is documented |
| Genealogy | Capture sponsor at signup; validate it and sync to PillarsHub | Each accepted relationship is traceable; invalid/self/cyclic referrals are rejected; failed syncs can be retried without duplication |
| Crypto funding | Support direct crypto transfer on one chosen network and asset initially | Show supported asset/network and distinguish pending, confirmed, and failed funding; balances reconcile with chain evidence |
| Vault | Display approved terms, fees, risks, deposit and redemption rules | User can complete an approved deposit and see the confirmed position; redemption works according to the selected vault's actual rules |
| Gamification | Reuse the existing game and points system with minimum integration | Verified activity awards points once; rules and limits are visible; duplicate or abusive events are handled |
| Support | Provide an accessible support channel with relevant user context | User can open a conversation; support can identify the member without exposing private keys or secrets |
| Operations | Provide minimum monitoring, reconciliation, and controlled admin actions | Operations can identify failed transactions, mismatches, and sync errors and resolve or escalate them |
| Reporting | Report onboarding, funded users, confirmed vault participation, referrals, and engagement | Metric definitions and data freshness are visible; reports avoid double-counting wallet transfers and vault deposits |

Proposed default: Phase 0 points have no cash value and do not create a token or financial reward obligation. Business must approve the rules. Phase 0 commission calculation/payment is not assumed: validate against Terrel's PRD and explicitly decide whether the current three-level plan is required for launch.

## 5. Scope boundaries to accelerate launch

**Include:** one approved network, one supported funding asset, one initial vault, direct crypto deposits, basic member/admin views, referral capture and reconciliation, one existing game, points, and basic support.

**Defer unless essential to launch:** integrated fiat/crypto purchase services, additional chains/assets/vaults, new game development, token issuance, complex Phase 1 compensation, custom wallet infrastructure, and extensive provider dashboard duplication.

Direct crypto funding still needs correct network/asset handling, confirmation rules, and operational support. A payment provider is optional for this proposed MVP; if Business requires one at launch, it becomes a critical dependency.

## 6. Genealogy readiness for Phase 1

- Stable Helm member ID with explicit mappings to Privy, PillarsHub, game, and support identities.
- Separate the full sponsor relationship from the three-level commission calculation. Preserve all accepted sponsor edges, not just the currently payable levels.
- Record referral provenance, timestamps, status, and any approved corrections with an audit trail.
- Define handling of missing/invalid sponsors, existing members, account merging, and controlled sponsor changes. Proposed default: prohibit self-service sponsor changes after acceptance.
- Designate PillarsHub as the intended authority for accepted genealogy and validate the required APIs and configuration. Helm keeps pending requests and a reconciled reporting copy. If a capability gap affects this design, specify the smallest adapter or controlled process needed within the confirmed stack.
- Verify export/import and reconciliation of identities, sponsor edges, and relevant historical business events before claiming Phase 1 readiness. Full compensation history support remains a question for the provider.

## 7. Proposed technical architecture and data flow

The following is a design proposal, not a verified description of vendor behavior.

**Structure:** Helm Web App → Helm backend/integration layer → Privy, PillarsHub, Onyx/blockchain, Chatwoot, and Cyclone game/points services. Keep privileged provider credentials on the backend. Reuse provider operations tools where they reduce MVP work.

**Data authority:** Helm owns the member record and provider-ID mapping; Privy provides authentication/wallet identity; PillarsHub owns accepted genealogy/compensation; blockchain and deployed vault contracts establish confirmed transactions and positions; Cyclone’s points service owns points balances. Helm maintains reconciled views and an integration event history.

1. **Signup:** Authenticate → create/resolve Helm member → validate referral request → submit to MLM core → mark accepted only after acknowledgment → retry/reconcile failures.
2. **Wallet funding:** User receives/transfers the supported asset → observe chain confirmations → update funding status → reconcile wallet balance. A wallet transfer alone does not create a vault investment or commission eligibility.
3. **Vault deposit:** Display terms → user authorizes required approval/deposit → track transaction → confirm actual vault event/position → record business event → submit eligible volume to MLM only under approved rules.
4. **Gamification:** Receive verified gameplay/activity event → deduplicate → apply agreed points rules → update points balance and member view. Keep points separate from money, vault shares, and commissions.
5. **Redemption:** User submits request → track any pending/approval/settlement stages supported by the vault → confirm withdrawal → reconcile position and applicable business adjustments.
6. **Support:** Link the member to a support contact and send only necessary context. Support actions must not authorize fund movement.

Use unique event IDs, transaction references, retry queues, reconciliation jobs, and an audit log so delayed or repeated notifications do not duplicate deposits, points, or commission volume. Verify actual webhook/event availability before choosing each integration mechanism.

## 8. Critical decisions and launch dependencies

| Decision/dependency | Proposed responsible function; not an assigned owner |
| --- | --- |
| Approve minimum scope and whether three-level commissions are required | Business |
| Validate PillarsHub access, PRD fit, full genealogy, exports, and setup lead time | Business + Tech + provider |
| Assess existing-user/data migration needs from FirstAlphaWave/TaQUANT, only if applicable; PillarsHub remains the confirmed MLM core | Business + Tech |
| Select network, asset, wallet authority, strategy, and vault rules | Business + Tech + providers |
| Agree Onyx configuration, contract, commercial terms, deployment, and admin handover | Business + Enzyme |
| Confirm applicable legal structure, user eligibility, disclosures, and launch requirements | Business + qualified legal adviser |
| Verify relevant audit coverage and review Helm-specific permissions/integrations | Tech + security reviewers |
| Approve points rules and validate game readiness | Business + Cyclone |

Researching vendor audits does not by itself confirm that the configured vault, strategy, or Helm integration has been reviewed. Set acceptance requirements for the actual deployment before accepting user funds.

### Security and compliance requirements for implementation

The confirmed stack does not remove Helm’s responsibility to establish deployment-specific security and applicable compliance requirements. This PRD requires an applicability assessment; it does not assert that particular legal obligations already apply or have been satisfied.

| Area | Required assessment or implementation outcome |
| --- | --- |
| Security and custody | Document wallet signing/recovery, vault administration, approval permissions, secrets management, access controls, and test/production separation; verify relevant audit scope and review Helm-specific integrations |
| KYC/identity and eligibility | Determine requirements for the operating entity and intended users; define eligibility checks and pending/rejected states where applicable |
| AML and source of funds | Determine applicable monitoring and source-of-funds requirements for the actual funding and vault flows; document review and escalation procedures |
| Sanctions and geographic restrictions | Determine applicable screening/restrictions and required screening points; verify available provider support and identify integration gaps |
| Transaction handling | Define handling of flagged funding, deposits, and redemptions, including permissions and legal authority for any restriction; direct crypto funding does not by itself establish exemption |
| Privacy and disclosures | Define necessary user terms, risk/fee disclosures, consent, data sharing, retention, and access to identity and support data |
| Referral and gamification model | Assess the actual compensation and reward rules where relevant; keep points separate from financial balances and do not assume non-cash rewards remove every compliance issue |
| Operations | Establish monitoring, incident contacts, provider escalation, reconciliation, and documented resolution of security/compliance exceptions |

Produce a responsibility matrix covering **Helm/Business, Cyclone, Privy, Enzyme Onyx, PillarsHub, Chatwoot, and game/points services**, plus a payment provider only if included. For each control, record applicability, proposed accountable function, implementation responsibility, verified provider coverage, evidence needed, unresolved gaps, and whether it blocks launch. Final named owners remain TBD until agreed.

Acceptance for launch: relevant applicability questions are resolved with qualified reviewers, required controls are implemented and checked, and responsibilities are agreed before accepting real funds. Separate these requirements from nonblocking improvements so implementation can begin promptly on the confirmed stack.

## 9. Delivery approach

1. **Configuration and access:** Obtain the confirmed providers’ environments and Terrel’s PRD; finalize funding path, wallet model, vault strategy, integration contracts, and launch scope.
2. **Thin end-to-end slice:** Demonstrate signup → referral capture → wallet funding → vault deposit → confirmed position → redemption on an appropriate test environment, plus one game-to-points flow.
3. **MVP completion:** Add reconciliation, exception handling, support, admin visibility, and required user terms.
4. **Controlled launch:** Start with the approved cohort and limits, verify operations, then expand after the agreed checks pass.

Dates and cost estimates are TBD until team capacity and provider lead times are known. Separate tasks Cyclone can start immediately from vendor/legal dependencies; do not allow optional features to delay the core funding journey.

## 10. Success measures and open inputs

Track time to first approved live deposit, signup completion, signup-to-funded conversion, confirmed vault participation, referral attribution completeness, reconciliation exceptions, game participation, repeat engagement, and support resolution. Targets are TBD; investment returns are not an MVP delivery guarantee.

Missing inputs: Terrel's PRD, Phase 1 compensation rules, user jurisdictions, intended custody/signing model, selected chain/asset/strategy, deposit/redemption terms, funding source and launch cohort, provider contracts and SLAs, team capacity, budget, game integration documentation, data retention requirements, and launch acceptance thresholds.
