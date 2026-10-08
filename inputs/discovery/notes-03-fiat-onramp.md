# 03 — Fiat-to-crypto on-ramps and payment acceptance

- **Project:** Helm (Cyclone for AlphaWave)
- **Workstream:** Fiat on-ramps, off-ramps and payment acceptance
- **Research date:** 2026-10-06
- **Currency:** USD unless a provider publishes only in another currency (stated where so)
- **Jurisdiction:** None confirmed. All findings are jurisdiction-neutral. Provider availability is quoted as the provider states it.

**Evidence labels**
- **Verified:** read directly on the provider's own legal, documentation or pricing page on the research date (quoted where wording matters).
- **Vendor claim:** the provider's marketing or self-description; not independently tested.
- **Not verified:** no primary evidence found, or the page could not be read. Treat as an open question.

Glossary terms used: **Member**, **Deposit**, **Commission**, **Sponsor Tree**, **Yield Product**, **Staking**, **Cyclone**, **QUANT** (see `GLOSSARY.md`).

---

## 1. Summary and recommendation

### Key findings

1. **Stripe expressly prohibits MLM, and the prohibition flows into its Crypto Onramp.** Stripe's Prohibited and Restricted Businesses list (last updated 2026-09-22) names "Pyramid schemes" and "Multilevel marketing services offering commission or recruitment-based sales" as **prohibited**, not merely restricted. It also prohibits "Cryptocurrency mining and staking". The Stripe Crypto Onramp Merchant Terms (§5.4) bind the integrating platform to that list. Helm pays Commissions calculated from Sponsor Tree activity, which falls squarely within that wording. **Verified.** ([Stripe list](https://stripe.com/legal/restricted-businesses), [Onramp merchant terms](https://stripe.com/legal/crypto-onramp/merchant-terms))
2. **Every other major on-ramp whose partner or business terms could be read also bars MLM.** This covers Coinbase (CDP), Transak, Banxa, Ramp Network and Bridge. MoonPay prohibits transactions that "support ... certain multi-level marketing programs". Mercuryo prohibits "Ponzi or pyramid schemes". The team's worry is well-founded and **not specific to Stripe**. It is an industry-wide pattern, largely driven by card-network and banking-partner rules (Coinbase says this explicitly). **Verified** (see §5 evidence table).
3. **Privy's own Acceptable Use Policy does not name MLM.** It prohibits "deceptive, fraudulent, or abusive acts or practices", misrepresenting "the nature of the business", and acting "as a custodian, payment services institution, money transmitter ... without appropriate licensure". **Verified.** However, Privy's fiat funding runs through third parties (Stripe, MoonPay, Meld, Coinbase, Bridge), each with its own terms. Privy's headless card on-ramp requires the app's *own* Stripe account and onramp application. **Verified.** Stripe announced the Privy acquisition in June 2025. **Verified** via Privy's announcement and press.
4. **An on-ramp is structurally different from accepting fiat.** With an on-ramp, the provider is merchant of record, runs KYC, takes fraud and chargeback liability, and delivers crypto to the Member's wallet. The platform never touches fiat. Stripe, MoonPay and Transak document this model. **Verified.** Direct fiat acceptance through a PSP or acquirer, followed by conversion, puts licensing, chargebacks, safeguarding and reconciliation on the platform. It is not a Release 1 candidate.
5. **An aggregator (Onramper, Meld) spreads the risk across providers but does not remove the MLM problem.** Onramper states it is "solely a provider of technical infrastructure" and never acts as a fiat gateway. **Verified.** Underlying providers' terms still apply. Whether each provider separately reviews the integrating platform through an aggregator is **Not verified**.

### Recommendation (working position, subject to legal counsel)

- **Release 1 base case: crypto-direct Deposits only.** Members fund their platform wallet by transferring crypto (for example, a stablecoin on a supported network) from a wallet or exchange they already use. Do not ship an embedded fiat on-ramp in Release 1. This path depends on no on-ramp partner's approval and cannot be switched off by one. It does **not** remove KYC/AML obligations. Those depend on the operating model and jurisdiction and are for legal counsel to determine (brief §3).
- **Treat an embedded on-ramp as a gated Phase 2 item** that requires all of the following:
  - (a) legal counsel's characterisation of the compensation plan and Yield Product;
  - (b) full, accurate disclosure of the MLM model to the provider during business review. Misrepresenting the nature of the business breaches Privy's AUP, Transak's partner terms and Ramp's due-diligence terms, and risks abrupt termination;
  - (c) **written** approval from at least two providers, or an aggregator plus at least two approved underlying providers.
- **Do not plan on Stripe Crypto Onramp** (directly or via Privy's default Stripe routing) unless Stripe confirms eligibility in writing. On the published wording, approval is unlikely.
- **Do not plan direct fiat acceptance** (PSP/acquirer) for Release 1. See §7 for the later-phase path.
- **Withdrawals to fiat** have the same partner-eligibility issue. Release 1 should support crypto withdrawals to a Member's external address only.

### What this changes elsewhere in the report

- Fiat on-ramp integration cost in Release 1 can be set to near zero. Budget instead for provider due diligence, legal review and a Phase 2 integration.
- Cost and timeline risk moves to **provider approval**, which more engineering effort cannot speed up (brief §7).
- The architecture must keep a provider-neutral "funding" seam so that on-ramps can be added, swapped or removed without touching the ledger.

---

## 2. Stripe policy findings (quoted)

Source: [Stripe Prohibited & Restricted Businesses](https://stripe.com/legal/restricted-businesses), page "Last updated: 2026-09-22". **Verified.**

### Prohibited Businesses: "Unfair, deceptive, or abusive acts or practices"

> - Pyramid schemes
> - Multilevel marketing services offering commission or recruitment-based sales
> - "Get rich quick" schemes, including investment opportunities or other services that promise high rewards to mislead consumers; schemes that claim to offer high rewards for very little effort or up-front work; and sites that promise fast and easy money
> - Businesses offering unrealistic incentives or rewards as an inducement to purchase products or services
> - Predatory investment opportunities with no or low money down
> - Any other businesses that Stripe considers unfair, deceptive, or predatory towards consumers

### Prohibited Businesses: "Nonfiat currency"

> - Cryptocurrency mining and staking
> - Initial coin offerings (ICOs)
> - Secondary NFT sales

### Prohibited Businesses: "The following financial products and services" (excerpt)

> - Funded prop trading
> - Peer-to-peer money transmission

### Restricted Businesses (additional due diligence; approval "may be modified or revoked by Stripe at any time")

> **Cryptocurrency** (Limited availability ...) — Cryptocurrency (for example, Bitcoin, Ripple, Ethereum, Dogecoin, Cardano, etc.) exchanges and wallets.
>
> **Financial products and services** — Investment and brokerage services ...; Lending services ...; Money transmitters, remittances, currency exchange services, and other money service businesses; ... Escrow services; Neobanks or challenger banks; Other financial services

No entry for "network marketing" by name was found; the MLM entry above is the operative one. **Verified.**

### Crypto Onramp Merchant Terms

Source: [Crypto Onramp Merchant Terms of Service](https://stripe.com/legal/crypto-onramp/merchant-terms), last updated 2023-02-24. **Verified.**

> 5.4 Restricted Business List. ... You further represent that you may not use Stripe's Software or Services for any of the prohibited businesses listed here: https://stripe.com/legal/restricted-businesses.

> This License is effective until terminated. Stripe may at any time, without notice to you, suspend your ability to use the Software or terminate the availability of the Software.

### Interpretation for Helm (analyst assessment, not legal advice)

- Helm's model pays Commissions based on Sponsor Tree activity. That matches "Multilevel marketing services offering commission or recruitment-based sales" on its face.
- A Yield Product described as "staking" could also engage "Cryptocurrency mining and staking". The Glossary already discourages "staking" as a generic term.
- Stripe being merchant of record for the onramp transaction does **not** exempt the platform. The merchant terms make the prohibited list a condition of using the onramp.
- Whether a corporate separation (for example, the wallet/Deposit platform as a separate entity from the MLM distributor) changes this is a legal and provider question. It must not be engineered as a workaround (see §9).

### Stripe Crypto Onramp: how it works

| Topic | Finding | Label | Source |
|---|---|---|---|
| Merchant of record | "Stripe acts as the merchant of record for these onramp transactions and assumes full liability for all fraud and disputes. We also handle all regulatory requirements, know your customer (KYC) verifications, and sanctions screening." | Verified | [docs](https://docs.stripe.com/crypto/onramp) |
| Fulfilment party | Consumer terms: Stripe "responsible solely for transmitting your payment to our Exchange Provider ... we are not a cryptocurrency exchange"; the Exchange Provider is not named | Verified | [Onramp terms (2022-11-08)](https://stripe.com/legal/crypto-onramp) |
| Platform review | "To access any of the onramps, you must first submit an onramp application." "We review most onramp applications within 48 hours." The application is needed even for sandbox | Verified | [docs](https://docs.stripe.com/crypto/onramp) |
| Integration | Stripe-hosted (crypto.link.com), Embedded (web, Onramp API) and Embedded components (iOS/Android SDK). All are "Public preview" | Verified | [docs](https://docs.stripe.com/crypto/onramp) |
| Regions | "The embedded onramp is only available in the EU and the US (excluding Hawaii)." The 2022 consumer terms say US residents only; Stripe points to a separate supportability page | Verified (docs); regional detail Not verified | [embedded guide](https://docs.stripe.com/crypto/onramp/embedded), [supportability](https://support.stripe.com/questions/crypto-supportability-and-availability-by-region) |
| Source fiat | `usd` and `eur` only | Verified | [embedded guide](https://docs.stripe.com/crypto/onramp/embedded) |
| Assets/networks | Quote API lists currencies `btc, eth, sol, matic, usdc, xlm` and networks `bitcoin, ethereum, solana, polygon, stellar`. Marketing page also mentions POL and Open Issuance stablecoins | Verified (docs); marketing Vendor claim | [embedded guide](https://docs.stripe.com/crypto/onramp/embedded), [product page](https://stripe.com/crypto-onramp) |
| Payment methods | "credit, debit, Apple Pay, Google Pay, and instant and regular ACH" | Vendor claim | [product page](https://stripe.com/crypto-onramp) |
| KYC | Customers supply email, name, DOB, SSN and address; the platform may prefill all except SSN. Product page: "For low-value transactions, detailed KYC information is not required." | Verified (docs) / Vendor claim (low-value) | [embedded guide](https://docs.stripe.com/crypto/onramp/embedded), [product page](https://stripe.com/crypto-onramp) |
| Wallet delivery | `wallet_addresses` per network with `lock_wallet_address`, so delivery can be locked to the Member's platform wallet | Verified | [embedded guide](https://docs.stripe.com/crypto/onramp/embedded) |
| Webhooks | `crypto.onramp_session.updated` on every status change. States: `initialized`, `rejected`, `requires_payment`, `fulfillment_processing`, `fulfillment_complete` | Verified | [embedded guide](https://docs.stripe.com/crypto/onramp/embedded) |
| Kill switch | Stripe can return `crypto_onramp_disabled` platform-wide during fraud events | Verified | [embedded guide](https://docs.stripe.com/crypto/onramp/embedded) |
| Fees | No published rate card. The product page shows an illustrative "$1.28" fee on $100. Docs show `network_fee_monetary` and `transaction_fee_monetary` fields in example quotes, which are illustrative only | Not verified (quote required) | [product page](https://stripe.com/crypto-onramp), [embedded guide](https://docs.stripe.com/crypto/onramp/embedded) |
| Off-ramp | No Stripe off-ramp found in the onramp docs. Bridge offers off-ramps (below) | Not verified | — |

### Stripe stablecoin products (brief)

Stripe now lists stablecoin payouts, stablecoin acceptance in Checkout, stablecoin balances in Treasury, stablecoin-backed cards, Privy wallets and Bridge orchestration/issuance under one crypto hub. **Verified** ([docs.stripe.com/crypto](https://docs.stripe.com/crypto)). All are Stripe services, so the same prohibited list applies.

**Bridge** (Stripe-owned) offers virtual accounts accepting USD, EUR, GBP, MXN and more, plus "onramps, offramps, and crypto to crypto transfers" APIs. **Vendor claim** ([apidocs.bridge.xyz](https://apidocs.bridge.xyz/)). Bridge's user terms (Bridge Building Limited, last updated 2026-05-05) Exhibit C prohibits using Bridge "to undertake or enable by you or any third party ... investment or credit services, ... multi-level marketing, unfair, predatory or deceptive practices, money services ...". **Verified** ([bridge.xyz/legal](https://www.bridge.xyz/legal)).

### Privy funding flow: does it depend on Stripe?

| Finding | Label | Source |
|---|---|---|
| Card on-ramps: "Privy enables Stripe Crypto Onramp (USD, EUR) and MoonPay (AUD, BRL)" by default. More fiat currencies require KYB with Meld. Bank transfer uses Bridge. Exchange funding uses Coinbase. Crypto deposits can be auto-swapped | Verified | [Privy funding config](https://docs.privy.io/guide/react/wallets/usage/funding/configuration), [Card onramps](https://docs.privy.io/wallets/funding/fiat-onramp) |
| Developers must hold their own accounts with Bridge and Coinbase for those methods | Verified (as stated in docs) | [config](https://docs.privy.io/guide/react/wallets/usage/funding/configuration) |
| Headless card on-ramp is Stripe-only and requires the app to "Create your Stripe account and submit your onramp application" | Verified | [Headless card onramp](https://docs.privy.io/wallets/funding/headless-fiat-onramp) |
| Whether the default (non-headless) Stripe/MoonPay routing runs under Privy's provider relationship or needs the app's own approval | Not verified | — |
| Privy embedded wallets are just addresses, so any third-party on-ramp (Transak, Banxa and so on) can deliver to them via its own widget. Privy does not need to "support" the provider | Analyst assessment (follows from wallet-address delivery model) | — |
| Privy AUP (last update 2025-12-16): no MLM entry; prohibits deceptive practices, misrepresenting business nature, unlicensed custodian/money-transmitter use | Verified | [Privy AUP](https://www.privy.io/acceptable-use-policy) |
| Privy Developer Terms §10: developer "agrees to comply with all applicable terms governing use of Third Party Services" | Verified | [Developer terms](https://www.privy.io/developer-terms-of-service) |
| Stripe acquiring Privy, announced 11 June 2025; Privy "will continue as an independent product" | Verified (Privy announcement, press) | [Privy on X](https://x.com/privy_io/status/1932816495719166167), [SiliconANGLE](https://siliconangle.com/2025/06/11/stripe-acquires-crypto-wallet-infrastructure-provider-privy/) |

**Conclusion:** Privy is not a Stripe-only funding layer. However, every fiat route Privy documents leads to a provider whose terms bar or restrict MLM (Stripe, MoonPay, Coinbase, Bridge). For Meld, terms were not read.

---

## 3. On-ramp vs direct fiat acceptance

| Dimension | Third-party on-ramp (Release 1/2 candidate) | Platform accepts fiat via PSP/acquirer (later phase) |
|---|---|---|
| Who sells crypto to the Member | Provider (merchant of record) | The platform (or its licensed affiliate) |
| Who touches fiat | Provider only | Platform's merchant account / bank account |
| KYC for the purchase | Provider | Platform (plus PSP's own merchant KYB) |
| Chargebacks and fraud | Provider bears them, as Stripe, MoonPay and Transak state in docs or terms | Platform bears them. Card chargebacks against irreversible crypto delivery are a known loss vector |
| Licensing | Provider's licences cover the fiat-to-crypto sale (scope varies by provider and country) | Platform likely needs its own authorisation (for example, money transmission, e-money or crypto-asset service licences). Jurisdiction-dependent; legal counsel to confirm |
| Reconciliation | Match provider webhook (order ID, tx hash) to on-chain Deposit | Full three-way: PSP settlement ↔ bank ↔ internal ledger ↔ crypto purchase/treasury |
| Treasury | None | Platform must buy or hold crypto inventory, manage FX and price risk |
| MLM eligibility gate | Provider partner/business review | PSP/acquirer merchant underwriting. Card networks and acquirers generally classify MLM as high-risk; the Stripe and Coinbase lists both cite card-network rules |
| Time to live | Days to weeks for partner review (Stripe "within 48 hours" for the application; Onramper KYB "3–7 working days") | Months (licensing, banking, acquirer underwriting) |

### Later-phase path to direct fiat acceptance (high level only)

1. Legal counsel confirms target markets, the required licences and whether the MLM compensation plan is lawful there.
2. Choose the model:
   - (a) partner with a licensed VASP/EMI that offers a white-label "virtual account" or IBAN product, where the partner holds fiat (for example, Bridge-style virtual accounts, subject to that partner's MLM policy); or
   - (b) obtain your own licences and sign an acquirer or high-risk PSP agreement.
3. Build an internal double-entry ledger as the source of truth for fiat and crypto balances, with PSP/bank/on-chain reconciliation, chargeback reserve accounting and refund/reversal flows.
4. Add treasury and liquidity: an OTC or exchange account for conversion, inventory limits and price-risk policy.
5. Run enhanced KYC/AML and transaction monitoring at the platform level, with Travel Rule handling where applicable.
6. Start bank-transfer-first (lower chargeback exposure) before cards.

---

## 4. Per-provider sections

### 4.1 Stripe Crypto Onramp
Covered in §2. **MLM status: prohibited (Verified).**

### 4.2 MoonPay
- **Integration:** web SDK as a modal overlay or in-app web view, plus a sandbox. **Verified** ([MoonPay on-ramp docs](https://dev.moonpay.com/docs/on-ramp-overview)). MoonPay Enterprise offers "One API across fiat and crypto" with white-label branding. **Vendor claim** ([Enterprise article](https://support.moonpay.com/en/articles/682870-moonpay-enterprise-for-businesses-who-it-s-for-and-what-it-enables)).
- **Merchant of record:** "As the merchant of record MoonPay assumes full responsibility for all fraud disputes and chargebacks." **Verified** ([docs](https://dev.moonpay.com/docs/on-ramp-overview)).
- **KYC:** "All customers are required to pass MoonPay's established Know Your Customer (KYC) and risk management procedures." **Verified** (same).
- **Partner due diligence:** "Once you've completed the KYB process, your API keys will be made available." **Verified** (same).
- **MLM policy:** The Express Checkout Terms of Use (MoonPay USA LLC) list as "Unacceptable Activity" transactions that "(b) support pyramid or ponzi schemes, matrix programs, other 'get rich quick' schemes or certain multi-level marketing programs". **Verified** ([Express Checkout ToU](https://www.moonpay.com/legal/terms_of_use_express_checkout)). MoonPay's help centre also hosts consumer guidance titled "How to protect yourself from multi-level marketing and pyramid scheme scams". **Verified** ([article](https://support.moonpay.com/en/articles/633977-how-to-protect-yourself-from-multi-level-marketing-and-pyramid-scheme-scams)). Partner/business terms with a prohibited list were not publicly located. **Not verified.**
- **Regions/assets/methods:** "150+ countries". Visa, Mastercard and Maestro cards, bank transfers, Apple Pay, Google Pay, SEPA, UK Faster Payments, PIX. Docs claim "100+ cryptocurrencies". **Vendor claim** ([moonpay.com/buy](https://www.moonpay.com/buy), [docs](https://dev.moonpay.com/docs/on-ramp-overview)).
- **Fees:** "Transaction fees are as low as 1% for bank transfers and 4.5% for Visa cards." Minimum purchase usually about €20. **Verified** ([moonpay.com/buy](https://www.moonpay.com/buy), [how to buy](https://support.moonpay.com/en/articles/380500-how-do-i-buy-cryptocurrency-with-moonpay)).
- **Off-ramp:** Yes, via the MoonPay sell product. **Vendor claim** ([moonpay.com/sell](https://www.moonpay.com/sell)).
- **Webhooks:** Not confirmed in the pages read. **Not verified.**

### 4.3 Transak
- **Integration:** API, web redirect, iFrame, JS SDK, and native iOS/Android/React Native. **Verified** ([docs](https://docs.transak.com/getting-started/what-is-transak.md)).
- **KYC/compliance:** Transak handles "KYC, regulation and compliance", with KYC reliance options. **Vendor claim** (same).
- **Partner due diligence:** Partners submit business name, ID number, URL, "the nature of Your business or activities", plus director/UBO identity data. The account is "preliminary" until approved and may be terminated "at any time at our sole discretion". **Verified** ([Partner Terms, updated 2 Feb 2024](https://transak.com/partner-terms-of-service)).
- **MLM policy:**
  - The Partner Terms say "You may not use the Services to enable any person (including You) to benefit from any activities Transak has identified as a prohibited activity and agree to abide by Our Acceptable Use Policy."
  - The AUP lists "Prohibited Uses" including "Get rich quick schemes" and **"Multi-level marketing"**.
  - **Verified** ([Partner Terms](https://transak.com/partner-terms-of-service), [AUP](https://transak.com/acceptable-use-policy)).
- **Termination:** Fault termination with immediate effect after 10 business days' cure for material breach. Transak "may refuse, condition, or suspend any Transactions" that expose it to unacceptable risk. **Verified** (Partner Terms).
- **Fees (EUR-denominated, published):** Verified ([fee article](https://support.transak.com/en/articles/7845942-how-does-transak-calculate-prices-and-fees)).
  - On-ramp: card (EUR) 3.5% + €1; card (non-EUR) 5.5% + €1; Apple/Google Pay 3.5% (EUR) or 5.5% (non-EUR), minimum €1; SEPA 0.99%, minimum €1. Plus a spread of 0–2.5% over CoinGecko.
  - Off-ramp: card (EUR) 0.99%, minimum €3.49; card (non-EUR) 4.99%, minimum €5.99; SEPA 0.6%, minimum €3.
- **Off-ramp:** Yes. **Verified** (docs/fees).
- **Webhooks:** Referenced in docs. Not inspected in detail. **Not verified.**

### 4.4 Banxa
- **Integration:** Referral URL/iFrame, server-side API (with webhooks and KYC sharing), and mobile SDKs (React Native, iOS, Android). **Verified** ([docs](https://docs.banxa.com/docs)).
- **KYC/compliance:** Banxa runs document verification, KYC, "Sanctions screening, transaction monitoring, and ongoing compliance". **Vendor claim** (same).
- **Partner onboarding:** Partner ID (`partnerRef`), API key, sandbox and production. KYB detail was not read. **Not verified.**
- **MLM policy:** Customer Terms & Conditions, Part A, effective 15 December 2024, "Prohibited Businesses". **Verified** ([Banxa T&C PDF](https://banxa.com/wp-content/uploads/2025/02/Customer-Terms-and-Conditions-13-December-2024-BANXA.pdf)). Whether a newer version supersedes this PDF is **Not verified**.
  > (i) Investment and credit services: ... investment schemes; ... (x) Multi-level marketing: pyramid schemes, network marketing, and referral marketing programs; (xi) Unfair, predatory or deceptive practices: investment opportunities or other services that promise high rewards; ...
- **Fees:** No public rate card located. **Quote required.**
- **Off-ramp:** Offered (sell flows in docs). **Vendor claim.**

### 4.5 Ramp Network
- **Integration:** Widget plus SDK reference, webhooks, on-ramp and off-ramp docs. **Verified** ([docs.rampnetwork.com](https://docs.rampnetwork.com/)).
- **Partner due diligence:** The Widget Partnership Agreement "terminates immediately upon your failure to pass the Ramp Network Due Diligence Review", which has initial and periodic reviews. Ramp may suspend or terminate "without advance notice" if, among other things, the partner does "something which does or may pose a security or reputational risk to us". Partners must notify "material changes to the Integrator Services at least 30 days before". **Verified** ([Partner T&Cs, updated 7 Jan 2026](https://rampnetwork.com/partners-terms-conditions)).
- **MLM policy:** Ramp's partner-integration article: "we cannot currently work with businesses coming from the following list of restricted industries or sectors: ... Get-rich-quick schemes, multi-level marketing, drop-shipping, or other activities that may be considered unfair, deceptive, or abusive acts or practices (UDAAP)". **Verified**, but the article is dated 8 Sep 2022, so confirm it is still current ([Ramp blog](https://rampnetwork.com/blog/integrating-with-ramp-network-things-you-need-to-get-started)). User terms (updated 24 Sep 2026) prohibit gambling and securities but do not name MLM. **Verified** ([ToS](https://rampnetwork.com/terms-of-service)).
- **Fees:** Charged to end users and shown in the preview screen, which may include a spread. No public rate card. A partner **annual maintenance fee of $2,000** may be charged "at our sole discretion" if annual volume is under $1,000,000. Partners may add a "fee on top" (not available to UK-registered partners unless conditions are met). **Verified** (Partner T&Cs).

### 4.6 Mercuryo
- **Integration:** Widget and API, with fee/subtotal/total/rate fields in API v1.6. **Verified** ([Mercuryo API migration docs](https://github.com/mercuryoio/api-migration-docs)). The public developer docs domain did not resolve on the research date. **Not verified.**
- **Partner terms:** "Terms and conditions for widget and API integration services" (MONEYMAPLE TECH LTD, Canada, Version 5). Partners must implement IP/BIN blocking for prohibited jurisdictions. Mercuryo "at any time retains the right at its sole discretion to prohibit the use of the Widget and/or API Interface by the Company's partners". **Verified** ([Business terms](https://mercuryo.io/legal/terms-business/)). No MLM entry was found in the business terms. **Verified (absence in text read).**
- **MLM-adjacent policy:** EEA individual terms (v1.0.5, from 01.07.2026) §3.4 bar use "in connection with any unlawful, prohibited or restricted activity, including ... Ponzi or pyramid schemes, ... or any activity prohibited by applicable law or by any Third-Party Provider, acquirer, payment service provider, ... card scheme". **Verified** ([EEA terms](https://mercuryo.io/legal/terms-eea/)).
- **Fees, KYC detail, webhooks, regions:** **Not verified / quote required.**

### 4.7 Coinbase Onramp (Coinbase Developer Platform)
- **Integration:** Coinbase-hosted and headless (embedded Apple Pay / Google Pay). Off-ramp is Coinbase-hosted only. Session tokens, webhooks and a transaction status API are available. New integrations start in trial mode until formal onboarding. **Verified** ([Onramp docs](https://docs.cdp.coinbase.com/onramp/docs/faq/), [FAQ](https://docs.cdp.coinbase.com/onramp/additional-resources/faq)).
- **Regions:** "available in all countries which Coinbase operates except Japan." Guest checkout (US/UK/CA) "Will be deprecated on June 30, 2026", so after the research date users likely need a Coinbase account. Off-ramp requires a Coinbase account. **Verified** ([FAQ](https://docs.cdp.coinbase.com/onramp/additional-resources/faq)).
- **Fees:** "2.5% fee for credit card transactions, and 0.5% fee for ACH". "Zero-fee USDC onramping is available to select partners through a subsidy program". **Verified** ([FAQ](https://docs.cdp.coinbase.com/onramp/additional-resources/faq)).
- **MLM policy:**
  - The CDP Terms prohibit using CDP Tools to "engage in any prohibited use or prohibited business as defined in the prohibited use policy". **Verified** ([CDP Terms](https://www.coinbase.com/legal/developer-platform/terms-of-service); coinbase.com returned HTTP 403 to automated fetch, so this was read via a [Wayback copy of 17 Apr 2026](https://web.archive.org/web/20260417102632/https://www.coinbase.com/en-ca/legal/developer-platform/terms-of-service)).
  - The Prohibited & Conditional Use Policy (effective 31 Jan 2022) lists "**Multi-level Marketing:** Pyramid schemes, network marketing, and referral marketing programs." and "**Investment and Credit Services:** ... investment schemes." It also says "Most Prohibited Businesses categories are imposed by card network rules or the requirements of our banking providers or processors." **Verified** ([policy](https://www.coinbase.com/legal/prohibited_use), read via [Wayback copy of 12 Jun 2026](https://web.archive.org/web/20260612092227/https://www.coinbase.com/legal/prohibited_use)).

### 4.8 Alchemy Pay
- **Offering:** On-ramp (bank transfers, mobile wallets and local methods in "over 40 countries") and off-ramp ("50+ countries"). **Vendor claim** ([Alchemy Pay docs](https://alchemypay.readme.io/docs/alchemypay-on-ramp)).
- **Terms, MLM policy, KYB, fees, webhooks:** The legal pages are JavaScript-rendered and could not be read. **Not verified.** Request the merchant agreement and prohibited list.

### 4.9 Onramper (aggregator)
- **Model:** "solely a provider of technical infrastructure ... does not sell cryptocurrencies ... never acts as a Fiat Gateway ... not party to any transactions" and "does not take custody of End-User funds". **Verified** ([Onramper T&C](https://onramper.com/terms-conditions)). Onramper "only receives a fee from the Fiat Gateways". **Verified** (same).
- **Coverage:** "190+ countries", "130 local payment methods", "20+ on-ramp providers". Widget or API, webhooks, signed URLs, sandbox, white-label. **Vendor claim** ([docs](https://docs.onramper.com/)).
- **Partner KYB:** "KYB reviews typically take 3–7 working days". A subscription is required. **Verified** ([onboarding guide](https://docs.onramper.com/docs/step-by-step-guide)).
- **Pricing:** Verified ([pricing](https://onramper.com/pricing)).
  - Essentials: US$199/month, 6 onramps.
  - Premium: US$599/month, "All 30+ onramps", off-ramps, "Add your own fees".
  - White-Label: custom pricing.
  - Annual options are also shown.
- **MLM policy:** The Onramper T&C read does not list MLM. Each underlying gateway's own terms govern its transactions. Whether underlying gateways (for example, Transak, Banxa) separately review the integrating platform when routed via Onramper is **Not verified**. This is a key question.

### 4.10 Meld (aggregator; Privy's extended-currency partner)
- Offers buying, selling and transferring digital assets through "network partners". **Vendor claim** ([Meld docs](https://docs.meld.io/docs/welcome/overview)). Privy requires KYB with Meld for extra currencies. **Verified** ([Privy config](https://docs.privy.io/guide/react/wallets/usage/funding/configuration)).
- Provider list, terms, MLM policy and fees: **Not verified.**

---

## 5. MLM-acceptance evidence table

| Provider | Applies to integrating platform? | MLM / pyramid wording (quoted) | Investment-scheme wording | Label | Source |
|---|---|---|---|---|---|
| Stripe (incl. Crypto Onramp) | Yes, via Onramp Merchant Terms §5.4 | "Multilevel marketing services offering commission or recruitment-based sales"; "Pyramid schemes" (Prohibited) | "'Get rich quick' schemes, including investment opportunities ..."; "Cryptocurrency mining and staking" (Prohibited) | Verified | [list](https://stripe.com/legal/restricted-businesses), [merchant terms](https://stripe.com/legal/crypto-onramp/merchant-terms) |
| Bridge (Stripe) | Yes ("by you or any third party") | "multi-level marketing" | "investment or credit services" | Verified | [bridge.xyz/legal](https://www.bridge.xyz/legal) |
| Coinbase CDP Onramp | Yes, via CDP Terms | "Multi-level Marketing: Pyramid schemes, network marketing, and referral marketing programs." | "investment schemes"; "Investment opportunities ... that promise high rewards" | Verified (Wayback copy) | [policy](https://www.coinbase.com/legal/prohibited_use), [CDP terms](https://www.coinbase.com/legal/developer-platform/terms-of-service) |
| Transak | Yes, via Partner Terms → AUP | "Multi-level marketing" | "Get rich quick schemes" | Verified | [AUP](https://transak.com/acceptable-use-policy), [Partner Terms](https://transak.com/partner-terms-of-service) |
| Banxa | Yes ("you confirm that you will not use ... in connection with a Prohibited Business") | "Multi-level marketing: pyramid schemes, network marketing, and referral marketing programs" | "investment schemes"; "investment opportunities ... that promise high rewards" | Verified (Dec 2024 PDF) | [T&C PDF](https://banxa.com/wp-content/uploads/2025/02/Customer-Terms-and-Conditions-13-December-2024-BANXA.pdf) |
| Ramp Network | Yes (partner restricted industries + DD review) | "Get-rich-quick schemes, multi-level marketing, drop-shipping ..." | — | Verified (2022 article; confirm current) | [blog](https://rampnetwork.com/blog/integrating-with-ramp-network-things-you-need-to-get-started), [Partner T&Cs](https://rampnetwork.com/partners-terms-conditions) |
| MoonPay | Transaction-level (Express Checkout ToU); partner terms not public | "pyramid or ponzi schemes, matrix programs, other 'get rich quick' schemes or certain multi-level marketing programs" | — | Verified (consumer terms); partner terms Not verified | [Express Checkout ToU](https://www.moonpay.com/legal/terms_of_use_express_checkout) |
| Mercuryo | Individual terms; business terms silent on MLM | "Ponzi or pyramid schemes" | — | Verified | [EEA terms](https://mercuryo.io/legal/terms-eea/), [business terms](https://mercuryo.io/legal/terms-business/) |
| Privy | Yes (AUP) | None named; "deceptive, fraudulent, or abusive acts or practices"; no misrepresentation of "the nature of the business" | — | Verified | [Privy AUP](https://www.privy.io/acceptable-use-policy) |
| Onramper | Platform contracts with Onramper; gateways' terms apply to transactions | None found in T&C | — | Verified (absence); gateway pass-through Not verified | [T&C](https://onramper.com/terms-conditions) |
| Alchemy Pay | — | Could not read | — | Not verified | [docs](https://alchemypay.readme.io/docs/alchemypay-on-ramp) |
| Meld | — | Not read | — | Not verified | [docs](https://docs.meld.io/docs/welcome/overview) |

**Pattern:** No provider reviewed publishes a positive statement that it accepts MLM businesses. Providers that do not name MLM (Privy, Onramper, Mercuryo business terms) either do not perform the fiat leg themselves or route to parties that do restrict it. Any acceptance would need to come as an explicit written approval after disclosure.

---

## 6. Comparison table

| Provider | Integration | Merchant of record / seller | KYC by provider | Partner review | Regions (broad) | Fiat-to-crypto assets | Off-ramp | Webhooks | MLM status |
|---|---|---|---|---|---|---|---|---|---|
| Stripe Onramp | Hosted, embedded web, mobile SDK (preview) | Stripe MoR; unnamed Exchange Provider fulfils (V) | Yes (V) | Application, ~48h (V) | US (excl. HI) + EU (V) | BTC, ETH, SOL, POL/MATIC, USDC, XLM (V) | No (Bridge separately) | Yes (V) | Prohibited (V) |
| MoonPay | Web SDK overlay / web view; Enterprise API | MoonPay MoR (V) | Yes (V) | KYB (V) | 150+ countries (VC) | 100+ (VC) | Yes (VC) | NV | "certain MLM programs" barred at transaction level (V) |
| Transak | API, redirect, iFrame, JS, mobile SDKs (V) | Transak (VC) | Yes (VC) | KYB + nature of business (V) | NV | NV | Yes (V) | NV | Prohibited (V) |
| Banxa | Referral/iFrame, API, mobile SDKs (V) | Banxa (VC) | Yes (VC) | NV | NV | NV | Yes (VC) | Yes, API path (V) | Prohibited (V) |
| Ramp Network | Widget, SDK (V) | Ramp entities per ToS (V) | Yes (VC) | DD review, periodic (V) | NV | NV | Yes (V) | Yes (V) | Restricted industry, cannot work with (V, 2022) |
| Mercuryo | Widget, API (V) | NV | NV | Approval + IP/BIN controls (V) | NV | NV | Sell endpoints exist (V) | NV | Pyramid barred; MLM silent (V) |
| Coinbase Onramp | Hosted, headless Apple/Google Pay (V) | Coinbase (VC) | Yes (V) | Trial → onboarding (V) | Coinbase countries except Japan (V) | Coinbase-listed assets incl. Base, Arbitrum, OP (VC) | Yes, hosted, Coinbase account (V) | Yes (V) | Prohibited (V) |
| Alchemy Pay | NV | NV | NV | NV | 40+/50+ countries (VC) | NV | Yes (VC) | NV | NV |
| Onramper | Widget, API (VC) | Not a seller; gateway is (V) | Via gateways (V) | KYB 3–7 days (V) | 190+ (VC) | Via gateways | Premium plan (V) | Yes (VC) | Silent; gateways apply |

V = Verified, VC = Vendor claim, NV = Not verified.

**Settlement into embedded/smart wallets.** All providers above deliver to a wallet address on a chosen network. Stripe additionally supports locking the destination address (Verified). A Privy embedded wallet (EOA) is a standard address. A smart-contract account (for example, ERC-4337) must exist, or be deployable, on the delivery chain. The Member must not be allowed to change the address or pick an unsupported network. Provider-specific behaviour with smart accounts is **Not verified**.

---

## 7. Fees evidence (USD unless stated)

| Provider | Card | Bank / ACH / SEPA | Other | Label | Source |
|---|---|---|---|---|---|
| Stripe Onramp | Not published | Not published | Illustrative "$1.28" on $100 on product page | Quote required | [product page](https://stripe.com/crypto-onramp) |
| MoonPay | "as low as ... 4.5% for Visa cards" | "as low as 1% for bank transfers" | Min. purchase ~€20 | Verified | [moonpay.com/buy](https://www.moonpay.com/buy) |
| Transak (EUR) | 3.5% + €1 (EUR card); 5.5% + €1 (non-EUR) | SEPA 0.99%, min. €1 | Spread 0–2.5%; off-ramp SEPA 0.6%, min. €3 | Verified | [fee article](https://support.transak.com/en/articles/7845942-how-does-transak-calculate-prices-and-fees) |
| Coinbase Onramp | 2.5% (credit card) | 0.5% (ACH) | USDC zero-fee for select partners (subsidy) | Verified | [FAQ](https://docs.cdp.coinbase.com/onramp/additional-resources/faq) |
| Ramp Network | Shown at checkout only | Shown at checkout only | Partner maintenance fee $2,000/yr if < $1M annual volume (discretionary) | Partner fee Verified; user fees Quote required | [Partner T&Cs](https://rampnetwork.com/partners-terms-conditions) |
| Onramper (platform cost) | — | — | US$199/month (Essentials), US$599/month (Premium), custom (White-Label); end-user fees are the gateway's | Verified | [pricing](https://onramper.com/pricing) |
| Banxa | — | — | — | Quote required | — |
| Mercuryo | — | — | — | Quote required | — |
| Alchemy Pay | — | — | — | Quote required | — |
| Meld | — | — | — | Quote required | — |
| Bridge | — | — | Fee Disclosure Statement exists (not read) | Quote required | [bridge.xyz/legal](https://www.bridge.xyz/legal) |

Note: Member-paid on-ramp fees are not platform costs. Platform costs are aggregator subscriptions, partner minimums, integration effort and compliance review.

---

## 8. Off-ramps for withdrawals to fiat (brief)

- **Off-ramps are documented for:**
  - MoonPay (sell), **Vendor claim**
  - Transak (published off-ramp fees), **Verified**
  - Ramp Network, **Verified** (docs section)
  - Coinbase (hosted only, requires a Coinbase account), **Verified**
  - Alchemy Pay ("50+ countries"), **Vendor claim**
  - Onramper Premium, **Verified**
  - Bridge (offramp APIs), **Vendor claim**
- **The same partner MLM policies apply.** Off-ramp partner approval faces the same barrier as on-ramp approval.
- **A withdrawal off-ramp is a second failure point.** If an off-ramp is terminated, Members cannot exit to fiat through the app. Release 1 should support **crypto withdrawals to the Member's own external address**. Members then use any exchange or off-ramp they hold an account with, under that provider's terms.
- **Commission payouts:** pay out in crypto to the Member's platform wallet. Fiat payouts would make the platform a payer of fiat and bring PSP/payout-provider underwriting into scope.

---

## 9. Risks

| # | Risk | Likelihood / impact | Mitigation |
|---|---|---|---|
| R1 | On-ramp partner refuses at onboarding because of MLM classification | High / Medium (Release 1 unaffected if crypto-direct is the base case) | Crypto-direct Deposits as Release 1 base; approach several providers with full disclosure; get approvals in writing |
| R2 | Partner approves, then terminates later after a periodic review, complaints or a reputational event. Ramp, Stripe, Transak and Mercuryo terms all allow suspension at short or no notice | Medium–High / High | Multiple providers, or an aggregator plus at least two direct contracts; provider-neutral funding interface; crypto-direct path always on; Member comms and runbook for provider loss; never hold Member funds in provider balances |
| R3 | Misrepresentation: onboarding under a description that omits MLM or Commissions | — / Severe | Prohibited. Privy AUP bars misleading information on "the nature of the business"; Transak requires "the nature of Your business"; Ramp requires notice of material changes. Disclose fully |
| R4 | "Staking" label triggers separate prohibitions (Stripe: "Cryptocurrency mining and staking") | Medium / Medium | Use Glossary-accurate product descriptions (Yield Product vs Staking) in all provider applications |
| R5 | Member-level account actions: Members buying crypto on consumer exchanges to fund Helm may breach those exchanges' consumer terms (for example, MoonPay "Unacceptable Activity", Coinbase Prohibited Use) | Medium / Medium | Legal review of Member-facing guidance. Do not instruct Members to describe purposes inaccurately. Enforcement practice Not verified |
| R6 | Chargebacks and fraud if fiat is later accepted directly | — / High | Bank-transfer-first; reserves; delayed crypto release; licensed partner model (§3) |
| R7 | Smart-account delivery failure (wrong network, undeployed account) | Low–Medium / Medium | Lock address and network; restrict assets and networks; test per provider |
| R8 | Regional gaps (Stripe US/EU only; Coinbase not in Japan; guest checkout ended) | High / Medium | Aggregator coverage; resolve target markets first |
| R9 | Concentration in the Stripe group (Privy wallets + Stripe Onramp + Bridge under one prohibited list) | Medium / High | Keep wallet provider and fiat providers contractually independent; avoid a single group for both custody/wallet and fiat |

---

## 10. Open questions

### For providers (ask only after Cyclone/AlphaWave approval to engage; no contact made in this research)

1. Do you accept integrating platforms whose business includes multi-level compensation (Commissions on Sponsor Tree activity)? If so, under what conditions? Please answer in writing.
2. Does your review consider the platform entity alone, or affiliated distributors and the compensation plan too?
3. **Stripe:** does "Multilevel marketing services offering commission or recruitment-based sales" apply to a wallet/Deposit platform whose users are recruited and paid through an MLM plan? Does Privy's default Stripe routing require the app's own onramp approval?
4. **Aggregators (Onramper, Meld):** do underlying gateways run their own KYB on the integrating platform? Can individual gateways decline us while others serve us?
5. What termination notice, wind-down period and pending-transaction handling apply? Is there a cure process?
6. Can you deliver to ERC-4337 smart accounts and lock the destination address and network? What are the webhook retry and idempotency semantics?
7. What are the fees, any partner revenue share or "fee on top", minimum volumes and maintenance fees?
8. Which licences cover the fiat-to-crypto sale in each candidate market? Which entity contracts with the Member?
9. **MoonPay / Banxa / Mercuryo / Alchemy Pay:** please provide the current partner agreement and prohibited-business list.

### For legal counsel

1. How is the compensation plan characterised (lawful MLM vs pyramid) in candidate markets? This decides provider eligibility.
2. Is there any lawful structure (for example, separate entities for distribution and the Deposit/wallet platform) that providers would accept on full disclosure? Is that structure appropriate on its own merits?
3. With crypto-direct Deposits and no fiat leg, what KYC/AML, Travel Rule and licensing obligations does the platform still carry in each market? Brief §3: crypto deposits do not automatically remove KYC.
4. Does accepting fiat directly in a later phase require money transmission, e-money, payment institution or crypto-asset service authorisation in target markets?
5. Could Member guidance on funding through third-party exchanges create liability if those exchanges' consumer terms prohibit MLM-related transactions?
6. How should the Yield Product be described to providers and Members so it is not mischaracterised as Staking?

---

## 11. Evidence limitations

- coinbase.com legal pages returned HTTP 403 to automated fetch. They were read via Wayback Machine snapshots from 2026 (linked).
- Alchemy Pay legal pages are JavaScript-rendered and unreadable. Mercuryo's developer documentation domain did not resolve. Meld's terms were not located.
- The Banxa terms PDF is effective 15 Dec 2024. The Ramp restricted-industries article is from 2022. Both should be reconfirmed with the providers.
- The MoonPay MLM clause was found in Express Checkout consumer terms. Partner terms are not public.
- No provider was contacted and no account was created. All fees are as published on the research date and are subject to change.
