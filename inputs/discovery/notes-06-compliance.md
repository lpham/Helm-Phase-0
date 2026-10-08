# 06 — Compliance-supporting tooling and regulatory question map

- **Project:** Helm (Cyclone for AlphaWave)
- **Workstream:** KYC/KYB, AML screening, blockchain analytics, Travel Rule, security assurance, and regulatory questions for legal counsel
- **Research date:** 2026-10-06
- **Currency:** USD
- **Jurisdiction:** None confirmed. Regulatory sources below are **examples** (FATF as the global standard-setter; EU and US as large, well-documented regimes). They show what kind of questions exist. They do not say which rules apply to AlphaWave.

**This note is not legal advice.** It describes software that can *support* compliance. No vendor feature, certification or integration authorises AlphaWave's business model, and none replaces the advice of legal counsel in the jurisdictions where AlphaWave operates and markets.

**Evidence labels**
- **Verified:** read directly on the vendor's own documentation or pricing page, or in the regulator's or legislator's own text, on the research date.
- **Vendor claim:** the vendor's own statement about itself, for example certifications listed on its website. The certificate or audit report itself was not inspected.
- **Not verified:** no primary evidence found, the page could not be read, or the only source is a third party. Treat as an open question.
- **Consultant estimate:** Cyclone's working figure. Not a quotation.

Glossary terms used: **Member**, **Deposit**, **Commission**, **Sponsor Tree**, **Yield Product**, **Staking**, **Cyclone**, **QUANT** (see `GLOSSARY.md`).

Related notes: `02-wallets-custody.md` (custody model, Privy/Bridge), `03-fiat-onramp.md` (on-ramp terms and MLM restrictions), `04-yield.md` (Yield Product mechanics).

---

## 1. Summary

### Key findings

1. **The assumption that crypto Deposits need no KYC cannot be confirmed from the software side. The global standard points the other way when the operator controls assets.** The FATF guidance says that anyone who, as a business, holds Members' crypto, or has "control" over it, may be a virtual asset service provider (VASP). This includes control through multi-signature or shared-key set-ups. VASPs must apply customer due diligence (CDD) like banks. The threshold for occasional transactions is **USD/EUR 1,000**, not 15,000. The Travel Rule also applies. **Verified** ([FATF 2021 Updated Guidance, paras 72–76 and 146](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html)). Whether AlphaWave falls within this depends on its custody model and jurisdictions. That is a question for legal counsel.
2. **"Non-custodial" is a fact test, not a label.** FATF and FinCEN both test *control*, not branding. FinCEN looks at four things: who owns the value, where it is stored, whether the owner deals directly with the blockchain, and whether the intermediary has "total independent control". A provider is a money transmitter "regardless of the label the person applies to itself". **Verified** ([FinCEN FIN-2019-G001, §4.2](https://www.fincen.gov/sites/default/files/2019-05/FinCEN%20Guidance%20CVC%20FINAL%20508.pdf)). The EU MiCA definition of custody also covers controlling "the means of access" to crypto-assets on behalf of clients. **Verified** ([MiCA Art. 3(1)(17)](https://eur-lex.europa.eu/eli/reg/2023/1114/oj)).
3. **Even a no-KYC-at-onboarding design still needs some screening, and the payout side needs more.** `02-wallets-custody.md` found that Commission payouts always come from an operator-controlled (custodial) treasury wallet. The EU Transfer of Funds Regulation, for example, applies to transfers to and from self-hosted wallets whenever a crypto-asset service provider is involved. Above EUR 1,000 it requires steps to check that the self-hosted address belongs to the customer. There is no de minimis threshold for crypto in the TFR. **Verified** ([TFR recitals 38–39, Art. 14(5)](https://eur-lex.europa.eu/eli/reg/2023/1113/oj)).
4. **Fiat on-ramps impose KYC whatever AlphaWave decides.** On-ramp providers run their own KYC. Most also prohibit MLM (`03-fiat-onramp.md`). Scenario C (no KYC) therefore means crypto-only Deposits, and it does not remove the on-ramp problem.
5. **Commissions linked to Deposits or Yield Product returns raise questions under pyramid-scheme and securities law.** These are separate from AML. The FTC's MLM guidance condemns "recruitment with rewards unrelated to product sales". It also says that earnings claims must reflect what a typical participant achieves. **Verified** ([FTC MLM guidance](https://www.ftc.gov/business-guidance/resources/business-guidance-concerning-multi-level-marketing)). Under the US *Howey* test, a "reasonable expectation of profits … from the efforts of others" can create an investment contract. **Verified** (SEC text). Note that the SEC withdrew its 2019 digital-asset framework. A Commission interpretation issued on 17 March 2026 replaces it ([SEC press release 2026-30](https://www.sec.gov/newsroom/press-releases/2026-30-sec-clarifies-application-federal-securities-laws-crypto-assets)).
6. **The tooling is mature, quick to integrate and cheap at pilot volume. Tooling is not the bottleneck; the legal decision is.** Published self-serve prices range from USD 0.33 to 1.89 per full KYC check (Didit, Sumsub, Veriff). Monthly minimums range from USD 0 to 299. Free sanctions-address screening exists (Chainalysis oracle/API, TRM Sanctions API). The main blockchain analytics vendors (Chainalysis KYT, TRM, Elliptic, Merkle Science) do not publish prices.
7. **Sumsub is the most complete single vendor for a crypto platform.** One contract covers KYC, KYB, AML screening, crypto wallet and transaction screening (through six analytics providers), Travel Rule and transaction monitoring. **Verified** (docs). Due-diligence item: on 4 February 2026 Sumsub disclosed a July 2024 security incident in a support environment, detected in January 2026. **Verified** ([Sumsub](https://sumsub.com/newsroom/security-incident-update/)).
8. **Privy (the wallet base case) offers KYC/KYB only through Bridge.** Bridge is a Stripe company whose terms restrict MLM (see `02` and `03`). Privy's native KYC should therefore not be relied on. No native sanctions or wallet screening was found in Privy's documentation index. Its policy engine can restrict transfers. **Verified** ([Privy KYC setup](https://docs.privy.io/kyc-kyb/setup.md)).

### Recommendation (tooling, subject to legal confirmation)

- **Plan for Scenario B (tiered KYC) as the base case.** Build the identity and screening seams into Release 1 even if thresholds are not yet set. Retrofitting KYC after Members have deposited is harder operationally and commercially than turning on a tier that already exists.
- **Shortlist:** Sumsub (single-vendor crypto stack) and Didit (lowest published cost, wallet screening and KYT modules) for a pilot. Persona or Veriff are alternatives if a non-crypto-specialist IDV vendor is preferred. Pair Didit or Persona with a separate analytics or Travel Rule vendor if needed.
- **From day one, whatever the scenario:** screen every Deposit source address and every withdrawal or Commission payout address against sanctions lists. The free Chainalysis oracle/API is the minimum. A commercial KYT provider can replace it once the volume and risk appetite are known.
- **Do not accept real funds** until counsel has answered the questions in §10, at least for the launch jurisdictions.

---

## 2. KYC scenario implications

The three scenarios come from the report framing. Scenario B is the base case. The table describes what each scenario needs and what it changes. It does not say which scenario is lawful anywhere.

| | **A — KYC at onboarding** | **B — Tiered / threshold KYC (base case)** | **C — Crypto-only, no KYC** |
|---|---|---|---|
| **What Members experience** | Full document + liveness check before any Deposit or Sponsor Tree placement | Light tier at sign-up (email/phone, sanctions/PEP name check, maybe date of birth and country). Document + liveness check triggered by thresholds (cumulative Deposits, first withdrawal, Commission earned, Yield Product access) | Wallet sign-up only. No identity collected |
| **Tooling needed** | IDV (doc + liveness), AML/PEP screening + ongoing monitoring, KYB for corporate Members, wallet screening, case management, record retention | As A, plus a configurable level/tier engine (e.g. [Sumsub verification levels and applicant actions](https://docs.sumsub.com/docs/change-verification-levels-based-on-applicant-actions), [Persona Workflows](https://docs.withpersona.com/workflows.md)) and platform-side threshold logic in the ledger | Wallet/transaction screening only (sanctions oracle or KYT). There is still a Commission payout process, which needs a payee record of some kind |
| **Travel Rule** | Can be supported (Sumsub, Notabene) if counsel says it applies | Same as A | Cannot be met for withdrawals if counsel says it applies, because originator name and address are not collected (e.g. [TFR Art. 14](https://eur-lex.europa.eu/eli/reg/2023/1113/oj)) |
| **Effect on fiat on-ramps** | On-ramp runs its own KYC. Platform KYC does not remove it. MLM restrictions still apply (`03`) | Same | Fiat route effectively closed. On-ramps KYC the buyer, and most bar MLM merchants (`03`) |
| **Effect on Commission payouts** | Payee identity known. Supports tax-reporting questions and clawbacks | Gate payout above a threshold on full KYC | Payouts to anonymous wallets. Highest risk of sanctions exposure, duplicate-account abuse (self-sponsoring in the Sponsor Tree), and inability to claw back |
| **Effect on vendors (MLM, custody, banking)** | Easiest to explain in vendor and banking due diligence | Explainable if the tier thresholds are documented and approved by counsel | Many custody, banking and payment providers require their customer to have an AML programme. Scenario C may block those relationships. **Not verified** per vendor; ask in vendor due diligence |
| **Fraud and abuse** | Lowest. One person, one Member | Low above threshold. Sybil risk (many fake Members) below threshold | High. Commission structures reward fake Members, and there is no identity to deduplicate |
| **Conversion and speed** | Lowest conversion. Adds 1–3 minutes per Member (Consultant estimate) | Good balance | Highest conversion |
| **Indicative monthly tooling cost at pilot (1,000 new Members/month)** | USD 370–2,500 (Consultant estimate from published per-check prices in §8.3) | USD 250–2,000 plus KYT quote (Consultant estimate, §8.3) | USD 0 (free sanctions oracle) up to a KYT quote |
| **Main risks** | Conversion | Threshold design must be approved by counsel. Engineering must keep tiers consistent across the ledger, payouts and Yield Product | Regulatory (see §9), banking/vendor access, fraud. If counsel later requires KYC, existing anonymous balances must be frozen or remediated |
| **Reversibility** | Can be relaxed later | Thresholds can be tuned | Hard to tighten after launch |

**Design note for all scenarios:** keep identity status (KYC tier, screening results) in the platform as a **gate** read by the ledger, withdrawal service and Commission payout service. The IDV vendor is the source of evidence. The platform is the source of the decision record. This keeps vendors replaceable.

---

## 3. KYC/KYB providers

### 3.1 Sumsub

| Item | Evidence | Label |
|---|---|---|
| Plans: **Basic USD 1.35 per verification, USD 149/month minimum** (ID verification, liveness, face match). **Compliance USD 1.85 per verification, USD 299/month minimum**, adding AML screening and proof of address. Enterprise is custom. 14-day trial with 50 free checks | [sumsub.com/pricing](https://sumsub.com/pricing/) | Verified |
| Add-ons: ongoing AML monitoring USD 0.08 per initial check and per checked match; proof of address USD 1.35 on Basic; email/phone USD 0.04; questionnaires USD 200/month | [sumsub.com/pricing](https://sumsub.com/pricing/) | Verified |
| Business Verification (KYB), AML Transaction Monitoring and Travel Rule appear on the pricing page without a public price | [sumsub.com/pricing](https://sumsub.com/pricing/) | Verified (listed); price = quote |
| Configurable verification levels, and changing levels based on applicant actions (supports tiered KYC) | [Verification levels](https://docs.sumsub.com/docs/verification-levels), [level change by actions](https://docs.sumsub.com/docs/change-verification-levels-based-on-applicant-actions) | Verified |
| Reusable KYC (share, gateway, networks, via API/SDK) | [Reusable KYC](https://docs.sumsub.com/docs/reusable-kyc) | Verified (documented) |
| Webhooks for verification, transaction monitoring and fraud-network events, plus webhook logs | [Webhooks](https://docs.sumsub.com/docs/webhooks) | Verified |
| **Crypto Monitoring:** counterparty wallet screening before the transfer and transaction screening after confirmation. Rule outcomes are continue / on hold / rejected. Automatic retries with exponential backoff | [Crypto Monitoring](https://docs.sumsub.com/docs/crypto-monitoring) | Verified |
| Analytics providers integrated: Crystal Intelligence, Merkle Science, TRM Labs, Elliptic, Chainalysis ("six providers") | [Providers](https://docs.sumsub.com/docs/providers) | Verified |
| Travel Rule: protocols TRP, Sumsub, GTR, CODE, Sygna Bridge; unhosted wallet verification; VASP directory | [Travel Rule docs](https://docs.sumsub.com/docs/travel-rule) | Verified |
| Certifications: SOC 2 Type 2, SOC 1 Type 1, PCI DSS AoC listed in Trust Center. ISO/IEC 27001 also claimed | [Trust Center](https://sumsub.com/sumsub-trust-center/), [SOC 2 news](https://sumsub.com/newsroom/sumsub-receives-soc-2-type-ii-attestation/) | Vendor claim (reports not inspected) |
| Security incident: July 2024 intrusion via a support-ticket attachment. Disclosed 4 Feb 2026. Sumsub states that mainly names, some emails and phone numbers were exposed, and no ID images or biometrics | [Security Incident Update](https://sumsub.com/newsroom/security-incident-update/) | Verified (Sumsub's own statement of scope) |

**Crypto suitability:** high. Sumsub is the only vendor reviewed that covers KYC, KYB, AML, crypto wallet/transaction screening and Travel Rule in one contract. **Gap:** prices for crypto monitoring and Travel Rule are not public.

### 3.2 Persona

| Item | Evidence | Label |
|---|---|---|
| Public pricing page could not be read (HTTP 403 / bot challenge). Third-party sources report an "Essential" plan of about USD 250/month with an annual term and about USD 1.50 per verification | [withpersona.com/pricing](https://withpersona.com/pricing) (blocked); third-party: [Signzy blog](https://www.signzy.com/blogs/kyc-pricing-us-cost-per-verification) | **Not verified** |
| Inquiries (verification flows), Inquiry templates, Accounts, Cases, Lists, Graph (link analysis), Workflows (no-code automation) | [Persona docs index](https://docs.withpersona.com/2025-12-08/llms.txt) | Verified (documented) |
| Watchlist and PEP Reports via API. KYB via API (business reports + owner verification) | [Reports via API](https://docs.withpersona.com/integration-guide-reports-via-api.md), [KYB via API](https://docs.withpersona.com/integration-guide-kyb-via-api.md) | Verified (documented) |
| Webhooks with signature verification guidance, event filters and simulation. Separate sandbox and production environments. Versioned API | [Webhooks](https://docs.withpersona.com/webhooks.md), [Environments](https://docs.withpersona.com/environments.md) | Verified |
| Certifications: SOC 2 Type II, ISO 27001, PCI DSS, FedRAMP Moderate claimed on Persona pages. The security page says copies are available from the account manager | [Security](https://withpersona.com/security), [FedRAMP](https://withpersona.com/blog/personas-fedramp-status/), [PCI](https://withpersona.com/blog/persona-pci-dss-certification) | Vendor claim |
| Crypto wallet screening / Travel Rule | None found in the docs index | Not verified (assume absent) |

**Crypto suitability:** strong IDV and workflow engine. Needs a separate analytics vendor and, if required, a separate Travel Rule vendor.

### 3.3 Veriff

| Item | Evidence | Label |
|---|---|---|
| Self-serve: **Essential USD 0.80 per verification, USD 49/month minimum** (automated). **Plus USD 1.39, USD 99/month minimum** (hybrid AI + specialists). **Premium USD 1.89, USD 209/month minimum**. Enterprise custom, from 5,000+ verifications/month | [veriff.com/pricing](https://www.veriff.com/pricing) | Verified |
| Add-ons: PEP & sanctions screening +USD 0.64; ongoing monitoring +USD 0.09; 2-year retention +USD 0.30. 15-day trial (up to 50 sessions). No setup fee | [veriff.com/pricing](https://www.veriff.com/pricing) | Verified |
| ISO/IEC 27001:2022 (with 27017/27018), SOC 2 Type II, Cyber Essentials, UK DIATF | [Security and compliance](https://www.veriff.com/security-and-compliance) | Vendor claim |
| KYB, wallet screening, Travel Rule | Not checked in depth in this pass | Not verified |

**Crypto suitability:** a good IDV and liveness component with transparent pricing. Not a crypto-specific stack.

### 3.4 Didit

| Item | Evidence | Label |
|---|---|---|
| **Free: 500 full KYC checks/month** (ID, liveness, face match, device/IP). **Pay-as-you-go USD 0.33 per full KYC bundle.** No minimums. Enterprise custom | [didit.me/pricing](https://didit.me/pricing) | Verified |
| Module prices: ID verification 0.15; passive liveness 0.10; AML screening 0.20; ongoing AML monitoring 0.07/user/year; proof of address 0.20; **wallet screening 0.15** (0.02 when you bring your own analytics key, per docs); **transaction monitoring 0.02**; KYB registry 2–9 by tier | [didit.me/pricing](https://didit.me/pricing), [docs.didit.me](https://docs.didit.me/llms.txt) | Verified |
| KYC, KYB, transaction monitoring (KYT) and wallet screening on one API. Reusable KYC listed as free | [docs.didit.me](https://docs.didit.me/llms.txt) | Vendor claim (feature depth not tested) |
| SOC 2 Type 2 (Didit says issued July 2026), ISO 27001:2022 (Bureau Veritas, valid to June 2027), iBeta Level 1 liveness, and validation claims by Spanish authorities | [Security & compliance](https://docs.didit.me/getting-started/security-compliance) | Vendor claim |
| Travel Rule | Not found | Not verified |

**Crypto suitability:** lowest published cost, with crypto modules. It is a younger vendor with a recent SOC 2. Check depth of the wallet screening data source (which analytics provider sits behind it), case management and references during due diligence.

### 3.5 Onfido (Entrust IDV)

| Item | Evidence | Label |
|---|---|---|
| Onfido now operates as Entrust IDV. Workflow Studio, API reference, and new mobile SDKs (iOS, Android, React Native) replacing Onfido Smart Capture | [Entrust IDV docs](https://documentation.identity.entrust.com/) | Verified |
| No public pricing. Third-party sources describe sales-led annual contracts | Third-party only | **Not verified** (quote) |
| Certifications | Security page could not be read | Not verified |

### 3.6 Jumio

| Item | Evidence | Label |
|---|---|---|
| SOC 2, ISO 27001, PCI DSS 4.0.1 listed on the technology/security page | [Jumio security](https://www.jumio.com/about/technology-security/) | Vendor claim |
| No public pricing page found | — | Not verified (quote) |

Onfido/Entrust and Jumio are credible enterprise IDV vendors. They have no published self-serve pricing and no crypto-specific modules were confirmed, so they are lower priority for a 30-day pilot.

---

## 4. Blockchain analytics, wallet screening, transaction monitoring

| Vendor / tool | What it does | Evidence | Pricing | Label |
|---|---|---|---|---|
| **Chainalysis sanctions oracle** | Smart contract `isSanctioned(address)` on Ethereum, Polygon, BNB Chain, Avalanche, Optimism, Arbitrum, Fantom, Celo, Blast, Base. Covers US, EU, UN sanctions designations. Chainalysis "cannot guarantee the accuracy, timeliness" of the data | [Oracle docs](https://go.chainalysis.com/chainalysis-oracle-docs.html) | Free (public contract) | Verified |
| **Chainalysis sanctions screening API** | REST check whether an address is sanctioned. API key required | [API reference](https://auth-developers.chainalysis.com/sanctions-screening/api-reference/reference/check-if-an-address-is-sanctioned) | Free per launch announcement | Verified (exists); free = Vendor claim |
| **Chainalysis KYT** | Real-time transaction monitoring; exposure and behavioural alerts; case management | [KYT product](https://www.chainalysis.com/product/kyt/) | Quote only ("Contact us" on [pricing](https://www.chainalysis.com/pricing/)). Third-party buyer data suggests five-figure-plus annual contracts | Verified (features as marketed); price Not verified |
| **TRM Labs Sanctions API** | Public sanctions screening API. Rate-limited; API key | [TRM Sanctions API docs](https://docs.trmlabs.com/guides/sanctions/introduction), [launch release](https://www.businesswire.com/news/home/20220324005727/en/TRMs-Free-Sanctions-Screening-Tool-Goes-Live) | Free per 2022 release | Verified (docs); free = Vendor claim |
| **TRM Transaction Monitoring** | API + alerts + case management | [TRM TM](https://www.trmlabs.com/products/transaction-monitoring) | Quote | Vendor claim |
| **Elliptic Lens** | Wallet screening + transaction monitoring, "chain-agnostic, real-time" | [Elliptic Lens](https://www.elliptic.co/platform/lens) | Quote | Vendor claim |
| **Merkle Science** | Predictive transaction monitoring and behavioural rules; tracing (Tracker) | [merklescience.com](https://www.merklescience.com/) | Quote | Vendor claim |
| **Via Sumsub** | Uses any of the above as the provider inside Sumsub's rule engine | [Sumsub providers](https://docs.sumsub.com/docs/providers) | Quote | Verified |
| **Via Didit** | Wallet screening USD 0.15; KYT USD 0.02 per transaction | [didit.me/pricing](https://didit.me/pricing) | Published | Verified |

**Practical point:** the free sanctions tools cover **only** sanctions-designated addresses. They do not show indirect exposure to mixers, scams, hacks or darknet markets. A commercial KYT provider adds that. Which level is needed is a risk-appetite and legal question.

---

## 5. Travel Rule solutions

| Vendor | Evidence | Pricing | Label |
|---|---|---|---|
| **Notabene** | Travel Rule platform; VASP network; self-hosted wallet verification | **Free tier** ("Sunrise" / SafeTransact-Rise): send up to USD 10k/month, receive unlimited, no protocol integration. Full platform by demo/quote ([pricing](https://notabene.id/pricing)) | Verified |
| **Sumsub Travel Rule** | Five protocols, unhosted wallet verification, VASP directory; combined with Crypto Monitoring in one submission | Quote ([docs](https://docs.sumsub.com/docs/travel-rule), [crypto monitoring](https://docs.sumsub.com/docs/crypto-monitoring)) | Verified (features) |

Travel Rule tooling matters only if counsel concludes that AlphaWave (or an entity in its structure) is a VASP or CASP in a jurisdiction that has implemented the rule. Notabene publishes per-jurisdiction status ([jurisdictions](https://notabene.id/jurisdictions); Vendor claim). Use it as orientation only.

---

## 6. Sanctions and PEP screening (people and companies)

| Vendor | Evidence | Pricing | Label |
|---|---|---|---|
| **ComplyAdvantage** | Customer and company screening, sanctions/watchlists, PEPs/RCAs, adverse media, ongoing monitoring. Enterprise adds transaction monitoring and payment screening | **Starter from USD 99/month**, up to 2,000 monitored entities. ComplyLaunch free programme for early-stage start-ups (application) ([pricing](https://complyadvantage.com/pricing/)) | Verified |
| **Sumsub AML screening** | Included in the Compliance plan; ongoing monitoring USD 0.08 per check/match | [pricing](https://sumsub.com/pricing/) | Verified |
| **Veriff** | PEP & sanctions +USD 0.64; ongoing +USD 0.09 | [pricing](https://www.veriff.com/pricing) | Verified |
| **Didit** | AML screening USD 0.20; ongoing USD 0.07/user/year | [pricing](https://didit.me/pricing) | Verified |
| **Persona** | Watchlist and PEP Reports | [docs](https://docs.withpersona.com/integration-guide-reports-via-api.md) | Price Not verified |

---

## 7. Do MLM vendors or wallet providers include this natively?

| Provider | Finding | Label |
|---|---|---|
| **Privy** | KYC/KYB is documented as native, but "Privy uses Bridge … including identity verification". It needs a Bridge account and API key, and serves Bridge fiat on/off-ramps, cards and custodial wallets. Bridge's terms restrict MLM (`02`, `03`), so treat this as unavailable | [KYC overview](https://docs.privy.io/kyc-kyb/overview.md), [setup](https://docs.privy.io/kyc-kyb/setup.md) — Verified |
| **Privy** | No native sanctions or wallet-risk screening found in the docs index. Transfer policies (condition sets) can restrict wallet actions, for example to block listed addresses supplied by the platform | [Policies](https://docs.privy.io/controls/policies/overview.md) — Verified (policy engine); screening absent = Not verified |
| **MLM vendors** | Some claim "KYC/AML integration" or manual KYC. None evidenced a named IDV provider, sanctions screening or Travel Rule. See matrix in `01-mlm-vendors.md` §3 | Vendor claim / Not verified |

**Conclusion:** plan for a dedicated KYC/AML vendor and a wallet-screening source integrated at the platform layer. Do not rely on the MLM or wallet vendor to provide them.

---

## 8. Comparison and pricing evidence

### 8.1 Capability comparison

V = verified in vendor docs/pricing; C = vendor claim; — = not found / not verified.

| Capability | Sumsub | Persona | Veriff | Didit | Entrust (Onfido) | Jumio | ComplyAdvantage |
|---|---|---|---|---|---|---|---|
| Document + liveness | V | V | V | V | V | C | — (n/a) |
| Tiered / level-based flows | V | V (Workflows) | — | C | V (Workflow Studio) | — | n/a |
| KYB | V (listed) | V | — | V (priced) | — | — | V (company screening) |
| Sanctions / PEP | V | V | V (add-on) | V | — | — | V |
| Ongoing AML monitoring | V | — | V | V | — | — | V |
| Reusable KYC | V | — | — | C | — | — | n/a |
| Crypto wallet screening | V | — | — | V | — | — | — |
| Crypto transaction monitoring | V | — | — | V | — | — | Enterprise TM (fiat-oriented) |
| Travel Rule | V | — | — | — | — | — | — |
| Webhooks | V | V | — | — | — | — | — |
| Public self-serve pricing | V | — (blocked) | V | V | — | — | V |
| SOC 2 / ISO 27001 | C / C | C / C | C / C | C / C | — | C / C | — |

### 8.2 Pricing evidence (USD, research date 2026-10-06)

| Item | Price | Minimum | Type |
|---|---|---|---|
| Sumsub Basic | 1.35 / verification | 149 / month | **Verified public** |
| Sumsub Compliance (adds AML, PoA) | 1.85 / verification | 299 / month | **Verified public** |
| Sumsub KYB, Travel Rule, Transaction Monitoring, Crypto Monitoring | — | — | Quote |
| Veriff Essential / Plus / Premium | 0.80 / 1.39 / 1.89 | 49 / 99 / 209 per month | **Verified public** |
| Veriff PEP & sanctions add-on | +0.64 / verification | — | **Verified public** |
| Didit full KYC | First 500/month free, then 0.33 | None | **Verified public** |
| Didit AML / wallet screening / KYT | 0.20 / 0.15 / 0.02 | None | **Verified public** |
| Didit KYB registry | 2.00–9.00 by tier | None | **Verified public** |
| Persona Essential | ~250/month, ~1.50/verification (third-party) | Annual (third-party) | **Not verified** |
| Entrust IDV (Onfido), Jumio | — | — | Quote |
| ComplyAdvantage Starter | from 99 / month | ≤2,000 monitored entities | **Verified public** |
| Chainalysis sanctions oracle / API | Free | — | **Verified** (oracle) / Vendor claim (API free) |
| TRM Sanctions API | Free | — | Vendor claim |
| Chainalysis KYT, TRM, Elliptic, Merkle Science | — | — | Quote |
| Notabene Travel Rule (free tier) | Free up to USD 10k sent/month | — | **Verified public** |
| Notabene full platform | — | — | Quote |

### 8.3 Indicative monthly cost for verification and monitoring (Consultant estimate)

These figures assume **1,000 new Members per month**, with 60% reaching the document-KYC tier under Scenario B. They use published prices only. KYT is shown separately because it is quote-only.

| Scenario | Low | Base | High |
|---|---|---|---|
| A — full KYC at onboarding | ~USD 370 (Didit: 500 free + 500 × 0.33 + 1,000 × 0.20 AML) | ~USD 1,850 (Sumsub Compliance, 1,000 × 1.85) | ~USD 2,500 (Veriff Premium + PEP add-on) |
| B — tiered (base case) | ~USD 250 (Didit: 600 document checks, 500 free; AML name screening for all 1,000) | ~USD 1,100–1,300 (Sumsub Compliance, 600 × 1.85; light-tier screening extra) | ~USD 2,000 |
| C — no KYC | USD 0 (Chainalysis oracle) | — | — |
| Add-on: commercial KYT / analytics (any scenario) | via Didit (~USD 0.15 per wallet + 0.02 per tx) | Quote (Sumsub or direct vendor) | Quote. Third-party sources suggest annual contracts start in the five figures (Not verified) |

---

## 9. Regulatory question map (not legal advice)

Each row gives an authoritative source, what it says (quoted or closely paraphrased), and the question it raises for AlphaWave. The sources are **examples**. None has been assessed as applicable.

| # | Topic | Source | What the source says | Question for counsel |
|---|---|---|---|---|
| R1 | Who is a VASP (global standard) | [FATF 2021 Updated Guidance on VAs and VASPs](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html), Glossary / para 44 (PDF read via archived copy; the FATF site blocks automated access) | A VASP is a person who "as a business" conducts, for or on behalf of another person: exchange VA↔fiat, VA↔VA, transfer of VAs, "safekeeping and/or administration of virtual assets or instruments enabling control", or financial services related to an issuer's offer of a VA | Do any of AlphaWave's activities (Deposits, Yield Product, Commission payouts, swaps) fall within the VASP-equivalent definition in the target jurisdictions? |
| R2 | Custodial vs non-custodial | Same, paras 72–76 | "Control" means "the ability to hold, trade, transfer or spend the VA" and "does not mean the control must be unilateral", including multi-signature cases. Software developers and providers of unhosted wallets that "only" develop or sell software are "typically" not covered, but "countries must look at individual facts" | With Privy embedded wallets (with platform policy/signer keys) or an MPC custody model, does AlphaWave or Cyclone have "control" over Member assets? |
| R3 | DeFi labels | Same, para 67 | A DeFi application itself is not a VASP, but "creators, owners and operators … who maintain control or sufficient influence" may be | Does any "DeFi" or smart-contract component of the Yield Product leave AlphaWave with control or sufficient influence? |
| R4 | CDD threshold | Same, para 146 | For VASPs, the occasional-transaction CDD threshold is "USD/EUR 1 000 (rather than USD/EUR 15 000)" and the Travel Rule applies | If AlphaWave is a VASP anywhere, is any no-KYC tier permissible, and at what thresholds? Is Scenario C permissible at all? |
| R5 | Unhosted wallet transfers | Same, paras 295–296 | VASPs sending to or receiving from unhosted wallets should obtain originator/beneficiary information from their customer, and such transfers are within transaction monitoring and sanctions obligations | What information must be collected for Member withdrawals and Commission payouts to self-hosted wallets? |
| R6 | EU CASP licensing (example) | [MiCA, Reg. (EU) 2023/1114](https://eur-lex.europa.eu/eli/reg/2023/1114/oj), Art. 3(1)(16)–(17), Art. 59, Art. 143(3), Art. 149, recital 22 | Crypto-asset services include custody and administration (the "safekeeping or controlling … of the means of access", for example private keys), exchange, transfer and portfolio management. No one may provide them in the Union without authorisation (Art. 59). Applied from 30 Dec 2024. The transitional period ran to 1 July 2026 at the latest. "Fully decentralised" services without any intermediary are out of scope | If EU Members are targeted, does AlphaWave need CASP authorisation, or a licensed partner? Does marketing into the EU through Members count as providing services there? |
| R7 | EU Travel Rule (example) | [TFR, Reg. (EU) 2023/1113](https://eur-lex.europa.eu/eli/reg/2023/1113/oj), recitals 38–39, Art. 14 | Applies "to all transfers including … to or from a self-hosted address, as long as there is a crypto-asset service provider involved". Above EUR 1,000 to a self-hosted address, the CASP must "assess whether that address is owned or controlled by the originator". Applied from 30 Dec 2024 | If EU rules apply, the Travel Rule and self-hosted address verification are required. Scenario C would not meet them |
| R8 | US money transmission (example) | [FinCEN FIN-2019-G001](https://www.fincen.gov/sites/default/files/2019-05/FinCEN%20Guidance%20CVC%20FINAL%20508.pdf), §4.2 | Four-factor test. Hosted wallet providers are "account-based money transmitters". Unhosted single-signature wallet users are not. A multi-signature provider that also hosts, or holds "total independent control", is a money transmitter "regardless of the label" | If US persons are served, would AlphaWave (or the platform entity) be an MSB? What about state money transmitter licences? |
| R9 | MLM legality / pyramid test (US example) | [FTC Business Guidance Concerning MLM](https://www.ftc.gov/business-guidance/resources/business-guidance-concerning-multi-level-marketing) | Quotes *Koscot*: rewards "for recruiting other participants … unrelated to the sale of the product to ultimate users". The FTC assesses marketing, the compensation plan, and incentives to recruit rather than sell to "non-participant end users" | If Commissions are calculated on Members' Deposits (not on purchases of a product by end users), how does that compare with the pyramid-scheme tests in each target jurisdiction? |
| R10 | Earnings claims | Same | Earnings claims must reflect "what the typical person … is likely to achieve" and account for expenses. Atypical testimonials are "likely to generate a deceptive impression" | What income-disclosure statements, Member training controls and content review are required? |
| R11 | Business opportunity disclosure (US example) | [FTC Business Opportunity Rule, 16 CFR Part 437](https://www.ftc.gov/legal-library/browse/rules/business-opportunity-rule) | Requires sellers of business opportunities to give prospective buyers specified information | Does the Rule (or a local equivalent) apply to AlphaWave's Member opportunity? |
| R12 | Investment contracts (US example) | [SEC Howey framework (withdrawn)](https://www.sec.gov/about/divisions-offices/division-corporation-finance/framework-investment-contract-analysis-digital-assets), superseded by the [SEC/CFTC interpretation of 17 March 2026](https://www.sec.gov/newsroom/press-releases/2026-30-sec-clarifies-application-federal-securities-laws-crypto-assets) | *Howey*: "investment of money in a common enterprise with a reasonable expectation of profits to be derived from the efforts of others". The 2026 interpretation adds a token taxonomy and addresses protocol staking, airdrops and wrapping | Is the Yield Product (especially an operator-managed or QUANT trading-based one) an investment contract or collective investment scheme? Do Commissions on Deposits make Members unlicensed brokers or promoters? |
| R13 | Pyramid/Ponzi red flags | [Investor.gov: Pyramid Schemes](https://www.investor.gov/introduction-investing/investing-basics/glossary/pyramid-schemes) | "New participants' fees are typically used to pay money to existing participants for recruiting". Often pitched as MLM | How will AlphaWave show that Commissions and Yield Product returns are not funded by new Deposits? (This links to ledger and reconciliation design.) |

---

## 10. Questions for legal counsel

**Scope and structure**
1. In which jurisdictions will AlphaWave be established, and in which will Members be recruited or served? Which regimes are in scope as a result (R1, R6, R8)?
2. Which legal entity provides each service: wallet, Deposits, Yield Product, Commission calculation, Commission payout? Is Cyclone, as integrator and operator of the application layer, exposed to any of these classifications?

**Custody and licensing**
3. Under the proposed wallet model (Privy embedded wallets with platform policies, or MPC custody), does AlphaWave have "control" over Member assets (R2, R8)? Does the answer change if the platform holds a policy or signer key?
4. Does holding Commission balances in a platform treasury before withdrawal count as safekeeping or transfer on behalf of Members?
5. Does a Yield Product that routes Deposits to a third-party protocol or to QUANT make AlphaWave a VASP/CASP, an investment manager, or neither (R3, R6, R12)?

**KYC and AML**
6. Is any no-KYC tier permissible (Scenario C or a Scenario B light tier)? If so, up to what cumulative amounts, and for which actions (Deposit, withdrawal, Commission, Yield Product access) (R4)?
7. Which customer data must be collected for withdrawals and payouts to self-hosted wallets? Does the Travel Rule apply (R5, R7)?
8. What sanctions screening is required for wallet addresses and for Members? Which lists, and how often?
9. What record-retention periods, suspicious-activity reporting duties and MLRO/compliance-officer appointments apply?
10. Is identity needed for tax reporting on Commissions paid to Members, independent of AML?

**MLM, securities and consumer protection**
11. Are Commissions calculated on Deposits or Yield Product balances lawful under pyramid-scheme laws in each target jurisdiction (R9, R13)?
12. Is the Yield Product (any mechanism: Staking, lending, trading vault, operator-managed) a security, investment contract, collective investment scheme or deposit-taking activity (R12)?
13. Do Members who recruit and earn Commissions on Deposits need any licence or registration, for example as introducers, brokers or promoters?
14. What earnings disclosures, risk warnings and marketing controls are required (R10, R11)?

**Vendor and banking**
15. Can AlphaWave rely on a vendor's KYC (for example reusable KYC, or an on-ramp's KYC) for its own obligations, and on what terms?
16. Must the MLM model be disclosed to KYC, analytics, custody and banking vendors? (Yes, per vendor terms; see `03`.) Are any vendor contract terms incompatible with the model?

---

## 11. Security assurance services

| Service | Typical scope | Cost evidence | Label |
|---|---|---|---|
| Autonomous (AI-assisted) pentest | Web application; findings in 24 hours; human direction | **USD 3,500 per test** (Cobalt promotional offer, valid to 31 Dec 2026) ([Cobalt pricing](https://www.cobalt.io/pricing)) | Verified (promotional) |
| Manual web app + API pentest (PTaaS) | Member app, admin back office, APIs | Cobalt sells annual credit packages, 1 credit = 8 testing hours; price per credit not published ([Cobalt pricing](https://www.cobalt.io/pricing)) | Quote |
| Manual web app + API + cloud pentest, pre-launch | 2 web apps, admin, API, cloud configuration; one retest | USD 12,000–40,000 | Consultant estimate |
| Smart contract audit | Only if AlphaWave deploys its own contracts (for example a Yield Product vault or payout contract). Price scales with code size and complexity | USD 15,000–100,000+ for a small-to-medium codebase. Top-tier firms and competitive audits vary widely. No public rate cards found (Hacken, Halborn: quote) | Consultant estimate |
| Wallet / key-management review | Signing policies, MPC/Privy policy configuration, treasury controls | USD 10,000–30,000 | Consultant estimate |
| Bug bounty (post-launch) | Ongoing | Platform fee + rewards; quote | Not verified |

Avoiding custom smart contracts in Release 1 (using audited third-party protocols, see `04-yield.md`) removes the largest and least predictable assurance cost. The vendor's own audit evidence still needs checking.

---

## 12. Evidence limitations

- Persona's pricing page and the FATF website block automated access. FATF text was read from the official PDF via a Web Archive copy. Persona pricing is from third parties only and is marked Not verified.
- Certifications are vendor statements. SOC 2 reports and ISO certificates were not inspected. Request them under NDA during vendor due diligence, and check scope, period and the issuing body.
- Blockchain analytics and Travel Rule prices are quote-only. Vendors were not contacted, per the brief.
- Regulatory sources are examples from FATF, the EU and the US. Other jurisdictions may differ materially. Nothing here is a legal conclusion.
