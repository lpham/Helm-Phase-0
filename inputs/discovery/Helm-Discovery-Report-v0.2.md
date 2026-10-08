# Executive summary and recommended direction

## Purpose

AlphaWave intends to offer a crypto-based financial product through its established multi-level marketing (MLM) network. This report identifies the fastest credible way to build a first release from existing software. It covers MLM and CRM vendors, wallet and custody infrastructure, fiat on-ramps, Yield Product options and compliance tooling, and it recommends an architecture, a cost envelope and a 30-day scope.

The research was desk-based and conducted on 6 October 2026. No vendor was contacted and no account was opened. Every material claim is labelled as verified, a vendor claim, a working assumption or not verified (see section 12).

## Recommended direction

**Primary: a modular architecture (Option 2).** AlphaWave buys each core capability from a specialist and Cyclone integrates them behind one Member experience and one admin back office:

- **MLM core:** a headless commission engine and Sponsor Tree. MLM Soft is the lead candidate, with Exigo as the alternative to demonstrate side by side.
- **Member wallets:** Privy embedded wallets, owned by the Member, with no Privy features that depend on Stripe or Bridge.
- **Operator treasury:** a separate wallet with multi-person approval for Commission payouts.
- **Ledger and back office:** owned by Cyclone. The ledger is the single financial source of truth.
- **Compliance tooling:** tiered KYC (Sumsub or Didit) and sanctions screening of every wallet address from day one.
- **Customer operations:** a SaaS helpdesk (Zendesk or Freshdesk) linked to the back office, with CRM deferred.
- **Yield Product:** a provider-neutral adapter built now, switched on later, with Privy Earn (Morpho or Aave vaults) as the shortest route.

**Fallback: the same modular design with different components.** A Stripe-independent wallet stack, Turnkey with Alchemy Smart Wallets or ZeroDev Kernel, replaces Privy for Member wallets, and Fireblocks, Cobo or a Safe multisig runs the treasury. Because Privy is owned by Stripe, this alternative should be tested in parallel from week 1. Exigo or Epixel replaces MLM Soft if the lead candidate fails its demonstration or security due diligence. The integrated white-label option (Option 1) is not recommended for real funds because no candidate documents custody, signing authority or a genuine yield source.

**QUANT (Option 3)** is treated as a Phase 2 integration for algorithmic trading only. Its engine is not a dependency of the first release, and no Member funds are exposed to it in that release.

## Headline findings

1. **No MLM vendor offers a genuine Yield Product.** Every "staking" or "investment plan" feature found is an operator-set percentage displayed on a dashboard, with no named protocol behind it. A Yield Product must therefore come from outside the MLM software.
2. **Stripe, and almost every major fiat on-ramp, prohibits MLM businesses.** Stripe lists "Multilevel marketing services offering commission or recruitment-based sales" and "Cryptocurrency mining and staking" as prohibited (updated 22 September 2026). Coinbase, Transak, Banxa, Ramp and Bridge carry similar prohibitions. **Release 1 should accept crypto Deposits only**; fiat is a gated Phase 2 item.
3. **Privy fits the wallet requirement technically, but not through its Stripe-backed features.** Its fiat, custodial-wallet and KYC features run on Bridge, a Stripe company whose terms prohibit MLM. Its core wallet, policy engine and Earn features are usable, subject to Privy's written acceptance of the business model and an Enterprise quotation.
4. **Custody depends on who controls signing, not on labels.** Embedded wallets with a platform-held signer are a hybrid model, and an operator-run vault is custodial. Global AML standards test control in the same way.
5. **The assumption that crypto Deposits need no KYC is not supported.** The client's own compensation plan requires KYC for leadership ranks, on-ramps impose KYC, and Commission payouts always leave an operator-controlled treasury. Tiered KYC is the planning base case, pending legal advice.
6. **The commission base is the most consequential open business question.** Crypto-MLM software most commonly pays Commissions on Members' Deposits or on calculated returns, which are the patterns regulators associate with Ponzi and pyramid schemes. Paying Commissions from platform fee revenue, such as a fee on real yield, is structurally safer, and MLM Soft's documentation shows it can calculate on such amounts. The previous subscription-based plan is superseded and the client must confirm the new base.

## Can real funds be accepted within 30 days?

**No. A real-funds launch within 30 days is not supported by the evidence.** The gating items are outside engineering control:

- legal characterisation of the compensation plan, custody model and KYC thresholds;
- written acceptance of the MLM model by the wallet, MLM and verification vendors;
- a defined commission base and Yield Product terms;
- an independent security test of the money-handling paths.

**The closest credible milestone at day 30** is a complete end-to-end system on test networks (signup, Sponsor Tree, wallets, Deposits, withdrawals, Commission calculation and treasury payouts, KYC tiers, admin approvals and helpdesk), plus vendor contracts and the legal questions in progress. A controlled real-funds pilot is realistic roughly **10–14 weeks** from start if legal answers arrive within four to six weeks (consultant estimate).

## Indicative cost (external software and services)

| Item | Low | Base | High |
|---|--:|--:|--:|
| One-time (setup, security testing) | $32,000 | $65,000 | $100,000 |
| Monthly operating (pilot scale) | $2,900 | $8,200 | $17,800 |
| Indicative 12-month total | $67,000 | $163,000 | $314,000 |

Implementation effort is about **9 person-months** for the 30-day milestone and about **22 person-months** cumulatively to a controlled pilot. Cyclone's rates are contracted, so effort is shown in person-months only. Section 7 gives the breakdown and the evidence status of each figure.

## What can be decided now, and what needs more work

| Status | Items |
|---|---|
| **Decide now** | Modular architecture direction. Crypto-only Deposits in Release 1. Separate operator treasury with multi-person approval. Cyclone-owned ledger as the financial source of truth. Helpdesk before CRM. Web-first delivery. No Member funds exposed to QUANT in Release 1. No display-only "ROI" modules. |
| **Needs vendor demonstration or quotation** | MLM Soft and Exigo scripted demos against Helm test cases. Privy Enterprise pricing and written acceptance of the MLM model. Turnkey with Alchemy or ZeroDev technical spike as the Stripe-independent wallet alternative. Treasury vendor (Privy key quorum, Cobo or Fireblocks). KYC vendor pricing. Helpdesk trial. |
| **Needs technical due diligence** | MLM Soft security evidence (none published). Privy policy-engine configuration and fee-wrapper audit status. Vault selection criteria for a future Yield Product. QUANT engine, custody and controls (Phase 2). |
| **Needs legal confirmation** | Commission base. Custody classification of the hybrid wallet model. KYC thresholds and Travel Rule. Yield Product characterisation. Target jurisdictions and the operating entity. |
# Business requirements and working assumptions

## Business context

AlphaWave has an established MLM distribution network and wants to offer a financial product through it. The intended platform covers:

- Member onboarding and sponsor attribution;
- wallets or smart accounts;
- crypto Deposits and withdrawals;
- a product currently described as "staking", whose mechanism is not yet defined;
- MLM genealogy and configurable compensation plans;
- administrative tools and customer support;
- fiat deposits, either in the first release or later.

An associated trading company, QUANT, has built an MVP covering onboarding and smart-account creation, and intends to connect a trading engine to Hyperliquid. Its capabilities have not been independently verified. Cyclone is the implementation company and technology lead. It prefers to buy core software and integrate it rather than build core systems.

No operating jurisdiction, legal entity or target market has been confirmed. This report is therefore jurisdiction-neutral. AlphaWave will engage legal counsel on regulatory obligations; nothing in this report is legal advice, and no vendor software or certification authorises the business model.

## Requirements as understood

The client's product requirements document (PRD) and compensation plan overview were treated as statements of business intention, not as validated specifications. The scope below reflects those documents and the decisions taken during this research.

| Area | First release | Later phases |
|---|---|---|
| Onboarding | Signup, sponsor attribution, referral link, privacy-safe downline view | Campaigns, academy, gamification |
| Wallets | Member-owned embedded wallets; separate operator treasury | Additional chains and assets |
| Deposits | Crypto only, assets and networks as supported by the selected components | Fiat on-ramp, subject to provider approval and legal review |
| Withdrawals | Crypto to the Member's own external address | Fiat off-ramp |
| Yield Product | Not live with real funds; provider-neutral adapter and read-only or test-network demonstration | Lending vaults or Staking through a named provider, after legal confirmation |
| MLM | Sponsor Tree, compensation plan configured in the bought engine, Commission calculation separate from payout, tested against defined cases | Full plan, simulations, campaigns |
| Operations | Admin back office with roles, approvals and audit trail; helpdesk | CRM, advanced analytics |
| Trading | None | QUANT integration via Hyperliquid, with restrictions (Option 3) |

## Working assumptions

The following assumptions underpin the recommendations. Each one that materially changes the outcome is flagged in section 11 as a decision for the client.

1. **Cyclone leads technology** and acts as integrator of purchased core software. Self-built compensation engines, including QUANT's, are excluded.
2. **Jurisdiction-neutral design.** Controls are designed to be switched on by policy once counsel has identified obligations.
3. **Privy is the base case for Member wallets**, without any of its Stripe- or Bridge-backed features.
4. **Tiered KYC (scenario B) is the base case** for tooling and cost estimates (see section 3.5).
5. **The commission base is open.** The compensation plan overview pays Commissions on subscription sales, but that model has been superseded. This report presents the bases that real software supports and their structural risks; the client must confirm the base.
6. **Web-first delivery.** The PRD itself excludes a standalone mobile app from the first release.
7. **Pilot scale** for cost purposes: up to 3,000 commission-active Members, under 10,000 monthly active wallet users and about 1,000 new Members per month.

## Contradictions in the reference documents

The research brief takes precedence where documents conflict. The following contradictions and unresolved assumptions were found:

| # | Topic | Observation | Treatment in this report |
|---|---|---|---|
| 1 | Status of the PRD | The PRD calls itself a "final-programme draft", yet leaves custody, compensation formulas, payout rates, KYC thresholds, return claims and vendor selection open. | Treated as non-binding intention. |
| 2 | "Staking" timing | The brief lists staking as a proposed component; the PRD places "Staking or Saving" in Phase 2 and says it "requires a separate definition before build". | Yield Product researched in full but not live in Release 1. |
| 3 | KYC | The client assumes crypto Deposits need no KYC. The PRD leaves KYC open and gated on legal approval; the compensation plan requires KYC for Certified Leader rank and above. | Assumption treated as unverified; tiered KYC is the base case. |
| 4 | Commission base | The compensation plan pays only on subscription sales. That model has since been superseded and the new base is undefined. | Bases compared on evidence; decision required (section 11). |
| 5 | Build status | The compensation plan says the engine is "fully built into the system" and switched off; the PRD says no formula is approved. The brief says Cyclone prefers to buy. | Self-built engines excluded; a bought engine is recommended. |
| 6 | Plan arithmetic | Level rates for levels 2–10 are missing, so total payout cannot be checked against the stated 30% cap per sale. Whether the leadership match counts toward the cap is unclear. | Listed as client questions. |
| 7 | QUANT and Hyperliquid | Central to the brief but absent from the client documents. | QUANT treated as a Phase 2 integration only. |
| 8 | Scope breadth | The PRD roadmap includes binary options, B-Books, debit cards and fund products. | Not researched; flagged as high-sensitivity later-phase items. |
| 9 | Recruitment-based qualification | Ranks depend on counts of verified referrals and active enrollees, and leadership ranks require "plan tier 7 or higher". | Flagged for legal review as an observation, not a conclusion. |
# Key findings and constraints

## "Staking" covers six different mechanisms

The client material uses "staking" for any product that pays a return on deposited crypto. The mechanisms behind that word differ in risk, custody and regulatory profile. This report uses **Yield Product** as the umbrella term and reserves **Staking** for native and liquid proof-of-stake staking.

| Category | Examples | Where the return comes from | Platform must control funds? | Liquidity | Main risks |
|---|---|---|---|---|---|
| Native Staking | ETH validators via Kiln, Figment or Coinbase; SOL or HYPE delegation | Protocol rewards for securing a network | No, if each Member's wallet signs | Chain unbonding periods; HYPE has a 1-day lockup and a 7-day queue | Token price, slashing, provider compromise |
| Liquid Staking | Lido stETH, Rocket Pool rETH, Jito JitoSOL | The same protocol rewards, via a tradable receipt token | No | Market sale (price may deviate) or protocol queue | Receipt-token depeg, smart contract |
| Lending | Aave; Morpho vaults curated by Steakhouse or Gauntlet | Interest paid by borrowers who post crypto collateral | No, if supplied from Member wallets | Usually instant, limited by available liquidity | Smart contract, oracle, bad debt, curator error |
| Trading vault | Hyperliquid HLP and user vaults | Trading profit and loss | No (depositor holds a vault share) | HLP 4-day lockup; user vaults 1 day | **Loss of principal**, market manipulation |
| Operator-managed program | Custodial "earn" programmes; a QUANT-run strategy | Whatever the operator does with pooled funds | **Yes** | Set by operator terms; can be suspended | Operator failure, commingling, highest regulatory sensitivity |
| Return calculator | MLM software "staking", "ROI" or "daily return" plans | **None.** A number credited in a database | Operator holds funds | Depends on new Deposits | Ponzi and pyramid dynamics; not a Yield Product |

Sources: [Hyperliquid staking](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/staking), [Hyperliquid protocol vaults](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/protocol-vaults), [Aave v3 overview](https://aave.com/docs/aave-v3/overview), [Cloud MLM investment plan](https://cloudmlmsoftware.com/mlm-plan/investment-mlm-plan/).

Key points for AlphaWave:

- **For a dollar-denominated product, over-collateralised stablecoin lending is the most credible mechanism.** Interest comes from borrowers, and the Member's position stays in the Member's wallet. Morpho states that Coinbase, Kraken and Deel embed Morpho vaults (vendor claim).
- **Hyperliquid HLP is a trading vault, not Staking.** Press reports document three loss events in 2025 of about $4 million, $12–13.5 million (unrealised) and $4.9 million (not verified against Hyperliquid disclosures). Hyperliquid's published audits cover only its legacy bridge, not the matching engine or HLP logic ([audits page](https://hyperliquid.gitbook.io/hyperliquid-docs/audits), verified).
- **Third-party providers carry real operational risk.** In September 2025 a compromised Kiln API was used to steal about $41 million of SOL from SwissBorg's operator-managed programme ([SwissBorg](https://swissborg.com/blog/swissborg-security-update-kiln-breach), verified). In March 2026 an Aave oracle misconfiguration wrongly liquidated 34 accounts; users were reimbursed from the DAO ([post-mortem](https://governance.aave.com/t/post-mortem-exchange-rate-misallignment-on-wsteth-core-and-prime-instances/24269), verified). In April 2026 the Kelp rsETH bridge exploit left Aave with a large WETH shortfall. A coverage package was proposed and contested; in May most of the unbacked rsETH was recovered through liquidations, with a coalition of protocols committed to cover the remainder ([incident thread](https://governance.aave.com/t/rseth-incident-2026-04-18/24481), [Aave Labs May update](https://governance.aave.com/t/al-development-update-may-2026/25013); final completion not verified).
- **Return-calculator modules are unacceptable as a Yield Product.** The SEC's Forsage action concerned this kind of design ([SEC 2022-134](https://www.sec.gov/newsroom/press-releases/2022-134)).

## Payment providers prohibit MLM

The team's concern about Stripe is justified, and the issue is industry-wide rather than specific to Stripe.

- **Stripe** lists "Pyramid schemes" and "Multilevel marketing services offering commission or recruitment-based sales" as **prohibited** businesses, as well as "Cryptocurrency mining and staking" (page updated 22 September 2026). Its Crypto Onramp merchant terms (§5.4) bind the integrating platform to that list, and Stripe may suspend access without notice. Verified: [Stripe prohibited and restricted businesses](https://stripe.com/legal/restricted-businesses), [Crypto Onramp merchant terms](https://stripe.com/legal/crypto-onramp/merchant-terms).
- **Bridge** (a Stripe company that powers Privy's fiat and custodial features) lists "multi-level marketing" among prohibited activities in §2.1.1 of its [Developer Agreement](https://www.bridge.xyz/legal/developer-agreement). Verified.

| Provider | MLM wording found in terms | Evidence status |
|---|---|---|
| Stripe (incl. Crypto Onramp) | "Multilevel marketing services offering commission or recruitment-based sales"; "Pyramid schemes" | Verified |
| Bridge (Stripe) | "multi-level marketing" | Verified |
| Coinbase Developer Platform | "Multi-level Marketing: Pyramid schemes, network marketing, and referral marketing programs" | Verified (archived copy) |
| Transak | "Multi-level marketing" | Verified |
| Banxa | "Multi-level marketing: pyramid schemes, network marketing, and referral marketing programs" | Verified (December 2024 terms) |
| Ramp Network | "multi-level marketing" among restricted partner industries | Verified (2022 source; current terms to be confirmed) |
| MoonPay | Consumer terms bar "certain multi-level marketing programs"; partner terms not public | Partly verified |
| Mercuryo | "Ponzi or pyramid schemes" | Verified |
| Privy | No MLM wording; prohibits misrepresenting "the nature of the business" | Verified |
| Onramper (aggregator) | No MLM wording; underlying providers' terms still apply | Verified (absence) |

No provider reviewed publishes a positive statement that it accepts MLM businesses. Any acceptance would have to come as written approval after full disclosure of the model.

**Consequences:**

- **Release 1 accepts crypto Deposits only.** Members transfer crypto from a wallet or exchange they already use. This path cannot be switched off by an on-ramp partner. It does not remove KYC or AML obligations.
- **A fiat on-ramp is a gated Phase 2 item.** It requires counsel's characterisation of the compensation plan, full disclosure of the MLM model during provider review, and written approval from at least two providers or from an aggregator plus two underlying providers.
- **Direct fiat acceptance** (taking card or bank payments and converting) brings licensing, chargebacks, safeguarding and three-way reconciliation, and belongs to a later phase.

## Custody is determined by control, not by labels

A model is non-custodial only if no party other than the Member can move the Member's assets without the Member's approval of each action. Embedded wallets, multi-party computation (MPC) and smart accounts are mechanisms; who holds signing authority decides the classification.

| Model | Who can sign | Classification towards Members |
|---|---|---|
| Privy embedded wallet, Member-owned, no platform signer | Member, with Privy's enclave share | Non-custodial (dependent on the vendor) |
| Privy embedded wallet with a platform signer limited by policy | Member, or the platform within the policy | **Hybrid** |
| Platform signer with broad permissions | Effectively the platform | Custodial in substance |
| Key quorum requiring both Member and platform | Both | Non-custodial for outflows, with a platform veto |
| Operator MPC vault (Fireblocks, Cobo, BitGo) | Operator, co-signed by the vendor | **Custodial** (the operator is the custodian) |
| Licensed third-party custodian | Custodian on operator instruction | Custodial (third-party) |

Vendors that market MPC vaults as "self-custody" mean self-custody for the business, not for its customers. **Commission payouts require an operator treasury in every model, and that treasury is always custodial.** The design choice concerns where Member Deposits sit.

Regulators apply the same test. The FATF counts any business with "control" over virtual assets as a virtual asset service provider (VASP), including shared or multi-signature control ([FATF 2021 guidance](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html), paragraphs 72–76). FinCEN treats a provider as a money transmitter "regardless of the label the person applies to itself" ([FIN-2019-G001](https://www.fincen.gov/sites/default/files/2019-05/FinCEN%20Guidance%20CVC%20FINAL%20508.pdf), §4.2). The EU MiCA definition of custody covers controlling "the means of access" to crypto-assets ([MiCA](https://eur-lex.europa.eu/eli/reg/2023/1114/oj), Art. 3(1)(17)). These are examples; which regime applies is for counsel.

## KYC: three scenarios

The client's assumption that crypto Deposits need no KYC cannot be confirmed from the software side. For VASPs, the FATF threshold for occasional transactions is USD/EUR 1,000 and the Travel Rule applies (FATF guidance, paragraph 146). The EU Transfer of Funds Regulation, for example, covers transfers to self-hosted wallets and has no minimum amount for crypto ([TFR](https://eur-lex.europa.eu/eli/reg/2023/1113/oj)).

| | A: KYC at onboarding | **B: Tiered KYC (base case)** | C: Crypto only, no KYC |
|---|---|---|---|
| Member experience | Document and liveness check before any Deposit | Light checks at signup; full check triggered by thresholds (Deposits, first withdrawal, Commission earned, Yield Product access) | Wallet signup only |
| Tooling | Identity verification, AML screening, wallet screening, case management | As A, plus a tier engine and threshold logic in the ledger | Wallet screening only |
| Fiat on-ramp | Provider still runs its own KYC | Same | Route effectively closed |
| Commission payouts | Payee identity known | Full KYC before payouts above a threshold | Payouts to anonymous wallets; sanctions, duplicate-account and clawback risk |
| Vendor and banking access | Easiest to explain | Explainable with counsel-approved thresholds | May block custody, banking and payment relationships |
| Reversibility | Can be relaxed later | Thresholds can be tuned | Hard to tighten after launch |

**Whatever the scenario, every Deposit source address, withdrawal address and payout address should be screened against sanctions lists from day one.** The free [Chainalysis sanctions oracle](https://go.chainalysis.com/chainalysis-oracle-docs.html) is the minimum. Build the identity gates into Release 1 even before thresholds are set; adding KYC after Members have deposited is harder than switching on a tier that already exists.

## Commission base: what the software actually supports

The compensation plan overview pays Commissions on subscription sales. That model is superseded, and the new base has not been defined. Rather than propose a base from first principles, the research examined what real MLM software supports.

| Base | Evidence from vendors | Status | Observation |
|---|---|---|---|
| Product orders | Exigo, ByDesign, DirectScale organise around orders and products | Verified (docs) | Default for enterprise platforms; a non-product base needs synthetic orders |
| Deposit ("investment") amount | Hybrid MLM: "Commissions are earned when a recruit makes an initial investment"; Cloud MLM: "daily percentage returns based on individual member investments" | Verified (as described) | **The most common base in crypto-MLM software.** Rewards funded by new Deposits are the structural pattern behind Ponzi and pyramid concerns |
| Calculated "ROI" | Hybrid MLM: "whenever a recruit's investment generates ROI" | Verified (as described) | The "ROI" is itself an operator-set number, not protocol yield |
| Entry or package fee | ARM MLM "Forsage clone": "Pay 0.5 ETH to join" | Verified (as described) | The pattern the SEC alleged in the Forsage case |
| Trading activity | Epixel: "new trader registration or ... the first trade" | Vendor claim | Relevant only if trading is integrated later |
| Arbitrary platform amount, such as fee revenue | MLM Soft: plan properties flagged as volume or bonus can be "set by API request" | Verified (vendor docs); needs a demo | The only route found to a **platform fee revenue** base |

Sources: [Hybrid MLM](https://www.hybridmlm.io/investment-mlm-plan/), [Cloud MLM](https://cloudmlmsoftware.com/mlm-plan/investment-mlm-plan/), [ARM MLM](https://www.armmlm.com/tron-smart-contract-mlm-software/), [Epixel](https://www.epixelmlmsoftware.com/cryptocurrency-trading-mlm-software), [MLM Soft plan properties](https://help.mlmsoft.net/hc/en-us/articles/39249705385235-Plan-properties-configuration).

**A non-custodial source of fee revenue exists.** Privy Earn deposits a Member's funds into Morpho or Aave vaults and lets the platform take up to 50% (Morpho) or up to 100% (Aave) of the **yield only**; Members keep the principal and can withdraw at any time ([Privy revenue sharing](https://docs.privy.io/wallets/actions/earn/revenue-sharing), verified). A plan in which Commissions are a capped share of realised platform fee revenue, held for a period before payout, is structurally the lowest-risk option found. It is still a matter for legal counsel, because both choosing the yield source and paying Commissions linked to it raise questions in several jurisdictions (see the SEC's action concerning Celsius's "Earn Interest Program", [SEC 2023-133](https://www.sec.gov/newsroom/press-releases/2023-133)).

The client must confirm the base before the compensation plan can be configured or tested (section 11).
# MLM platform comparison, shortlist and exclusions

## Approach

Fifteen vendors were considered. They include white-label platforms marketed for crypto MLM, established enterprise direct-selling platforms, and headless or API-first commission engines. Bespoke development agencies and self-built engines were excluded by design. Vendors were assessed only from public sources; nothing was demonstrated or tested.

Because the Sponsor Tree is the only tree in AlphaWave's plan, binary and matrix placement trees are not required. The capabilities that matter are unilevel, generation, matching and rank logic; compression and caps; plan versioning with effective dates; simulation; Commission explanations; clawbacks; and a hard separation between Commission calculation and payout execution. **No vendor publicly documents all of these.**

## Eligibility conditions

A vendor had to meet all four conditions before scoring. Low price cannot compensate for a failed condition.

1. **No display-only yield.** Any "staking", "ROI" or "investment plan" module must be capable of being fully disabled; it is never used as a Yield Product.
2. **Payout can be separated from calculation**, so that payouts execute from AlphaWave's own wallet layer under its controls, not inside the MLM software.
3. **Documented integration surface**: a published API guide or reference, or vendor documentation of the event and data model.
4. **A maintained product from an identifiable vendor**, not a clone script or a one-off custom build.

## Vendors reviewed

| Vendor | Type | Crypto | Yield | Security evidence | Pricing | Outcome |
|---|---|---|---|---|---|---|
| MLM Soft | Headless SaaS engine | Token wallets as bookkeeping; payout adapter (claim) | None (by design) | None found | $499–$1,999/month + $10k–$30k setup (verified) | **Shortlist (lead)** |
| Exigo | Enterprise direct-selling platform | None | None | SOC 2 and PCI claimed; report not public | Quote | **Shortlist (alternative)** |
| Epixel | Integrated white-label | Payouts in BTC, ETH, USDT and others; "smart contract" commissions (claims) | "Investment plan" marketing only | ISO 27001 claims inconsistent (2013 and 2022 editions) | CA$1,381 and CA$6,914 tiers published; USD quote | **Shortlist (integrated option)** |
| Cloud MLM | Source-code licence, self-hosted | CoinPayments and Bitaps gateways named (custodial) | Calculated-return module (disable) | None | From $750 one-time + 18% yearly maintenance (verified) | **Shortlist (low-cost, exit)** |
| FlawlessMLM | Comp engine, SaaS or package | Claims only in third-party articles | None | None | $6,000 package or $1,499/month (verified) | Reserve |
| Infinite MLM | One-time licence | Claims (BTC, ETH, USDT, MetaMask) | "Staking & ROI dashboard" (display only) | ISO 27001:2013 (expired edition); SOC 2 asserted | $699 Basic (verified) | Reserve |
| Tapfiliate | Affiliate platform with multi-level API | None | None | Not found | Enterprise quote for API | Fallback for a very simple plan only |
| Post Affiliate Pro | Affiliate platform, up to 99 tiers (claim) | None | None | Not found | From $139/month | Fallback for a very simple plan only |
| Hybrid MLM | One-time licence + source | Gateways in top tier only | Commissions on "investment" and "ROI" | None | $599–$4,549 one-time | Excluded |
| ARM MLM | Scripts | "Forsage clone" smart contract | Entry-fee model | None | From $799 | Excluded |
| ByDesign | Enterprise | None | None | SOC 2 and ISO badges | Quote | Excluded (overlaps Exigo with less documentation) |
| InfoTrax | Enterprise, order-centric | None | None | Not found | Not found | Excluded |
| DirectScale | Enterprise API | None | None | Not found | Not found | Excluded (domain now redirects to Exigo; relationship unconfirmed) |
| Trinity (Firestorm) | Party-plan back office | None | None | Not found | Subscription | Excluded |
| Development agencies (Osiz, Suffescom and others) | Custom builds and clones | Claims | "Guaranteed ROI" language | None | Quote | Excluded (self-built) |

Sources: [MLM Soft pricing](https://www.mlmsoft.com/cloudplatform/subscription), [Exigo platform](https://www.exigo.com/exigo-platform/), [Epixel](https://www.epixelmlmsoftware.com/), [Epixel CAD pricing](https://www.epixelmlmsoftware.com/en-ca/pricing), [Cloud MLM pricing](https://cloudmlmsoftware.com/pricing/), [FlawlessMLM](https://flawlessmlm.com/en/mlm-marketing-software), [Infinite MLM pricing](https://infinitemlmsoftware.com/pricing), [Tapfiliate REST API](https://tapfiliate.com/docs/rest/), [Post Affiliate Pro pricing](https://www.postaffiliatepro.com/pricing/), [Hybrid MLM pricing](https://www.hybridmlm.io/pricing/).

Two findings apply across the market:

- **"Smart contract commission" claims are unsupported.** Epixel, Infinite MLM and Hybrid MLM advertise them, but no contract address, code repository or audit report was found for any of them.
- **Several ISO 27001 claims cannot be current.** All accredited ISO/IEC 27001:2013 certificates expired or were withdrawn on 31 October 2025 ([SGS transition notice](https://www.sgs.com/en/news/2024/05/iso-iec-27001-transition-what-you-should-know)). Every certification in this market should be treated as unverified until a current certificate or SOC 2 report is provided.

## Weighted scorecard

Scores run from 1 (weak or no evidence) to 5 (strong, documented). They are Cyclone's assessment of public evidence and will change after demonstrations.

| Criterion | Weight | MLM Soft | Exigo | Cloud MLM | Epixel | FlawlessMLM |
|---|--:|--:|--:|--:|--:|--:|
| Compensation features (plans, versioning, simulation, clawbacks, explanations) | 25% | 3 | 4 | 3 | 3 | 4 |
| Commission base flexibility (non-order events) | 15% | 5 | 2 | 3 | 3 | 2 |
| Integration (API, webhooks, headless, separation of payout) | 20% | 4 | 5 | 2 | 3 | 2 |
| Security and controls evidence | 15% | 1 | 4 | 1 | 2 | 1 |
| Time to deploy | 10% | 4 | 1 | 3 | 3 | 3 |
| Exit, data ownership and lock-in | 10% | 3 | 3 | 5 | 2 | 3 |
| Commercial transparency and cost | 5% | 5 | 1 | 5 | 3 | 4 |
| **Weighted score** | | **3.40** | **3.35** | **2.80** | **2.75** | **2.65** |

The top two are close for different reasons. MLM Soft wins on commission-base flexibility, speed and price; Exigo wins on controls evidence and integration maturity but is slower and quote-only. **The decisive item for MLM Soft is security due diligence**: no SOC 2 report, ISO certificate or penetration test summary was found. Both should be demonstrated side by side.

## Shortlist

**1. MLM Soft (lead candidate for the modular architecture).**

- Its REST API (API3) "covers all the functionality of the platform", with per-tenant Swagger documentation ([developers API](https://help.mlmsoft.net/hc/en-us/articles/39249636419475-Developers-API), verified in vendor documentation).
- Custom plan properties can be flagged as volume, bonus or rank and "set by API request", so a fee-revenue amount can be sent per Member per event and used as the commission base ([plan properties](https://help.mlmsoft.net/hc/en-us/articles/39249705385235-Plan-properties-configuration), verified in vendor documentation).
- Commissions post to a bookkeeping wallet; payout runs separately through a payment adapter. The vendor describes itself as "not a financial institution", which fits a Cyclone-owned ledger and wallet layer.
- Published pricing: $499, $999 and $1,999 per month for up to 300, 1,000 and 3,000 accounts with commercial activity in the last three months; Enterprise on quote; setup "usually varies between $10,000 to $30,000" (verified). The entry tier allows one wallet and one administrator, so Community or Network is the realistic starting point, and a large network will reach Enterprise pricing.
- Gaps: no security attestation; plan versioning, simulation and automatic clawbacks not documented; the API authenticates with a username and password rather than documented API keys.

**2. Exigo (enterprise alternative).**

- More than 200 APIs with public developer documentation ([developers.exigo.com](https://developers.exigo.com/), verified). SOC 2, PCI and GDPR compliance claimed (vendor claim; request the report). Mature payout integrations (PayQuicker, Worldpay, Hyperwallet, iPayout).
- No crypto capability, which matters less in the modular design because crypto sits outside the MLM core. Non-product bases would be modelled as synthetic orders or custom volumes.
- No public pricing; enterprise lead times make a 30-day configuration unlikely.

**3. Epixel (integrated white-label option).**

- The broadest crypto-MLM feature set among established vendors, with a public integration guide covering JWT authentication, webhooks and SSO ([api.epixelsoftware.help](https://api.epixelsoftware.help/), verified that the guide exists).
- Every crypto-execution claim needs a technical demonstration. Custody and key ownership are undocumented. Its "cryptocurrency investment plan" page uses language such as "investment will double or may triple", which must not be reused.

**4. Cloud MLM (low-cost, strongest exit position).**

- Full Laravel source code from $750 one-time, self-hostable, with 21 plan types (verified). Holding the source removes vendor lock-in but transfers security responsibility to Cyclone.
- Its named gateways (CoinPayments, Bitaps) are custodial, which conflicts with the Member-owned wallet design; they would be replaced by Cyclone's wallet integration. Its investment and "staking rewards" modules must be disabled.

**Reserve and fallbacks.** FlawlessMLM documents the strongest comp-engine features (what-if simulation, rule versioning, returns handling) and is the reserve headless engine. Tapfiliate and Post Affiliate Pro could support a deliberately simple plan (fixed percentages per level on fee revenue) but lack rank qualification, compression and versioning.

## Exclusions

| Vendor | Reason |
|---|---|
| Hybrid MLM | Its investment plan pays level Commissions on recruits' "investment" and "ROI", with returns funded from "company profits" generated with invested funds. This is a Ponzi-risk design pattern ([source](https://www.hybridmlm.io/investment-mlm-plan/)). |
| ARM MLM | Markets a "Forsage clone" entry-fee smart contract. The SEC charged Forsage's founders over an alleged pyramid and Ponzi scheme ([SEC 2022-134](https://www.sec.gov/newsroom/press-releases/2022-134)). |
| Infinite MLM | Display-only "Staking & ROI" dashboard; REST API documentation link returns an error; ISO claim refers to an expired edition. Held in reserve only as a like-for-like alternative to Cloud MLM. |
| ByDesign, InfoTrax | Order-centric enterprise platforms with no crypto evidence and less public documentation than Exigo. |
| DirectScale | Its domain redirected to Exigo on the research date; corporate status unconfirmed. Assess through Exigo if at all. |
| Trinity (Firestorm) | Party-plan back office without API documentation. |
| Development agencies | Custom builds and clone scripts, often marketed with "guaranteed ROI" language. They fall under the self-built exclusion. |
| CaptivateIQ, Everstage, QuotaPath and similar | Sales-compensation tools priced per payee and built around sales hierarchies, not Member genealogies. |
# CRM and customer operations

## Recommendation in brief

**For the first 30 days, use a dedicated SaaS helpdesk, not a CRM suite.** Customer operations at this stage are ticket handling: questions about Deposits and withdrawals, verification problems, Commission disputes, access and security. The helpdesk is the inbox; the Cyclone-built admin back office is where agents look things up and where operational actions happen. The two are linked by deep links and a read-only sidebar keyed on the Member ID.

Salesforce and Odoo, which AlphaWave has discussed previously, are assessed on equal terms. Both are better suited to a later CRM phase than to the 30-day helpdesk.

## Options compared

| | Zendesk Suite Professional | Freshdesk Omni Enterprise | Intercom Expert | Salesforce Service Cloud | Odoo (Enterprise apps) |
|---|---|---|---|---|---|
| List price, per agent per month (annual) | $115 | $119 | $132 | $195 (Core), $395 (Advanced) | Varies by billing country; quote |
| Custom objects (link to Member ID, wallet, KYC status) | Up to 30 | Yes | 15 on all plans (claim) | Yes, extensive | Yes (Studio) |
| SLAs and escalation | Yes | Yes | Expert plan | Yes (entitlements) | Yes |
| Approvals | Ticket approvals | Yes | Limited | Yes | Approvals app |
| Audit log | Enterprise tier (quote) | Included | Plan to confirm | Yes; Shield for field history | Yes |
| SSO | Yes | Yes | Expert plan | Yes | Yes |
| Telegram | Via integration | Marketplace app | **Native** (claim) | Custom build | Third-party modules (needs Odoo.sh or self-hosting) |
| Data residency | Free data-location add-on (US, EEA, UK, JP, AU) | Regional data centres | Regional hosting | Hyperforce regions | Hosting choice |
| Implementation effort (estimate) | 0.75–2.5 person-months | 0.75–2.5 | 0.75–2.5 | 3–5 | 2–3 |
| Fit for the 30-day milestone | **Good** | **Good** | Good if chat-led | Poor (effort) | Fair (effort, API on Custom plan only) |

Sources (prices seen 6 October 2026, verified on vendor pages): [Zendesk pricing](https://www.zendesk.com/pricing/), [Freshdesk Omni pricing](https://www.freshworks.com/freshdesk/omni/pricing/), [Intercom pricing](https://www.intercom.com/pricing), [Salesforce Service Cloud pricing](https://www.salesforce.com/service/pricing/), [Odoo editions](https://www.odoo.com/page/editions), [Odoo pricing](https://www.odoo.com/pricing).

Additional notes:

- **Odoo:** Helpdesk, Knowledge, Approvals and Studio are Enterprise-only, and the external API requires the Custom plan (verified). The USD price depends on the billing country: $13.40–$16.40 per user was shown for the research location, and a third party reports $49–$61 in the United States (not verified). Odoo also licenses every internal user, including back-office staff, whereas SaaS helpdesks license agents only. ISO 27001 and SOC 2 evidence could not be retrieved.
- **Salesforce:** the strongest case management, audit options and residency, at the highest licence and administration cost. Financial Services Cloud ($325–$700 per user) is not justified at this stage.
- **Intercom:** the only option with native Telegram, which suits community-led MLM support. Its AI agent costs $0.99 per resolved outcome on top of seats.

## System boundaries: CRM, helpdesk, back office and ledger

No CRM or helpdesk holds authoritative financial data.

| System | Source of truth for | Must not own or do | Agent access |
|---|---|---|---|
| Financial ledger | Balances, Deposits, withdrawals, Commission payouts, reconciliation state | Conversations; manual edits | None directly; only through back-office commands |
| MLM platform | Sponsor Tree, plan versions, Commission calculations and explanations | Payout execution; tickets | Read-only views via the back office |
| Verification provider | KYC status, evidence, sanctions results | Being copied into the helpdesk | Status only; evidence for the compliance role |
| Admin back office (Cyclone) | Operational actions: withdrawal hold, approval and retry; account freeze; address-change review; Commission adjustment requests; admin audit log | Messaging; SLA tracking | Role-scoped; any financial action needs a second approver |
| Helpdesk | Conversations, tickets, SLA timers, knowledge base, macros | Balances, wallet secrets, KYC documents, approval of funds movements, Sponsor Tree changes | All agents; cases store reference IDs only |
| CRM (later) | Relationship context: leaders, pipelines, segments, campaigns | Authoritative balances or Commission figures | Member-success staff |

Design rules:

1. The helpdesk stores **references, not values**. Member status is fetched live from the back office.
2. Helpdesk approvals are for non-financial decisions only. Every funds movement is approved in the back office with maker-checker control.
3. Agents never request private keys or seed phrases; macros, the knowledge base and inbound filters enforce this.
4. Cases are created automatically from the back office (stuck withdrawal, KYC rejection, Commission dispute) with a back-office reference.

## Minimum viable setup for 30 days

- **Tool:** one helpdesk chosen after a one-week scripted trial of Zendesk Suite Professional and Freshdesk Omni Enterprise, or Intercom if chat and Telegram will dominate.
- **People:** three to five agents for a controlled pilot, one support lead and a quarter of a helpdesk administrator's time. Finance and compliance approvers work in the back office.
- **Channels:** email and in-app chat. Telegram and WhatsApp only after verified accounts and a security review.
- **Case types:** Deposit, withdrawal, KYC, Commission dispute, Sponsor Tree or referral, account access, security or phishing.
- **Queues and SLAs:** security and withdrawal cases at the highest priority; separate queues for funds, verification and Commissions.
- **Knowledge base:** 20–40 articles reviewed by compliance, including wrong-network Deposits, network fees, verification steps, how and when Commissions are paid, and security warnings. No financial advice.
- **AI agent:** off, or restricted to approved knowledge with forced escalation on funds and verification topics.
- **Effort:** about 1.5 person-months (range 0.75–2.5) and two to three weeks elapsed once procurement is complete.

| Monthly licence cost (estimate from list prices) | 5 agents | 15 agents |
|---|--:|--:|
| Low (Freshdesk Omni Growth or Zendesk Suite Team) | $145–$275 | $435–$825 |
| Base (Zendesk Suite Professional or Freshdesk Omni Enterprise) | $575–$595 | $1,725–$1,785 |
| High (Zendesk Enterprise, or Salesforce Service Core with messaging) | about $1,350+ | about $4,050+ |

Usage-based AI and messaging fees are additional.

## Expansion path

- **Months 2–4: harden the helpdesk.** Add Telegram and WhatsApp, upgrade to the tier with audit logs and custom roles if not bought initially, add QA scoring and multilingual content, and enable a knowledge-restricted AI agent.
- **Months 4–9: add a CRM layer if the business case exists**, for leader relationship management, market onboarding pipelines and campaign segmentation. Options: the helpdesk vendor's own CRM (simplest); Odoo if AlphaWave also wants ERP functions (estimated 3–6 person-months); or Salesforce if scale and partner portals justify it (estimated 4–8 person-months plus 0.5–1 FTE administrator).
- **Later: consolidation.** If Salesforce or Odoo becomes the CRM, decide whether to migrate support into it; budget 2–4 person-months.
# Architecture options and fund flows

Three approaches were compared, as the brief requires. Every option shares one principle: **the Cyclone-owned platform ledger is the single financial source of truth.** The MLM software calculates Commissions, the wallet layer executes transfers, and the helpdesk and any CRM store references only.

## Option 1: Integrated white-label MLM platform

A single vendor (Epixel or Cloud MLM) provides the Member portal, compensation engine, internal e-wallet, crypto gateway and admin panel. Cyclone white-labels and customises it.

![Option 1: architecture and fund flow. The vendor's software holds balances and executes payouts; custody sits with an undocumented or custodial gateway.](figures/opt1-integrated){width=100%}

| Aspect | Assessment |
|---|---|
| Who controls assets | The vendor's gateway, or a custodial processor such as CoinPayments. Signing authority is not documented by any candidate. |
| Who provides the financial product | The vendor's "ROI/staking" module, which only calculates returns. **It must be disabled**, leaving no Yield Product. |
| Who processes withdrawals | The vendor's software, through its gateway. |
| Sources of truth | Identity, genealogy, balances, transactions and Commissions all sit inside the vendor database. |
| Buy, configure, build | Buy and configure the vendor package; customise the portal; build little. |
| Path to fiat | Through the vendor's gateway partners, which face the same MLM prohibitions as section 3.2. |
| Replaceability | Low. Balances, genealogy and payouts are tied to one vendor. Cloud MLM's source licence mitigates this but shifts security responsibility to Cyclone. |
| Complexity and timeline | Fastest visible portal (weeks), but the controls gap cannot be closed by configuration. |
| Material risks | Undocumented custody; unverified "smart contract" claims; expired or inconsistent ISO claims; vendor marketing that promises returns. |
| Conditions before real funds | Vendor proof of custody model, contract addresses and audits; current security attestation; replacement of the gateway with an AlphaWave-controlled wallet layer, at which point the option becomes Option 2. |

**Assessment: not recommended for real funds.** It is useful only as a fallback source of a Member portal or comp engine within Option 2.

## Option 2: Modular architecture (recommended)

AlphaWave buys a headless MLM core, a wallet layer, verification tooling and a helpdesk, and Cyclone builds the Member app, admin back office, ledger and integration layer.

![Option 2: high-level architecture. Cyclone builds the application layer and ledger; specialist components are purchased.](figures/opt2-architecture){width=100%}

![Option 2: fund flow. Member Deposits stay in Member-owned wallets; Commission payouts leave a separate operator treasury under multi-person approval; a later Yield Product keeps vault shares in the Member's wallet and pays the platform a share of yield only.](figures/opt2-fundflow){width=100%}

| Aspect | Assessment |
|---|---|
| Who controls assets | **Member Deposits:** the Member, through a Privy embedded wallet. If a narrowly scoped platform signer is added for vault deposits, the model is hybrid. **Treasury:** the operator, with quorum approval. |
| Who provides the financial product | Release 1: none with real funds. Later: a named lending or Staking protocol through the yield adapter (for example Privy Earn into Morpho or Aave vaults). |
| Who processes withdrawals | The Member signs withdrawals from their own wallet. Commission payouts are executed by the operator treasury after maker-checker approval. |
| Sources of truth | Identity status: verification provider (evidence) and platform identity service (decision record). Genealogy and Commission calculation: MLM core. Balances and transactions: platform ledger, reconciled to the chain. Commission payouts: ledger. |
| Buy | MLM core (MLM Soft or Exigo); wallet infrastructure (Privy); treasury tooling (Privy key quorum, Cobo or Fireblocks); KYC and screening (Sumsub or Didit, Chainalysis oracle); chain indexer or RPC provider; helpdesk. |
| Configure | Compensation plan; wallet policies; KYC tiers; helpdesk queues and SLAs. |
| Build | Member web app; admin back office; ledger and reconciliation; integration layer with idempotent event handling, webhook retries and feature gates; yield adapter interface. |
| Path to fiat | A provider-neutral funding interface allows an on-ramp to be added in Phase 2 once providers approve the model in writing. |
| Replaceability | High. Each component sits behind a Cyclone interface: the MLM engine receives events and returns Commission results; the wallet layer executes signed transfers; the yield adapter abstracts providers. QUANT can be added or removed without touching the core. Privy supports key export, giving Members an exit path. |
| Complexity and timeline | Highest integration effort of the three, but every piece is standard. About 9 person-months to the 30-day milestone and about 22 to a controlled pilot. |
| Material risks | MLM Soft security evidence; Privy's acceptance of the MLM model and Enterprise pricing; classification of the hybrid signer; gas costs for per-Member wallets; Commission clawbacks cannot be enforced on-chain once paid. |
| Conditions before real funds | See section 8.2. |

Key design rules for Option 2:

- **Separate the treasury from Member wallets.** Treasury signing keys never sit on the same server as any platform signer used with Member wallets.
- **Any platform signer is policy-restricted** to approved vault methods with amount caps and expiry, and can never transfer to a non-Member address. It is held in a hardware security module or key management service.
- **Deposits are detected twice**: by the wallet provider's webhooks and by an independent indexer, de-duplicated on chain, transaction hash and log index, with per-chain confirmation thresholds.
- **Commission calculation is separate from payout.** The MLM core emits payout instructions; the ledger records them; the treasury executes approved batches; clawbacks are applied before payout, which favours a hold period.
- **No Privy features that depend on Stripe or Bridge**: no fiat accounts, custodial wallets, fiat payouts or Stripe on-ramp.

## Option 3: QUANT integration in Phase 2

QUANT's trading engine is optional and is not part of the first release. If AlphaWave later offers algorithmic trading, the integration should keep the engine away from Members' core balances.

![Option 3: QUANT integration in Phase 2. Members opt in to a separate, capped trading account; QUANT receives only a trade-only key; Cyclone enforces limits and a kill switch.](figures/opt3-quant){width=100%}

| Aspect | Assessment |
|---|---|
| Who controls assets | The Member, through a separate trading account they opt into and fund with a capped amount. QUANT never holds withdrawal authority. |
| Who provides the financial product | QUANT's strategy, executed on Hyperliquid. This is a trading product with loss of principal possible, not Staking. |
| Who processes withdrawals | The Member, from their own Hyperliquid account back to their core wallet. |
| Sources of truth | Positions and P&L on Hyperliquid, mirrored in a separate sub-ledger. |
| Buy, configure, build | Integrate QUANT's engine; build the opt-in flow, risk monitor, limits and kill switch; configure Hyperliquid trade-only keys. |
| Path to fiat | As Option 2. |
| Replaceability | High if QUANT only sends orders through a trade-only key: another strategy provider can replace it. Hyperliquid documents agent (API) wallets that can place orders but not withdraw; this must be confirmed in due diligence (not verified in this research). |
| Complexity and timeline | Phase 2; depends on due diligence of QUANT's engine, security and operations. |
| Material risks | Strategy losses; venue manipulation (see HLP incidents); Hyperliquid's matching engine has no published audit; operator-selected trading products carry high regulatory sensitivity. |
| Conditions before real funds | Independent technical due diligence of QUANT; written risk limits and kill-switch tests; legal characterisation of the product; Member disclosures; QUANT never receives a signer over core Member wallets. |

**Release 1 restriction:** no Member funds are exposed to QUANT's engine, and no delegated signer is issued to QUANT.

## Wallet layer: Privy and a Stripe-independent alternative

Privy is the base case because it combines embedded wallets, smart accounts, a policy engine and a yield API in one product. Its ownership is the main concern: Stripe acquired Privy in June 2025, and Stripe and Bridge both prohibit MLM. Privy's own acceptable-use policy does not, and the design avoids every Privy feature that runs on Stripe or Bridge. There remains a risk that Privy's terms are later aligned with its parent's. Two independent alternatives were assessed.

| | Privy (base case) | Turnkey + Alchemy Smart Wallets (recommended alternative) | Dynamic (secondary alternative) |
|---|---|---|---|
| Ownership | Stripe (verified) | Both independent (Turnkey funding round May 2026, vendor claim) | Fireblocks, since October 2025 (verified) |
| Key model | Secure enclave plus 2-of-2 key split with the Member's login | Turnkey: keys in AWS Nitro enclaves; signing per policy-defined authenticators (vendor claim) | 2-of-2 MPC between Member device and vendor enclave (vendor claim) |
| Smart accounts | ERC-4337 and EIP-7702 (verified, docs) | Alchemy: EIP-7702 by default, Modular Account v2 (ERC-6900), audited by ChainLight and Quantstamp (vendor claim) | ERC-4337 (vendor claim); EIP-7702 not verified |
| Limits on platform actions | Off-chain policy engine in Privy's enclave (Enterprise) | Turnkey policies on amounts, recipients, contracts, chain, 7702 authorisations and Hyperliquid agent approval (verified, docs); **plus on-chain session keys** with spend, contract, function and expiry limits (verified, docs) | Delegated access share for the platform (vendor claim) |
| Built-in yield | Privy Earn: Morpho and Aave vaults with a fee on yield (verified) | None; integrate ERC-4626 vaults directly, or use Kiln DeFi vaults, which support integrator fees (verified) | None |
| Built-in on-ramps | Stripe (default), MoonPay, Meld | None core | Coinbase, Banxa (both prohibit MLM) |
| Published pricing | Free to $499/month; Enterprise quote needed (verified) | Turnkey $0.10 per signature, Pro $99/month at $0.05, Enterprise from $0.0015 (verified); Alchemy usage-based plus 8% gas fee, wallet pricing on quote | Free to $249/month, then $0.05 per user; bundled in Fireblocks Essentials at $999/month (verified) |
| SOC 2 | Type I/II (vendor claim) | Turnkey Type II (vendor claim); Alchemy not verified | Type II (vendor claim) |
| Main trade-off | Fastest integration; parent-company policy risk | More integration work; limits enforced on-chain, which is easier to evidence to counsel | Moves the parent-company question to Fireblocks, whose MLM stance is not verified |

Sources: [Privy pricing](https://www.privy.io/pricing), [Turnkey policies](https://docs.turnkey.com/concepts/policies/overview), [Turnkey pricing](https://www.turnkey.com/pricing), [Alchemy wallets](https://www.alchemy.com/docs/wallets), [Alchemy session keys](https://www.alchemy.com/docs/reference/wallet-apis-session-keys), [Kiln DeFi FAQ](https://docs.kiln.fi/v1/kiln-products/defi/kiln-defi-faq), [Fireblocks acquisition of Dynamic](https://www.fireblocks.com/blog/fireblocks-acquires-dynamic), [Dynamic pricing](https://www.dynamic.xyz/pricing).

Four further smart-account providers were assessed. None is owned by a payment company or an exchange, and none names MLM in its terms.

| Provider | What it is | Strengths for Helm | Limitations | Fit |
|---|---|---|---|---|
| **ZeroDev Kernel** (operated by Offchain Labs, the company behind Arbitrum) | Smart account (ERC-4337, ERC-7579, EIP-7702), on-chain permissions, bundler and paymaster | Platform session keys limited on-chain by contract, function, argument, expiry and rate; the private key never leaves the platform. HyperEVM listed. Earn API (beta) for Aave, Morpho and ERC-4626. Weighted multisig for a treasury. Kernel v3.x audit reports published. Plans $69 and $399/month; 8% gas premium | Offchain Labs may terminate if the relationship "would cause material harm to the reputation of Offchain" (verified). Earn is "an experimental product offered in beta" with no documented fee on yield (verified). No report found for Kernel v4 | **Co-equal alternative to Alchemy**, paired with Turnkey |
| **Openfort** | Full stack: embedded wallets, backend wallets, policy engine, paymaster, on-chain session keys | Closest to a Privy replacement on EVM networks; cheapest published entry pricing | No HyperEVM support; Hyperliquid signing is all-or-nothing; no SOC 2 evidence; its acceptable-use policy bans "Ponzi or pyramid schemes" and unlicensed "securities", the wording closest to excluding the model | Possible on EVM networks, after written clearance |
| **Para** (formerly Capsule) | Key signer (2-of-2 MPC with a share on the Member's device) | A device-held share gives the Member an independent factor | Not a smart account and no gas sponsorship; needs ZeroDev, Alchemy or Pimlico. Server-side paths are platform-controlled. HyperEVM not listed | Not preferred |
| **Pimlico** | Bundler and paymaster infrastructure only | Second paymaster for redundancy; HyperEVM listed | No EIP-7702 on HyperEVM; 10% sponsorship surcharge | Infrastructure complement |

Sources: [ZeroDev terms](https://zerodev.app/terms), [ZeroDev Kernel](https://github.com/zerodevapp/kernel), [ZeroDev session keys](https://docs.zerodev.app/smart-accounts/permissions/session-keys), [ZeroDev Earn](https://docs.zerodev.app/onramp/earn), [ZeroDev pricing](https://zerodev.app/pricing), [Openfort acceptable use](https://www.openfort.io/acceptable-use-policy), [Openfort HyperEVM](https://www.openfort.io/docs/recipes/hyperliquid/hyperevm), [Openfort pricing](https://www.openfort.io/pricing), [Para terms](https://www.getpara.com/terms-of-service), [Pimlico pricing](https://www.pimlico.io/pricing). Quotations were read through automated retrieval and should be re-checked before contracts are signed.

**Recommendation:**

- Keep Privy as the base case, conditional on its written acceptance of the business model.
- Carry **Turnkey as the signer with either Alchemy Smart Wallets or ZeroDev Kernel as the account layer** as the Stripe-independent alternative. ZeroDev is stronger on HyperEVM, DeFi tooling and published pricing; Alchemy's own terms have not yet been reviewed for comparable termination rights. Decide between them on the vendors' written answers.
- Run a **parallel technical spike of Turnkey with Alchemy Smart Wallets or ZeroDev Kernel in week 1**, covering wallet creation, a scoped session key limited to one vault and a cap, a Member-signed withdrawal and key export. Choose the wallet layer on the spike results and the vendors' written answers.
- Keep the wallet layer behind Cyclone's own interface so that a later switch does not touch the ledger, the MLM integration or the Member app. Member key export (offered by Privy and Turnkey, vendor claims) gives Members an exit path if a provider leaves.
- Coinbase Developer Platform (likely MLM prohibition), MetaMask Embedded Wallets (thinner policy documentation) and thirdweb (no SOC 2 evidence) were assessed and not recommended.

## Comparison

| Criterion | Option 1: Integrated | **Option 2: Modular** | Option 3: QUANT (Phase 2) |
|---|---|---|---|
| Custody clarity | Poor (undocumented) | **Good** (Member-owned wallets, separate treasury) | Good if trade-only keys are used |
| Genuine Yield Product path | None (display-only modules) | **Yes** (adapter to named protocols) | Trading returns, not yield |
| Controls evidence | Weak | **Mixed** (strong for Privy and verification vendors; MLM Soft unproven) | Unverified |
| Replaceability | Low | **High** | Medium |
| Effort | Lowest | **Highest** | Additional, later |
| Time to a credible real-funds pilot | Blocked by controls gaps | **10–14 weeks (estimate)** | After Option 2 is live |
| Recommendation | Not for real funds | **Primary** | Phase 2, conditional |

## Web-first delivery

**Web-first delivery is sufficient for the first release and native mobile should be deferred.** The PRD itself excludes a standalone mobile app from the first release. A responsive web app or progressive web app reaches Members on mobile browsers, and embedded wallets with passkey or email login work in the browser. Native apps add app-store review, which applies its own policies to crypto and MLM apps, plus a second release pipeline, with no gain for a controlled pilot. Mobile can follow once the product and legal position are stable.

## Recommendation: primary and fallback

- **Primary: Option 2 with MLM Soft, Privy and a quorum-approved treasury.** It is the only option that delivers clear custody boundaries, a genuine route to a Yield Product, replaceable components and a ledger AlphaWave controls.
- **Fallback: Option 2 with substitutions**, triggered by specific failures:
  - if Privy declines the business, its Enterprise terms are unacceptable, or Stripe ownership is judged too great a policy risk: the Stripe-independent wallet stack of Turnkey with Alchemy Smart Wallets or ZeroDev Kernel (section 6.4), with Fireblocks, Cobo or a Safe multisig for the treasury;
  - if MLM Soft fails its demonstration or security due diligence: Exigo (stronger controls evidence, slower) or Epixel (integrated, crypto features to be proven);
  - if counsel or the business prefers an omnibus model: Fireblocks, Cobo or a qualified custodian such as BitGo, accepting that the operator becomes custodian of Member assets with the licensing implications that follow.

The trade-off is effort for control: Option 2 needs more integration work than Option 1, in exchange for custody, data and vendor independence that Option 1 cannot provide.
# Cost, effort and 12-month operating estimates

## Basis of estimates

- **Currency and date:** USD, prices seen on 6 October 2026. Prices exclude tax.
- **Scale:** a controlled pilot with up to 3,000 commission-active Members, under 10,000 monthly active wallet users, about 1,000 new Members per month and five helpdesk agents.
- **Scope:** Option 2 (modular). Release 1 has no fiat on-ramp, no custom smart contracts and no live Yield Product.
- **Labour:** Cyclone's day rates are contracted, so effort is shown in **person-months** only. Monetary figures cover external software and services.
- **Excluded:** legal counsel fees, licensing applications, banking costs, entity set-up, marketing, and Member-funded network fees.
- **Evidence labels:** **V** = verified public price; **Q** = vendor quotation required; **E** = Cyclone consultant estimate. Where a public price exists but the required features sit in a quote-only tier, the figure is marked E.

## External software and services

| Component | Low | Base | High | Basis |
|---|--:|--:|--:|---|
| MLM core: MLM Soft subscription (monthly) | $999 | $1,999 | $4,000 | V for Community and Network tiers; high case is E for Enterprise (Q) |
| MLM core: setup and customisation (one-time) | $10,000 | $20,000 | $30,000 | V ("usually varies between $10,000 to $30,000") |
| Member wallets: Privy (monthly) | $499 | $1,500 | $3,000 | E. Public tiers are $299–$499/month, but the policy engine, key quorums and production webhooks are Enterprise (Q) |
| Operator treasury tooling (monthly) | $0 | $299 | $999 | V: Privy key quorum (within Privy Enterprise), Cobo Starter, Fireblocks Essentials |
| KYC and AML screening, scenario B (monthly) | $250 | $1,200 | $2,000 | E from V per-check prices (Didit, Sumsub, Veriff) |
| Wallet screening and transaction monitoring (monthly) | $0 | $100 | $1,500 | V for the free Chainalysis oracle and Didit per-check prices; commercial KYT is Q |
| Helpdesk, 5 agents (monthly) | $145 | $585 | $1,350 | V list prices; high case includes Q items |
| Hosting, RPC/indexer, monitoring and logging (monthly) | $800 | $2,000 | $4,000 | E |
| Gas sponsorship for Member wallet actions (monthly) | $200 | $500 | $1,000 | E; pass-through, volume-dependent |
| Fiat on-ramp (Release 1) | $0 | $0 | $0 | Deferred to Phase 2; an aggregator such as Onramper costs $199–$599/month (V) |
| Penetration test, pre-launch (one-time) | $12,000 | $25,000 | $40,000 | E (no public rate cards; an automated test from $3,500 is V but not sufficient alone) |
| Wallet and key-management review (one-time) | $10,000 | $20,000 | $30,000 | E |
| Smart contract audit | $0 | $0 | $0 | Not needed while Release 1 deploys no custom contracts; $15,000–$100,000+ if it does (E) |

Sources: [MLM Soft](https://www.mlmsoft.com/cloudplatform/subscription), [Privy](https://www.privy.io/pricing), [Cobo](https://www.cobo.com/pricing), [Fireblocks](https://www.fireblocks.com/pricing), [Sumsub](https://sumsub.com/pricing/), [Zendesk](https://www.zendesk.com/pricing/), [Freshdesk](https://www.freshworks.com/freshdesk/omni/pricing/), [Cobalt](https://www.cobalt.io/pricing).

## One-time implementation costs (external)

| | Low | Base | High |
|---|--:|--:|--:|
| MLM setup and customisation | $10,000 | $20,000 | $30,000 |
| Penetration test | $12,000 | $25,000 | $40,000 |
| Wallet and key-management review | $10,000 | $20,000 | $30,000 |
| **Total one-time** | **$32,000** | **$65,000** | **$100,000** |

## Monthly operating costs (external)

| | Low | Base | High |
|---|--:|--:|--:|
| MLM subscription | $999 | $1,999 | $4,000 |
| Wallet infrastructure | $499 | $1,500 | $3,000 |
| Treasury tooling | $0 | $299 | $999 |
| KYC, AML and wallet screening | $250 | $1,300 | $3,500 |
| Helpdesk | $145 | $585 | $1,350 |
| Hosting, RPC, monitoring | $800 | $2,000 | $4,000 |
| Gas sponsorship | $200 | $500 | $1,000 |
| **Total monthly** | **≈ $2,900** | **≈ $8,200** | **≈ $17,800** |

## Indicative 12-month total cost of ownership (external)

| | Low | Base | High |
|---|--:|--:|--:|
| One-time | $32,000 | $65,000 | $100,000 |
| 12 × monthly | $34,700 | $98,200 | $214,200 |
| **Indicative 12-month total** | **≈ $67,000** | **≈ $163,000** | **≈ $314,000** |

What would move these figures most:

- **Network size.** MLM Soft's Network tier covers up to 3,000 commission-active accounts; a larger active base moves to Enterprise pricing (Q).
- **Wallet volume.** Privy's pay-as-you-go pricing above 10,000 monthly active users is $2,000 plus $0.05 per user (V); Enterprise pricing is negotiated.
- **Wallet vendor.** The Turnkey and Alchemy alternative is priced per signature and per compute unit (Turnkey $0.05 per signature on Pro, V), so its cost scales with transaction volume rather than monthly active users; at pilot scale it is expected to fall within the Privy range above (E).
- **KYC scenario.** Scenario A raises verification spend; scenario C lowers it but closes the fiat route and raises other risks.
- **Commercial transaction monitoring.** Chainalysis, TRM and Elliptic publish no prices; third-party sources suggest five-figure annual contracts (not verified).
- **A live Yield Product** adds audit review of the chosen vaults and any fee wrapper, and possibly a smart contract audit.

## Effort by workstream (person-months)

Engineering effort is not the same as elapsed time. Vendor procurement, provider approvals and legal review run in parallel and cannot be shortened by adding staff.

| Workstream | 30-day milestone | Cumulative to controlled pilot |
|---|--:|--:|
| Delivery management and solution architecture | 1.0 | 2.5 |
| MLM core integration and compensation plan configuration | 1.0 | 2.5 |
| Wallet and treasury integration (Privy, policies, quorum) | 0.75 | 1.5 |
| Ledger, Deposit detection and reconciliation | 1.0 | 3.0 |
| Member web app | 1.5 | 3.5 |
| Admin back office (roles, approvals, audit, case links) | 1.0 | 2.5 |
| KYC and screening integration | 0.5 | 1.0 |
| Helpdesk configuration and integration | 0.5 | 1.25 |
| QA, Commission test pack and test automation | 1.0 | 2.5 |
| DevOps, security engineering and monitoring | 0.75 | 2.0 |
| **Total** | **9.0** | **22.25** |

All figures are consultant estimates (E). The 30-day figure assumes the client's decisions in section 11 are made in week 1; otherwise configuration work on the compensation plan slips.

## Minimum delivery team

| Role | FTE | Responsibility |
|---|--:|---|
| Delivery lead | 1.0 | Plan, vendor coordination, decision log, readiness reviews |
| Solution architect and blockchain lead | 1.0 | Architecture, wallet and treasury design, custody controls |
| Backend engineers | 2.0 | Ledger, reconciliation, MLM and KYC integrations |
| Wallet and blockchain engineer | 1.0 | Privy integration, policies, indexer, gas sponsorship |
| Frontend engineers | 2.0 | Member web app and admin back office |
| QA engineer | 1.0 | Commission test pack, end-to-end and negative tests |
| DevOps and security engineer | 0.75 | Environments, secrets, monitoring, incident tooling |
| **Cyclone total** | **≈ 8.75** | |
| Client: product owner | 0.5 | Product mechanics, Member terms, compensation plan decisions |
| Client: compliance owner | 0.5 | KYC scenario, policies, counsel liaison |
| Client: operations and support lead | 0.5–1.0 | Support processes, knowledge base review, finance approvals |
| External: legal counsel | As engaged | Questions in section 10 |

## Dependencies and critical path

The critical path to accepting real funds runs through decisions and approvals rather than engineering:

1. **Client decisions** (week 1): commission base, target markets, KYC scenario, treasury approvers.
2. **Legal characterisation** of the compensation plan, custody model and KYC thresholds (estimated four to six weeks from engagement; outside Cyclone's control).
3. **Vendor acceptance and contracts**: Privy's written acceptance of the MLM model and Enterprise terms; MLM Soft contract and security evidence; KYC vendor onboarding (each runs its own business review).
4. **Compensation plan specification** with complete rates and the confirmed base, then configuration and testing against the Commission test pack.
5. **Ledger reconciliation proven** on test networks, then on a small real-funds rehearsal using operator funds.
6. **Independent penetration test and wallet review**, with high-severity findings fixed.
7. **Go/no-go review** against the readiness criteria in section 8.

Items 2 and 3 typically determine the launch date. Engineering can complete the 30-day milestone in parallel, but real funds wait for both.
# Proposed 30-day scope and readiness criteria

## Milestone definition

A real-funds launch within 30 days is not supported (section 1). The 30-day milestone is therefore defined as:

> **An end-to-end system running on test networks, with every money path, approval and support process working, plus vendor contracts and legal questions in progress, so that a controlled real-funds pilot can start as soon as the legal and vendor gates clear.**

Onboarding-only production (signup, sponsor attribution, referral links and wallet creation, with no Deposits) can be opened at day 30 if counsel agrees that pre-registration raises no issue in the target markets.

## Weekly plan

| Week | Outcomes | Owners | Dependencies | Acceptance criteria |
|---|---|---|---|---|
| 1 – Decide and procure | Decision log covering commission base, markets, KYC scenario and treasury approvers. Scripted demos of MLM Soft and Exigo. Parallel wallet spikes on Privy and on Turnkey with Alchemy Smart Wallets or ZeroDev Kernel. Written MLM-acceptance requests to Privy, Turnkey, Alchemy, ZeroDev (Offchain Labs), MLM Soft and the KYC vendor. Counsel engaged with the question list. Environments and repositories set up. | Client product owner; Cyclone delivery lead and architect | Client availability; vendor demo slots | Decisions signed off; demo scorecards and wallet spike results completed; vendor questionnaires sent; counsel engagement confirmed |
| 2 – Foundations | Member signup, sponsor attribution and referral links. Privy wallet creation on test networks. MLM core sandbox with a placeholder plan. Ledger schema and event model. Admin roles and audit log skeleton. Helpdesk tenant and case types. | Cyclone engineering | MLM and Privy sandbox access | A test Member can register under a sponsor, receive a wallet and appear in the Sponsor Tree; all admin actions are logged |
| 3 – Money flows on test networks | Deposit detection with independent reconciliation. Member-signed withdrawals. Commission calculation from test events. Treasury payouts with quorum approval. Sanctions screening on every address. KYC tiers in sandbox. | Cyclone engineering; client compliance owner (tier thresholds) | Placeholder thresholds agreed; KYC sandbox | Deposits credited exactly once, including under duplicate and delayed webhooks; payouts need two approvers; a sanctioned test address is blocked |
| 4 – Harden and review | Commission test pack (unilevel levels, matching, rank qualification, compression, caps, plan version change, reversal). Incident and suspension runbooks. Kill switches. Helpdesk integration and knowledge base drafts. Security self-assessment and pen test booked. Readiness review. | Cyclone QA and DevOps; client operations lead | Complete placeholder plan; knowledge base review | Test pack passes; runbooks rehearsed in a tabletop exercise; readiness report issued with open gates listed |

## Requirements before accepting real funds

All of the following must be met. None can be waived to meet a date.

1. **Defined product mechanics and Member terms**, including the commission base and complete plan rates, approved by counsel.
2. **Legal confirmation** for the launch jurisdictions covering custody classification, KYC thresholds, Travel Rule applicability and the compensation plan.
3. **Written vendor acceptance** of the MLM model from the wallet, MLM and verification vendors.
4. **Custody and signing controls** in force: separate treasury with quorum approval; any platform signer policy-restricted and held in an HSM or KMS; key rotation and recovery tested.
5. **Deposits and withdrawals** proven on test networks and in a small real-funds rehearsal using operator funds.
6. **Ledger and daily reconciliation** to on-chain balances, with breaks investigated before payouts.
7. **Verification and screening** live for the agreed scenario, with sanctions screening on every address.
8. **Commission calculations tested** against the agreed test pack, with explanations exportable per Member.
9. **Administrative permissions and auditability**: role-based access, maker-checker approvals for all funds movements, immutable audit log.
10. **Incident response**: service suspension and withdraw-only modes, failed and stuck transaction handling, Member communication templates.
11. **Independent penetration test and wallet review** completed, with high-severity findings fixed.

## Controlled pilot features

- Crypto Deposits in the assets and networks supported by the chosen components; withdrawals to the Member's own address.
- Sponsor Tree and Commission calculation on the confirmed base, with payouts in batches after a hold period.
- Tiered KYC and sanctions screening.
- Admin back office with approvals; helpdesk with funds, verification and Commission queues.
- Exposure limits: an invitation-only Member list, caps per Member and in total, and the ability to suspend.

## Later phases

- Live Yield Product through the adapter, after legal confirmation and vault due diligence.
- Fiat on-ramp, after written provider approvals.
- QUANT trading integration (Option 3), after due diligence.
- CRM layer, Telegram and WhatsApp support channels, AI support restricted to approved knowledge.
- Native mobile apps.
- PRD roadmap items with high regulatory sensitivity (binary options, B-Books, debit cards, fund products), each subject to separate legal review.

## Readiness assessment

Expected status at day 30 if week-1 decisions are made on time:

| Criterion | Expected status at day 30 | Blocking for real funds? |
|---|---|---|
| Product mechanics and Member terms | Commission base decided; terms drafted, not approved | Yes, until counsel approves |
| Legal confirmation | Questions with counsel; answers pending | **Yes** |
| Custody and signing controls | Designed and working on test networks | Yes, until reviewed |
| Deposits and withdrawals | Working on test networks | Yes, until the real-funds rehearsal |
| Ledger and reconciliation | Working on test networks | Yes, until the real-funds rehearsal |
| Verification and screening | Sandbox; thresholds provisional | Yes, until thresholds are approved |
| Commission calculations | Test pack passing against the placeholder plan | Yes, until rerun on the approved plan |
| Admin permissions and auditability | Built and tested | No |
| Incident response and suspension | Runbooks drafted and rehearsed | No, once rehearsed |
| Security testing | Scheduled | **Yes** |
| Vendor acceptance | Requested | **Yes** |

**Conclusion:** at day 30 the system should be ready to demonstrate end to end. It should not be described as production-ready for real funds until every blocking item above is closed.
# Risks and due diligence requirements

## Risk register

Likelihood (L) and impact (I) are rated High, Medium or Low by Cyclone for the recommended Option 2.

| # | Risk | L | I | Mitigation |
|---|---|:-:|:-:|---|
| R1 | Counsel finds the compensation plan or commission base unlawful in a target market | M | H | Decide the base early; prefer Commissions funded from realised fee revenue with caps and hold periods; no Commissions on Deposits until counsel confirms |
| R2 | A vendor declines or later terminates the business because of the MLM model (wallet, KYC, payments) | H | H | Full disclosure during onboarding; written acceptance before build depends on it; replaceable components behind Cyclone interfaces; fallback vendors identified |
| R3 | The hybrid wallet model (platform signer) is classified as custody or money transmission | M | H | Release 1 without a platform signer on Member wallets; add a scoped signer only after counsel's view; key quorum with a Member signature as an alternative |
| R4 | Compromise of treasury or platform signer keys | L | H | Quorum approval; HSM or KMS; strict policies; separation of keys; withdrawal limits; wallet review before launch |
| R5 | MLM Soft fails security due diligence or cannot support the plan | M | M | Side-by-side demo with Exigo; scripted test pack; request SOC 2, ISO 27001:2022 or penetration test evidence before contract |
| R6 | Commission errors or disputes (rates, compression, reversals) | M | H | Complete specification; test pack; per-Member explanations; hold period before payout; maker-checker on adjustments |
| R7 | Commission clawback impossible once paid on-chain | H | M | Pay after a hold period; net future Commissions against reversals; state this in Member terms |
| R8 | Fraud through fake Members (self-sponsoring, sybil accounts) | H | M | Tiered KYC before payouts; device and behaviour signals; caps; Commission eligibility rules |
| R9 | Reconciliation breaks between ledger, wallets and chain | M | H | Two independent Deposit signals; idempotency on transaction identifiers; daily reconciliation with payouts blocked on unresolved breaks |
| R10 | Yield protocol loss (smart contract, oracle, curator, liquidity) when the Yield Product goes live | M | H | Vault allow-list with curator criteria; exposure caps; kill switch; Member disclosures by category; no projected returns shown |
| R11 | Members misunderstand returns or rely on promotional earnings claims | H | H | Compliance-reviewed content; no return promises; earnings disclosures; control of Member-created marketing |
| R12 | Gas costs for per-Member wallets exceed budget | M | L | Choose low-fee networks; batch payouts; sponsorship limits |
| R13 | Delays in legal review or vendor onboarding push the pilot beyond plan | H | M | Start both in week 1; treat as critical path; keep engineering milestones independent of them |
| R14 | Dependence on Privy, which is owned by Stripe: its terms could be aligned with Stripe's MLM prohibition | M | H | Use no Stripe or Bridge features; confirm acceptance in writing; wallet layer behind a Cyclone interface; Member key export; Turnkey with Alchemy Smart Wallets or ZeroDev Kernel tested in parallel as the independent alternative |
| R15 | QUANT integration exposes Member funds to trading losses | L (Release 1) | H | No QUANT access in Release 1; Phase 2 only through opt-in, capped, trade-only accounts after due diligence |

## Due diligence requirements

**MLM vendor (before contract):**

- Current SOC 2 Type II report or ISO/IEC 27001:2022 certificate, with scope and period; latest penetration test summary and remediation.
- Scripted demonstration of the Helm test pack, including a non-order commission base sent by API, plan versioning, simulation, reversal and per-Member explanations.
- Data export of genealogy, plan history and Commission history; exit terms.
- API authentication, rate limits, versioning, webhook signing and retries; sandbox access.

**Wallet and treasury vendors:**

- Written acceptance of the MLM model and confirmation that core wallet features need no Stripe or Bridge account (Privy).
- Enterprise pricing; SOC 2 report; policy-engine capabilities; key export and migration path.
- Audit status of the Earn fee wrapper and any contracts the platform would rely on.

**Verification vendor:** acceptance of the model; certifications; data residency; record retention; Sumsub's disclosed 2024 support-system incident ([Sumsub statement](https://sumsub.com/newsroom/security-incident-update/)).

**Yield providers (later phase):** audit history, incident history and remediation, curator risk framework, liquidity profile, and custody implications of the integration pattern.

**QUANT (Phase 2):** independent technical review of the engine, custody model, security controls, operational readiness, historical performance methodology and incident history. QUANT's MVP capabilities have not been verified in this research.
# Questions for vendors, QUANT and legal counsel

## Vendors

**All shortlisted MLM vendors (MLM Soft, Exigo, Epixel, Cloud MLM)**

1. Will you contract with a platform that distributes a crypto product through an MLM network, with Commissions paid in crypto?
2. Provide your current SOC 2 Type II report or ISO/IEC 27001:2022 certificate, and the latest penetration test summary with remediation status.
3. Demonstrate a Sponsor-Tree-only plan with unilevel levels, a matching bonus, rank qualification, dynamic compression, per-Member caps, a plan version effective from a future date, simulation of that version, recalculation after a reversed event, and a per-Commission explanation export.
4. Can a commissionable event carry an arbitrary amount and type that is not a product order, such as a fee-revenue event? How is it submitted (endpoint, idempotency key) and reversed?
5. Can payouts be disabled so that the platform only emits approved payout instructions to an external wallet system?
6. Describe API authentication, rate limits, versioning and deprecation, webhook signing and retries, and sandbox availability.
7. Describe administrator MFA, maker-checker approvals, immutable audit logs and log export.
8. What data can be exported (genealogy, ledger, Commission history), in what format, and on what exit terms?
9. What are hosting regions, data residency, SLA, backup objectives and support hours?
10. What is a realistic lead time for the plan above, and can you provide two references of similar scale?

**Vendor-specific**

11. MLM Soft: provide access to the API3 reference before contract; describe the webhook catalogue; confirm whether API keys are supported instead of username and password; describe versioning, simulation and clawback support; give Enterprise pricing beyond 3,000 active accounts.
12. Exigo: confirm support for non-order commissionable volume and payout to external crypto rails; give pricing and lead time; clarify the relationship with DirectScale.
13. Epixel: provide contract addresses, repositories and audits for "multi-chain smart contract" commission processing; state who holds signing keys; clarify the ISO 27001 edition; provide USD pricing.
14. Cloud MLM: confirm the investment and "staking rewards" modules can be fully removed; state what security review the codebase has had and the patch cadence.

**Privy**

15. Will Privy onboard this business model, and do embedded wallets, policies, key quorums and Earn require any Stripe or Bridge account?
16. Which features in our design require the Enterprise plan, and at what price?
17. Has the Earn fee wrapper been audited, and by whom? What are its upgrade and admin controls?
18. How does key export work for Members if the platform leaves Privy?

**Turnkey, Alchemy and ZeroDev (Stripe-independent wallet alternative)**

19. Will you onboard this business model? Turnkey: which plan covers delegated API keys, policies and gas sponsorship, and can policies restrict a platform key to deposits into named ERC-4626 vaults with amount caps? Alchemy: confirm Turnkey as a supported signer for Smart Wallets, the pricing for wallet APIs, and SOC 2 status. ZeroDev (Offchain Labs): confirm acceptance given the reputational-harm termination right, provide the Kernel v4 audit report, and confirm paymaster coverage on HyperEVM.

**Treasury vendors (Cobo, Fireblocks)**

20. Will you onboard this business model? Which plan covers quorum approvals and batch payouts on the networks we need?

**Verification vendors (Sumsub, Didit)**

21. Will you onboard this business model? Which plan covers tiered verification, wallet screening and Travel Rule? What are data residency and retention options?

**Helpdesk vendors**

22. Zendesk: Enterprise pricing for audit log and custom roles. Freshdesk: whether custom objects are included in Pro. Intercom: which plan includes the audit log.

**On-ramp providers (Phase 2)**

23. After full disclosure of the model, will you approve the platform in writing? Who is merchant of record? Do aggregators route the platform through each provider's own business review?

## QUANT (Phase 2)

1. What exactly does the MVP include today, and which parts run in production?
2. What custody model does the MVP use, and who can sign for user funds?
3. Can the engine operate solely through trade-only keys on Member-owned Hyperliquid accounts, with no withdrawal authority?
4. What risk limits, kill switches and monitoring exist? Who can override them?
5. What security assessments, penetration tests and audits have been performed, with dates and scope?
6. How is historical performance measured and presented, and has it been independently verified?
7. What incidents have occurred, and how were they handled?
8. What is the relationship between QUANT and the "Quantitative Engine" and "TA Capital Trade Deck" referenced in the PRD?

## Legal counsel

**Scope and structure**

1. In which jurisdictions will AlphaWave be established, and in which will Members be recruited or served? Which regimes apply as a result?
2. Which legal entity provides each service (wallet, Deposits, Yield Product, Commission calculation, Commission payout)? Is Cyclone, as integrator and operator of the application layer, exposed to any of these classifications?

**Custody and licensing**

3. Under the proposed wallet model, with or without a policy-restricted platform signer, does AlphaWave have "control" over Member assets?
4. Does holding Commissions in an operator treasury before payout amount to safekeeping or transfer on behalf of Members?
5. Does a Yield Product that routes Deposits to a third-party protocol make AlphaWave a virtual asset service provider, an investment manager, or neither?

**KYC and AML**

6. Is any no-KYC tier permissible, and up to what cumulative amounts and for which actions?
7. What information must be collected for withdrawals and payouts to self-hosted wallets? Does the Travel Rule apply?
8. What sanctions screening is required for wallet addresses and Members, against which lists and how often?
9. Which record-retention, suspicious-activity reporting and compliance-officer obligations apply?
10. Is identity needed for tax reporting on Commissions, independently of AML?

**MLM, securities and consumer protection**

11. Which commission bases are lawful under pyramid-scheme laws in each target jurisdiction: platform fee revenue, Deposit volume, yield amounts?
12. Is the Yield Product, under each mechanism considered (Staking, lending, trading vault, operator-managed), a security, investment contract, collective investment scheme or deposit-taking activity? The SEC and CFTC issued a joint interpretation on crypto assets, including protocol staking, on 17 March 2026 ([SEC 2026-30](https://www.sec.gov/newsroom/press-releases/2026-30-sec-clarifies-application-federal-securities-laws-crypto-assets)); how do it and local equivalents apply?
13. Do Members who recruit and earn Commissions need any licence or registration?
14. What earnings disclosures, risk warnings and marketing controls are required, including over Member-created content?

**Vendors and banking**

15. Can AlphaWave rely on a vendor's KYC (for example an on-ramp's) for its own obligations?
16. Are any vendor terms incompatible with the business model as structured?

Reference sources for counsel (examples, not an assessment of applicability): [FATF 2021 guidance on virtual assets](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html), [EU MiCA](https://eur-lex.europa.eu/eli/reg/2023/1114/oj), [EU Transfer of Funds Regulation](https://eur-lex.europa.eu/eli/reg/2023/1113/oj), [FinCEN FIN-2019-G001](https://www.fincen.gov/sites/default/files/2019-05/FinCEN%20Guidance%20CVC%20FINAL%20508.pdf), [FTC guidance on multi-level marketing](https://www.ftc.gov/business-guidance/resources/business-guidance-concerning-multi-level-marketing), [FTC Business Opportunity Rule](https://www.ftc.gov/legal-library/browse/rules/business-opportunity-rule), [Investor.gov on pyramid schemes](https://www.investor.gov/introduction-investing/investing-basics/glossary/pyramid-schemes).
# Business decisions required from the Client

The decisions below materially change the recommendation, cost or timeline. The first five are needed in week 1.

| # | Decision | Why it matters | Cyclone's recommendation |
|---|---|---|---|
| D1 | **Commission base**: what Commissions are calculated on, now that subscriptions are superseded | Determines MLM configuration, legal risk and whether a vendor can support it out of the box | A capped share of realised platform fee revenue, paid after a hold period; no Commissions on Deposits until counsel confirms |
| D2 | **Complete compensation plan**: rates for every level, cap treatment, rank definitions ("active", "verified referral", "certification", "team sales", "plan tier") | Commissions cannot be configured or tested without them | Provide a complete, versioned specification with worked examples |
| D3 | **Target markets and operating entity** | Drives every legal question, KYC thresholds, data residency and vendor eligibility | Name the launch markets for the pilot, even provisionally |
| D4 | **KYC scenario** | Affects onboarding, payouts, vendor access and cost | Scenario B (tiered), with thresholds set by counsel |
| D5 | **Treasury approvers and limits** | Required for payout controls | At least two approvers from different functions, plus daily limits |
| D6 | **Yield Product definition**: mechanism, asset, provider category, fees, disclosures | Determines custody pattern and legal characterisation | Over-collateralised stablecoin lending through Member-held vault shares; launch after legal confirmation |
| D7 | **Fiat timing** | On-ramps prohibit MLM; approval is uncertain | Crypto-only Release 1; pursue written approvals in parallel for Phase 2 |
| D8 | **Assets and networks for Release 1** | Affects gas costs, indexing and vendor fit | Limit to what the selected components support natively; prefer low-fee networks |
| D9 | **Pilot size and exposure caps** | Bounds risk during the controlled pilot | Invitation-only list with per-Member and total caps |
| D10 | **Wallet vendor**: Privy, or the Stripe-independent stack (Turnkey with Alchemy Smart Wallets or ZeroDev Kernel) | Determines integration effort and exposure to a parent company's payment policies | Decide after the week-1 spikes and the vendors' written answers on the MLM model |
| D11 | **MLM vendor selection** after demonstrations | Locks in integration path | Demonstrate MLM Soft and Exigo side by side; decide on test pack results and security evidence |
| D12 | **QUANT's role** | Determines whether Option 3 is planned | Phase 2 only, after due diligence, through trade-only access |
| D13 | **Support channels** | Telegram and WhatsApp add security review and set-up time | Email and in-app chat first; community channels in Phase 2 |
| D14 | **Treatment of high-sensitivity roadmap items** (binary options, B-Books, debit cards, fund products) | Each carries separate regulatory exposure | Remove from the near-term roadmap pending separate legal review |
# Sources, research date and evidence limitations

## Research date and method

- **Research date:** 6 October 2026. Prices and terms were read on that date and may have changed since.
- **Method:** desk research using vendor websites, documentation, pricing pages, legal terms, protocol documentation, governance forums and regulator publications. No vendor was contacted, no account was opened, no demonstration was requested and no client information was shared.
- **Evidence labels used in this report:**
  - **Verified:** confirmed in a primary source on the research date (vendor documentation or terms, published price, protocol documentation, regulator text).
  - **Vendor claim:** stated by the vendor about itself, for example a certification badge, without the underlying report or certificate being inspected.
  - **Working assumption or consultant estimate:** Cyclone's judgment, stated as such.
  - **Not verified:** no primary evidence found, or the source could not be read.

## Evidence limitations

- **Certifications are unverified.** No vendor publishes its SOC 2 report or current ISO certificate. All such statements are vendor claims until the documents are reviewed under NDA.
- **No product was tested.** Crypto execution, "smart contract" and custody claims could not be tested without demonstrations.
- **Search coverage.** The research tool's web-search allowance was exhausted partway through. Later checks used direct retrieval of official pages only, so vendors discoverable only through search may have been missed. Spiff, Xactly, Varicent and Kobie were not reviewed.
- **Blocked pages.** Some pages blocked automated access (for example parts of Coinbase, FATF, Persona, Odoo and the Rocket Pool audit files). Where an archived copy of an official document was used, this is stated.
- **Press-only incidents.** Hyperliquid HLP losses and the Stream/xUSD event rest on press reports, not primary disclosures.
- **Jurisdiction.** Regulatory sources are examples from FATF, the EU and the US. Other jurisdictions may differ materially. Nothing in this report is legal advice.
- **Prices change frequently.** Some prices are regional (Epixel in CAD, Odoo by billing country) or promotional (Cobalt).
- **Client documents.** The PRD and compensation plan were treated as statements of intention. Their figures were not validated.

## Sources

**MLM software**

- MLM Soft: [pricing](https://www.mlmsoft.com/cloudplatform/subscription), [compensation plans](https://www.mlmsoft.com/cloudplatform/compensation-plan), [developers API](https://help.mlmsoft.net/hc/en-us/articles/39249636419475-Developers-API), [plan properties](https://help.mlmsoft.net/hc/en-us/articles/39249705385235-Plan-properties-configuration), [payout automation](https://www.mlmsoft.com/about/blog/payout-automation-simplify-your-mlm-payout-process)
- Exigo: [platform](https://www.exigo.com/exigo-platform/), [developers](https://developers.exigo.com/), [integrations](https://www.exigo.com/company/integrations/)
- Epixel: [home](https://www.epixelmlmsoftware.com/), [cryptocurrency MLM](https://www.epixelmlmsoftware.com/cryptocurrency-mlm-software), [API guide](https://api.epixelsoftware.help/), [CAD pricing](https://www.epixelmlmsoftware.com/en-ca/pricing)
- Cloud MLM: [pricing](https://cloudmlmsoftware.com/pricing/), [cryptocurrency MLM](https://cloudmlmsoftware.com/cryptocurrency-mlm-software/), [investment plan](https://cloudmlmsoftware.com/mlm-plan/investment-mlm-plan/)
- FlawlessMLM: [commission software](https://flawlessmlm.com/en/mlm-commission-software), [pricing](https://flawlessmlm.com/en/mlm-marketing-software)
- Infinite MLM: [crypto investment](https://infinitemlmsoftware.com/industries/crypto-investment-network), [pricing](https://infinitemlmsoftware.com/pricing)
- Hybrid MLM: [investment plan](https://www.hybridmlm.io/investment-mlm-plan/), [pricing](https://www.hybridmlm.io/pricing/)
- ARM MLM: [Tron smart contract MLM](https://www.armmlm.com/tron-smart-contract-mlm-software/)
- Tapfiliate: [REST API](https://tapfiliate.com/docs/rest/); Post Affiliate Pro: [pricing](https://www.postaffiliatepro.com/pricing/)
- ISO/IEC 27001 transition: [SGS](https://www.sgs.com/en/news/2024/05/iso-iec-27001-transition-what-you-should-know)

**Wallets and custody**

- Privy: [about](https://privy.io/about-us), [acceptable use policy](https://www.privy.io/acceptable-use-policy), [pricing](https://www.privy.io/pricing), [fiat deposits](https://docs.privy.io/wallets/funding/fiat-deposits/overview), [custodial wallets](https://docs.privy.io/wallets/custodial-wallets/overview), [Earn overview](https://docs.privy.io/wallets/actions/earn/overview), [Earn revenue sharing](https://docs.privy.io/wallets/actions/earn/revenue-sharing)
- Bridge: [developer agreement](https://www.bridge.xyz/legal/developer-agreement)
- Turnkey: [pricing](https://www.turnkey.com/pricing); Dynamic: [pricing](https://www.dynamic.xyz/pricing); Fireblocks: [pricing](https://www.fireblocks.com/pricing); Cobo: [pricing](https://www.cobo.com/pricing); BitGo: [USD1 terms](https://www.bitgo.com/usd1-terms/)
- Turnkey: [policies](https://docs.turnkey.com/concepts/policies/overview); Alchemy: [wallets](https://www.alchemy.com/docs/wallets), [session keys](https://www.alchemy.com/docs/reference/wallet-apis-session-keys); ZeroDev: [terms](https://zerodev.app/terms), [Kernel](https://github.com/zerodevapp/kernel), [Earn](https://docs.zerodev.app/onramp/earn), [pricing](https://zerodev.app/pricing); Openfort: [acceptable use](https://www.openfort.io/acceptable-use-policy), [pricing](https://www.openfort.io/pricing); Para: [terms](https://www.getpara.com/terms-of-service); Pimlico: [pricing](https://www.pimlico.io/pricing)
- Stripe acquisition of Privy: [CoinDesk](https://www.coindesk.com/business/2025/06/11/stripe-to-acquire-crypto-wallet-startup-privy-in-bid-to-expand-web3-capabilities)

**Fiat on-ramps**

- Stripe: [prohibited and restricted businesses](https://stripe.com/legal/restricted-businesses), [Crypto Onramp merchant terms](https://stripe.com/legal/crypto-onramp/merchant-terms)
- Coinbase: [prohibited use](https://www.coinbase.com/legal/prohibited_use); Transak: [acceptable use](https://transak.com/acceptable-use-policy); Banxa: [terms (Dec 2024)](https://banxa.com/wp-content/uploads/2025/02/Customer-Terms-and-Conditions-13-December-2024-BANXA.pdf); Ramp Network: [partner requirements](https://rampnetwork.com/blog/integrating-with-ramp-network-things-you-need-to-get-started); MoonPay: [Express Checkout terms](https://www.moonpay.com/legal/terms_of_use_express_checkout); Mercuryo: [EEA terms](https://mercuryo.io/legal/terms-eea/); Onramper: [terms](https://onramper.com/terms-conditions)

**Yield Product**

- Aave: [v3 overview](https://aave.com/docs/aave-v3/overview), [V4 launch](https://aave.com/blog/aave-v4-live-ethereum), [Earn vaults](https://aave.com/docs/aave-v3/vaults/overview), [wstETH oracle post-mortem](https://governance.aave.com/t/post-mortem-exchange-rate-misallignment-on-wsteth-core-and-prime-instances/24269), [rsETH incident](https://governance.aave.com/t/rseth-incident-2026-04-18/24481), [May 2026 update](https://governance.aave.com/t/al-development-update-may-2026/25013)
- Morpho: [Vault V2](https://docs.morpho.org/learn/concepts/vault-v2/)
- Hyperliquid: [staking](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/staking), [protocol vaults](https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/vaults/protocol-vaults), [audits](https://hyperliquid.gitbook.io/hyperliquid-docs/audits)
- Kiln: [DeFi FAQ](https://docs.kiln.fi/v1/kiln-products/defi/kiln-defi-faq); SwissBorg: [Kiln breach update](https://swissborg.com/blog/swissborg-security-update-kiln-breach)
- Coinbase: [Dedicated ETH staking](https://docs.cdp.coinbase.com/staking/staking-api/protocols/dedicated-eth/overview)

**Compliance tooling**

- Sumsub: [pricing](https://sumsub.com/pricing/), [verification levels](https://docs.sumsub.com/docs/verification-levels), [crypto monitoring](https://docs.sumsub.com/docs/crypto-monitoring), [security incident](https://sumsub.com/newsroom/security-incident-update/)
- Chainalysis: [sanctions oracle](https://go.chainalysis.com/chainalysis-oracle-docs.html); Cobalt: [pricing](https://www.cobalt.io/pricing)

**CRM and helpdesk**

- [Zendesk pricing](https://www.zendesk.com/pricing/), [Freshdesk Omni pricing](https://www.freshworks.com/freshdesk/omni/pricing/), [Intercom pricing](https://www.intercom.com/pricing), [Salesforce Service Cloud pricing](https://www.salesforce.com/service/pricing/), [Odoo editions](https://www.odoo.com/page/editions), [Odoo pricing](https://www.odoo.com/pricing)

**Regulatory references (examples)**

- [FATF 2021 guidance](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html), [MiCA](https://eur-lex.europa.eu/eli/reg/2023/1114/oj), [Transfer of Funds Regulation](https://eur-lex.europa.eu/eli/reg/2023/1113/oj), [FinCEN FIN-2019-G001](https://www.fincen.gov/sites/default/files/2019-05/FinCEN%20Guidance%20CVC%20FINAL%20508.pdf), [FTC MLM guidance](https://www.ftc.gov/business-guidance/resources/business-guidance-concerning-multi-level-marketing), [SEC 2022-134 (Forsage)](https://www.sec.gov/newsroom/press-releases/2022-134), [SEC 2023-133 (Celsius)](https://www.sec.gov/newsroom/press-releases/2023-133), [SEC 2026-30](https://www.sec.gov/newsroom/press-releases/2026-30-sec-clarifies-application-federal-securities-laws-crypto-assets), [Investor.gov](https://www.investor.gov/introduction-investing/investing-basics/glossary/pyramid-schemes)

Supporting research notes with full per-vendor evidence are held in Cyclone's project repository and are available on request.
