# 08 — Smart-account alternatives: Openfort, ZeroDev, Para (+ Pimlico)

- **Project:** Helm (Cyclone for AlphaWave)
- **Workstream:** Wallets, account abstraction, custody (follow-up to note 02)
- **Research date:** 2026-10-06
- **Currency:** USD unless stated otherwise
- **Method:** Desk research of vendor documentation, pricing pages, legal terms, security pages and GitHub. No web search was used; official URLs were fetched directly. We did not contact any vendor or create any account.

**Evidence labels** (same as note 02)

- **Verified:** confirmed on a primary source, such as official docs, a pricing page, legal terms, an audit report or a GitHub repository.
- **Vendor claim:** a statement the vendor makes about itself (marketing, blog, docs describing its own security) that no independent source confirms. Example: SOC 2 status when the report has not been seen.
- **Not verified:** no primary evidence found, or the source could not be accessed.
- **Assumption:** Cyclone's working assumption or analysis, stated for transparency.

Glossary terms (Member, Deposit, Commission, Yield Product, Staking) are used as defined in `GLOSSARY.md`. The custody classification rule is the one in note 02 §6, applied unchanged.

**Helm requirements tested in this note** (from the fallback design in note 02 §1):

1. Members own embedded wallets.
2. The platform can optionally hold a narrowly scoped signer or session key that can deposit into allowlisted ERC-4626 vaults (Morpho / Aave), with caps and expiry, and can never transfer funds out.
3. Gas sponsorship.
4. An operator treasury with multi-approval.
5. Hyperliquid / HyperEVM support (a plus).
6. No dependency on a payment company or exchange whose terms prohibit MLM.

The benchmarks are **Privy** (base case, Stripe-owned) and **Turnkey + Alchemy Smart Wallets** (current Stripe-independent fallback).

---

## 1. Summary and recommendation

### Key findings

1. **None of the three is owned by a payment company or exchange.**
   - **ZeroDev is now an Offchain Labs product.** The ZeroDev Terms of Service are "by and between Offchain Labs, Inc., a Delaware corporation" and the customer. Offchain's own site lists ZeroDev under "Our Products" next to Arbitrum and Prysm. **Verified** ([ZeroDev terms](https://zerodev.app/terms), [offchain.io](https://offchain.io/)). The date and terms of the acquisition were **Not verified** (no announcement found on [zerodev.app/blog](https://zerodev.app/blog) or offchain.io). Offchain Labs builds Arbitrum (an L2), so it is neither a payment company nor an exchange. The ownership does add an ecosystem bias towards Arbitrum (**Assumption**).
   - **Openfort** contracts as **Alamas Labs Inc. d/b/a Openfort** (Delaware). **Verified** ([terms](https://www.openfort.io/terms), [developer terms](https://www.openfort.io/developer-terms)). We found no parent company or acquisition. Ownership and funding: **Not verified**.
   - **Para** (formerly Capsule) contracts as **Capsule Labs Inc.** and names a16z crypto, Geometry, TCG Crypto and Spice Capital as backers. **Verified** for entity and backer list on Para's own pages ([terms](https://www.getpara.com/terms-of-service), [about](https://www.getpara.com/about)). We found no acquisition.
   - **Pimlico** contracts as **Austerlitz Labs Limited** (England and Wales). **Verified** ([ToS](https://www.pimlico.io/tos)).

2. **None of the four names MLM in its terms. Openfort comes closest to the business model.**
   - Openfort's [Acceptable Use Policy](https://www.openfort.io/acceptable-use-policy) (updated 2026-08-06) prohibits "Fraud, deceptive practices, Ponzi or pyramid schemes, market manipulation, or the sale of counterfeit goods" and "Unlicensed money services, gambling, securities, or other regulated activity conducted without the licences, registrations, or authorizations required". **Verified**. "Multi-level" and "network marketing" do not appear. **Verified (by absence)**. An MLM-distributed Yield Product is exactly the kind of business a reviewer could place under "pyramid schemes" or unlicensed "securities". That makes written clearance from Openfort a gating item.
   - ZeroDev / Offchain Labs: no MLM, pyramid or acceptable-use clause. But Offchain may terminate "if a continued relationship with Customer would cause material harm to the reputation of Offchain" (§9.2(a)(ii)), and may suspend for "fraudulent or illegal activities" (§2.5). **Verified** ([terms](https://zerodev.app/terms)). This is a discretionary off-boarding right that an MLM business is exposed to.
   - Para: no prohibited-business list. Para states it is "not a licensed or registered money transmitter, money service business, or custodian" and leaves regulatory authorisations to the customer. **Verified** ([terms](https://www.getpara.com/terms-of-service)).
   - Pimlico: generic "any applicable law" and "unlawful or injurious" restrictions only (ToS last updated 2023-12-12). **Verified** ([ToS](https://www.pimlico.io/tos)).

3. **ZeroDev Kernel is the closest technical substitute for Alchemy's account layer, and it is stronger on HyperEVM.**
   - Kernel supports ERC-4337, ERC-7579 and EIP-7702 and has on-chain permissions: one signer + policies (call policy with per-argument conditions, timestamp, rate limit, gas, signature). **Verified (GitHub, docs)** ([Kernel](https://github.com/zerodevapp/kernel), [permissions](https://docs.zerodev.app/sdk/permissions/intro), [call policy](https://docs.zerodev.app/smart-accounts/permissions/policies/call)).
   - An "agent-created" session key lets the platform generate its own key and have the Member authorise only the public address. The private key never leaves the platform. **Verified (docs)** ([session keys](https://docs.zerodev.app/smart-accounts/permissions/session-keys)).
   - HyperEVM (chain 999) is a listed ZeroDev network, and Privy's HyperEVM recipe names ZeroDev as a paymaster provider. **Verified (docs)** ([ZeroDev chains](https://docs.zerodev.app/api-and-toolings/faqs/chains), [Privy HyperEVM](https://docs.privy.io/recipes/hyperliquid/hyperevm)).
   - ZeroDev Earn (Beta) wraps Aave V3, Morpho, Fluid, Yearn and generic ERC-4626 deposits. **Verified (docs)** ([Earn](https://docs.zerodev.app/onramp/earn)).
   - Weighted multisig validator for an on-chain treasury. **Verified (docs)** ([multisig](https://docs.zerodev.app/advanced/multisig)).
   - Kernel v3.x audit PDFs (ChainLight, Kalos) are published in the repository. **Verified (published files)** ([release/v3.3 audits](https://github.com/zerodevapp/kernel/tree/release/v3.3/audits)). Kernel **v4** (the current `dev` branch) refers to Trail of Bits finding IDs (TOB-KERNEL-3, -11), but no v4 report was found. **Not verified**.

4. **Openfort is the only one of the three that offers a full Privy-like stack, but it does not support HyperEVM.**
   - It has embedded wallets (2-of-3 Shamir), TEE backend wallets, an off-chain default-deny policy engine, an ERC-4337 bundler and paymaster, EIP-7702 (Calibur) and **on-chain** EIP-7715 session keys with contract scope and expiry. A documented "user-owned wallet + server signer" pattern matches requirement 2. **Verified (docs)** ([user and server signers](https://www.openfort.io/docs/products/server/workflows/user-and-server-signers), [policies](https://www.openfort.io/docs/configuration/policies/)).
   - "HyperEVM isn't one of Openfort's supported chains, so Openfort's bundler and paymaster aren't available there." **Verified (docs)** ([HyperEVM recipe](https://www.openfort.io/docs/recipes/hyperliquid/hyperevm)).
   - Openfort's policy engine cannot tell a Hyperliquid withdrawal from an order: "it can allow or block all Hyperliquid signing for an account." **Verified (docs)** ([Hyperliquid policies](https://www.openfort.io/docs/recipes/hyperliquid/policies)). Turnkey's HyperCore controls are more granular (note 02 §3.2).
   - No SOC 2 claim was found. Five third-party audits are listed (CertiK, Cure53, Omniscia, Quantstamp ×2). **Vendor claim** ([security](https://www.openfort.io/security)).

5. **Para is a signer (MPC key infrastructure), not a smart-account platform.**
   - Para uses 2-of-2 DKLS19 MPC: a user share on the device (passkey / secure enclave) and a Para share in Para's cloud HSMs. Neither side signs alone. **Vendor claim** ([key management](https://docs.getpara.com/v3/concepts/key-management.md)). The device-held share gives Members a more independent factor than Privy's or Turnkey's TEE-only models.
   - "Para serves as the Signer and EOA … and is not a smart wallet itself. Para does not provide gas sponsorship." **Verified (docs)** ([account abstraction](https://docs.getpara.com/v3/general/account-abstraction.md)).
   - Transaction Permissions went generally available on 2026-09-24. They are enforced off-chain by Para. **Vendor claim** ([launch blog](https://blog.getpara.com/permissions-launch/)). The docs do not say who produces the signature under "standing access". **Not verified**.
   - Para's server path ("REST API") means "Para's enclave holds the key material; your server holds only an API key", which is platform-controlled. **Verified (docs)** ([llms.txt, REST section](https://docs.getpara.com/llms.txt)).
   - Para competes with Turnkey and Privy as the **signer** under a ZeroDev or Alchemy account. It does not replace the account layer.

6. **Pimlico is infrastructure only.** It provides a bundler, paymaster and permissionless.js (MIT). HyperEVM is listed with bundler and paymaster on EntryPoint v0.6 and v0.7, but **not** EIP-7702 and not v0.8 / v0.9. Gas sponsorship carries a 10% mainnet surcharge. **Verified** ([chains](https://docs.pimlico.io/guides/supported-chains), [pricing](https://www.pimlico.io/pricing)). It is a useful second paymaster for redundancy, not a wallet vendor.

### Ranked recommendation (subject to vendor confirmation and legal advice)

**Does any of them beat Turnkey + Alchemy or Privy for Helm?** No single vendor clearly beats either benchmark. One combination, **Turnkey + ZeroDev Kernel**, matches Turnkey + Alchemy and does better on HyperEVM, DeFi tooling and pricing transparency. We recommend carrying it as a co-equal fallback and deciding between it and Alchemy on vendor answers.

| Rank | Option | Verdict for Helm | Conditions |
|---|---|---|---|
| 1 | **Turnkey (signer) + ZeroDev Kernel (account, permissions, paymaster)** | **Co-equal fallback** with Turnkey + Alchemy. Same split of roles (Turnkey keys and off-chain policies; on-chain session-key limits in the account). Advantages over Alchemy: HyperEVM is a listed chain, Earn (Beta) for Aave / Morpho / ERC-4626, ERC-7579 module ecosystem, published v3.x audits, public plan prices ($69 / $399 per month). Gas premium is 8%, the same as Alchemy's 8% admin fee. | (a) Offchain Labs confirms in writing that it will serve an MLM-distributed Yield Product, given the §9.2 reputational-harm termination right. (b) Kernel v4 audit report obtained, or deploy the audited v3.3. (c) HyperEVM paymaster coverage confirmed for the EntryPoint / 7702 mode used. (d) Turnkey MLM clearance (already open in note 02). |
| 2 | **Turnkey + Alchemy Smart Wallets** (current fallback) | **Keep.** Equivalent on-chain session keys (Modular Account v2, ERC-6900). Its HyperEVM support is only evidenced through Privy's recipe (note 02 §2.5). | As in note 02. |
| 3 | **Privy** (base case) | **Keep as the base case** if Privy / Stripe clears the business. Nothing here removes the Bridge / Stripe concern, and nothing here is clearly better. | As in note 02. |
| 4 | **Openfort** (single-vendor stack) | **Viable alternative to Privy on EVM L2s (Base, Arbitrum and others), not for Hyperliquid.** It has the cheapest published entry pricing, on-chain session keys, a TEE backend wallet with a policy engine and its own paymaster. Its weaknesses: no HyperEVM; Hyperliquid policies are all-or-nothing; no SOC 2 evidence; the AUP's "pyramid schemes" / unlicensed "securities" wording is the closest any vendor here comes to excluding the model; no quorum approvals found for treasury. | Written MLM clearance. SOC 2 status. Quorum or multisig treasury design (for example, use Safe instead). |
| 5 | **Para** (signer) | **Not preferred as the Helm signer, but a credible alternative to Turnkey where a device-held key share is wanted.** It needs ZeroDev, Alchemy or Pimlico for accounts and gas. Its server-side paths (REST wallets, imported sessions of up to 30 days) are platform-controlled and would need the new permissions layer to be safe. HyperEVM is not a listed chain. | Clarify who signs under standing access. Permissions pricing. Report access (SOC 2 Type II, Least Authority audits). |
| — | **Pimlico** | **Infrastructure, not a wallet.** Use it as a secondary bundler / paymaster for HyperEVM (v0.6 / v0.7) or as an open-source SDK (permissionless.js). | No 7702 on HyperEVM. 10% sponsorship surcharge. SOC 2 Type 1 only (Vendor claim). |

**Can be decided now:**

- Keep the account layer separate from the signer vendor. Turnkey, Privy or Para can each sit under a ZeroDev Kernel or Alchemy MAv2 account, so the account-layer choice can be deferred until vendor answers arrive.
- Enforce the platform's Earn-only limits **on-chain** in the account (session-key policies), and in the signer's off-chain policy engine as a second layer.
- Do not use Para REST wallets, Para imported sessions or Openfort backend wallets for **Member** funds. They are platform-controlled (§6).

**Needs vendor answers:** MLM acceptance (all four), Kernel v4 audit, Openfort SOC 2, Para permissions signing mechanics, HyperEVM paymaster coverage.

**Needs legal confirmation:** unchanged from note 02. Does a platform-held, on-chain-scoped session key make the operator a custodian or money transmitter?

---

## 2. Openfort

### 2.1 Corporate status

| Claim | Label | Source |
|---|---|---|
| The contracting entity is **Alamas Labs Inc. d/b/a Openfort**, Delaware. The Terms and Developer Terms were last updated 2026-01-16. | Verified | [Terms](https://www.openfort.io/terms), [Developer Terms](https://www.openfort.io/developer-terms) |
| Acquisition, parent company or payment-company ownership: none found. | Not verified (absence on official pages; no about page, `/about` returns 404) | [openfort.io](https://www.openfort.io/), [blog](https://www.openfort.io/blog) |
| Funding and investors. | Not verified | — |
| Openfort describes itself as "a non-custodial service. We do not have access to your private keys or control over your digital assets." | Vendor claim (legal disclaimer) | [Terms](https://www.openfort.io/terms) |

### 2.2 Key model: who can sign?

- **Embedded wallets:** Shamir's Secret Sharing, **2-of-3**. **Vendor claim** ([on-device security](https://www.openfort.io/docs/products/embedded-wallet/security/on-device)).
  - Device share: in the browser's domain-partitioned local storage (iframe).
  - Auth share: "Encrypted on Openfort servers", released on valid authentication.
  - Recovery share: protected by the chosen recovery method.
  - The key is reconstructed "temporarily in isolated iframe memory" on the client.
  - Openfort states: "Neither Openfort nor any single share holder can access wallets independently."
- **Recovery method changes the custody analysis.** **Verified (docs)** ([recovery methods](https://www.openfort.io/docs/configuration/recovery-methods/)).
  - **Automatic recovery:** "The recovery share is encrypted with a combination of project entropy and Openfort's entropy." The developer backend holds an encryption session and Openfort holds Shield cold storage.
  - **Assumption (Cyclone analysis):** with automatic recovery, the platform and Openfort together hold or can unlock two of three shares (auth + recovery) without the Member. Under the note 02 rule ("alone or together"), that is **not non-custodial**.
  - **Password or passkey recovery** (user entropy, or a WebAuthn PRF-derived key) keeps the recovery share out of reach of both Openfort and the platform.
- **Backend wallets:** keys sit inside a TEE on **GCP Confidential Space**, with HSM-backed Cloud KMS envelope encryption. They are authorised by a developer "wallet secret". "Private keys never leave TEE memory in plaintext." **Vendor claim** ([server security](https://www.openfort.io/docs/products/server/security)). The developer controls these wallets, so they are **custodial** towards any Member whose funds sit in them.
- **OpenSigner:** open-source (Go, MIT), self-hostable key management, "keeping full custody of wallet key shares". **Verified (GitHub)** ([opensigner](https://github.com/openfort-xyz/opensigner), [self-host](https://www.openfort.io/docs/configuration/advanced/self-host)). Openfort says OpenSigner "is currently being audited by Quantstamp" (**Vendor claim**). Self-hosted key management is also listed as an Enterprise feature on the pricing page (**Verified**, [pricing](https://www.openfort.io/pricing)).

### 2.3 Embedded login

Email, social, passkey and wallet authentication, with React, React Native, Swift, Unity and JavaScript SDKs. **Vendor claim** ([homepage](https://www.openfort.io/), [user authentication](https://www.openfort.io/docs/products/embedded-wallet/security/user-authentication)).

### 2.4 Smart account standard

- **Account types:** EOA, Smart Account, Delegated Account. **Verified (docs)** ([EIP-7702 authorization](https://www.openfort.io/docs/products/embedded-wallet/react/wallet/actions/eip-7702-authorization)).
- **EIP-7702:** delegated accounts default to **Calibur**; Simple 7702 or a custom contract are alternatives. **Verified (docs)** (same source).
- **ERC-4337 smart account:** Openfort's own upgradeable account (`openfort-contracts`, ERC-1967 proxy, ERC-1271, paymaster contracts). **Verified (GitHub)** ([openfort-contracts](https://github.com/openfort-xyz/openfort-contracts)).
- **ERC-7579 / ERC-6900 modularity:** **Not verified** (not documented).

### 2.5 Session keys, permissions and policy engine

- **On-chain session keys** through EIP-7715 `wallet_grantPermissions`, on smart or delegated accounts. **Verified (docs)** ([session keys](https://www.openfort.io/docs/products/embedded-wallet/javascript/smart-wallet/advanced/session-keys), [user and server signers](https://www.openfort.io/docs/products/server/workflows/user-and-server-signers)).
  - Limits include expiry, contract allowlist, spend limits and function selectors. Optional `call-limit` caps the number of transactions per grant.
  - "The owner of the account can always revoke the session key". Members revoke through `useRevokePermissions`.
  - The Helm pattern is documented directly: the server holds a **backend wallet**, and the Member authorises its address as a session signer. Openfort's wording: "The wallet stays non-custodial. The user keeps their key, and your server's key never leaves your infrastructure." Under note 02's rule this is **hybrid**, not non-custodial (§6).
- **Off-chain policy engine:** governs **backend-wallet signing and gas-sponsorship requests** (EVM and Solana). **Verified (docs)** ([policies](https://www.openfort.io/docs/configuration/policies/)).
  - Value limits, recipient allow / deny lists, chain ID, ABI / function matching and message patterns.
  - Fail-closed: "if no rule matches, the operation is **rejected**." First match wins; criteria inside a rule are combined with AND.
- **Treasury multi-approval:** no quorum or threshold approval found for backend wallets. **Not verified** ([backend policies](https://www.openfort.io/docs/products/server/policies)). Use Safe (note 02 §3.5) or Turnkey / Fireblocks for the operator treasury.
- **Hyperliquid:** the policy engine sees Hyperliquid actions only as `signEvmHash`, so "a policy can't tell a withdrawal from an order today". Openfort recommends a separate backend "agent wallet" for trading. **Verified (docs)** ([Hyperliquid policies](https://www.openfort.io/docs/recipes/hyperliquid/policies)).

### 2.6 Gas sponsorship

- Openfort runs its own bundler and paymaster, and supports gas payment in ERC-20 / SPL tokens. "Smart accounts, the 4337 bundler, and gas sponsorship are available on every supported EVM chain". The exception: "gas sponsorship isn't available for delegated-account transactions on Ethereum mainnet." **Verified (docs)** ([chains](https://www.openfort.io/docs/configuration/chains), [gas sponsorship](https://www.openfort.io/docs/configuration/gas-sponsorship)).
- Paymaster surcharge: 10% on Free and Growth plans, 5% on Pro and Scale. **Verified** ([pricing](https://www.openfort.io/pricing)).

### 2.7 Chains (including Hyperliquid)

- **EVM mainnets:** Ethereum, Arbitrum One, Arbitrum Nova, Base, Optimism, Polygon PoS, BNB, Avalanche and Beam, plus Solana. **Verified (docs)** ([chains](https://www.openfort.io/docs/configuration/chains)). The blog also announces Robinhood Chain (2026-07-03) (**Vendor claim**, [blog](https://www.openfort.io/blog)).
- **HyperEVM:** not supported. "Openfort's bundler and paymaster aren't available there"; users must hold HYPE for gas. **Verified (docs)** ([HyperEVM recipe](https://www.openfort.io/docs/recipes/hyperliquid/hyperevm)).
- **HyperCore:** recipes for agent wallets, trading, subaccounts and builder codes. **Verified (docs)** ([Hyperliquid recipes](https://www.openfort.io/docs/recipes/hyperliquid/)). As with Privy, this covers trading access. It is **not** native Staking (brief §3).

### 2.8 Yield / DeFi

- Recipes (sample code, not a managed API) for Aave, Morpho, Yield.xyz, vaults.fyi and Zama. **Verified (docs)** ([llms.txt](https://www.openfort.io/docs/llms.txt)).
- The Morpho recipe deposits USDC into an ERC-4626 Morpho vault on Base, using client-side wallets and wagmi. It uses no session keys or policies and mentions no revenue share. **Verified (docs)** ([Morpho recipe](https://www.openfort.io/docs/recipes/morpho)).
- **No packaged Earn product** comparable to Privy Earn. Helm would build the deposit flow and session-key permissions itself (**Assumption**).

### 2.9 On-ramp

- "Funding" is a single API for cards, Apple Pay, bank transfers and tokens. The docs name **Coinbase** (CDP keys, Apple Pay / Google Pay) and **Stripe** (card checkout) and say "Openfort resolves the provider and presentation for each buyer server-side". **Verified (docs)** ([funding](https://www.openfort.io/docs/configuration/funding/)).
- Both named providers carry MLM risk (note 02 §1: Coinbase likely prohibits MLM; Stripe / Bridge prohibits it). The full provider list is **Not verified**. Openfort's funding product should be treated as unusable until a non-Stripe, non-Coinbase route is confirmed.

### 2.10 Acceptable use

- AUP (last updated 2026-08-06), quoted exactly: "Fraud, deceptive practices, Ponzi or pyramid schemes, market manipulation, or the sale of counterfeit goods" and "Unlicensed money services, gambling, securities, or other regulated activity conducted without the licences, registrations, or authorizations required". **Verified** ([AUP](https://www.openfort.io/acceptable-use-policy)).
- MLM is not named. **Verified (by absence)**. The AUP "applies to all deployment types, including self-hosted instances using Openfort-operated services". **Verified** (same source).
- The Developer Terms prohibit configuring delegated actions "in a manner that is misleading or intended to divert, misappropriate, or otherwise obtain unauthorized access to Digital Assets". **Verified** ([developer terms](https://www.openfort.io/developer-terms)). This bears directly on the platform session key: its scope must be disclosed to Members.
- Liability cap: fees paid or payable in the prior 12 months. **Verified** (same source).

### 2.11 Security, audits, portability

- **Audits listed:** CertiK (smart contract wallet, December 2023); Cure53 (Shamir library, September 2024); Omniscia (smart contract wallet, December 2024); Quantstamp (7702 contract delegator, September 2025); Quantstamp (key management, October 2025). "Full audit reports are available to customers and partners" through a Google Drive folder. **Vendor claim** ([security](https://www.openfort.io/security)). We did not open the reports.
- **SOC 2:** no claim found on the security page or the server security docs. **Not verified**.
- **Key export:** users can export the embedded wallet private key (Ethereum and Solana), with "options to restrict export based on user status". **Vendor claim** ([export key](https://www.openfort.io/docs/products/embedded-wallet/react/wallet/actions/export-key)).
  - Exporting the EOA key keeps a 7702 delegated-account address, because the address is the EOA.
  - For an Openfort 4337 smart account, the exported key is the owner key. The account contract stays on-chain, but its tooling stays Openfort-specific (**Assumption**).
- **Portability:** OpenSigner is open-source and self-hostable, which reduces exit risk compared with closed TEE vendors (**Assumption**).

### 2.12 Pricing

Published. See §8.

---

## 3. ZeroDev (Offchain Labs)

### 3.1 Corporate status

| Claim | Label | Source |
|---|---|---|
| The ZeroDev ToS is "by and between Offchain Labs, Inc., a Delaware corporation ("Offchain")" and the customer. Last updated 2026-09-29. | Verified | [ZeroDev terms](https://zerodev.app/terms) |
| Offchain lists ZeroDev under "Our Products" with Arbitrum and Prysm. | Verified | [offchain.io](https://offchain.io/) |
| The ZeroDev homepage says "backed by Offchain"; footers read "©2026 Offchain". | Verified | [zerodev.app](https://zerodev.app/), [ZeroDev Wallet blog](https://zerodev.app/blogs/introducing-zerodev-wallet) |
| **Acquisition by Offchain Labs:** consistent with all of the above (the ToS counterparty is Offchain Labs). The date, price and structure were not found on either official site. | **Verified that ZeroDev is operated by Offchain Labs; acquisition details Not verified** | as above |
| Offchain Labs is an L2 / Ethereum infrastructure company (Arbitrum, Prysm). It is not a payment company or exchange. | Verified (self-description) | [offchain.io](https://offchain.io/) |
| Scale claims: "10M+ smart accounts", "300+ apps", "$2B+ monthly volume", "130+ chains". The docs separately say "6M+ smart accounts" and "50+ networks". | Vendor claim (inconsistent figures) | [zerodev.app](https://zerodev.app/), [docs](https://docs.zerodev.app/) |

**Implication:** ZeroDev now sits inside a larger, well-funded protocol company (**Assumption**). That lowers vendor-viability risk compared with a start-up. It may also push ZeroDev's priorities towards Arbitrum and Robinhood Chain (both named in the ZeroDev Wallet launch post). The ToS reputational-harm termination clause (§3.10) is the main commercial risk.

### 3.2 Key model: who can sign?

- **Kernel accounts are signer-agnostic.** ECDSA, WebAuthn (passkey) and multisig signers are supported, and docs exist for third-party signers including Turnkey. **Verified (docs)** ([permissions](https://docs.zerodev.app/sdk/permissions/intro), [docs index](https://docs.zerodev.app/llms.txt)). Para's docs also list ZeroDev as a supported AA provider (**Verified**, [Para AA](https://docs.getpara.com/v3/general/account-abstraction.md)).
- **ZeroDev Wallet** (launched 2026-07-07) is ZeroDev's own embedded wallet, with email, OAuth and passkey signers. **Vendor claim** ([launch blog](https://zerodev.app/blogs/introducing-zerodev-wallet), [wallet quickstart](https://docs.zerodev.app/wallets/quickstart)).
  - Where its keys are held (TEE, MPC or third party) is **not documented** in the pages reviewed. **Not verified**.
  - **Treat ZeroDev as the account layer, with Turnkey or Privy as the key layer** (**Assumption**).
- **Remote key storage** (a paid add-on): "the private key is never transmitted to you or stored on your server". "Whoever has access to this API key effectively controls all the private keys you manage". **Verified (docs)** ([key storage](https://docs.zerodev.app/advanced/key-storage)). This is platform-controlled, so it is **custodial** if used for Member wallets.

### 3.3 Smart account standard

- **Kernel v4:** ERC-4337, ERC-7579, EIP-7702, ERC-7739, ERC-1271. Variants are KernelUUPS (upgradeable), KernelImmutableECDSA and Kernel7702. Six module types: Validator, Executor, Fallback, Policy, Signer and Scoped Execution Hook. MIT licence. **Verified (GitHub)** ([kernel README](https://github.com/zerodevapp/kernel)).
- The latest tagged release is **v3.3** (2025-04-03). v4 is on the `dev` branch. **Verified (GitHub releases)**.
- **ZeroDev Wallet modes:** "7702 Mode (recommended default)", which keeps the user's EOA address, and "4337 Mode", which uses a counterfactual Kernel address. **Verified (docs)** ([wallet quickstart](https://docs.zerodev.app/wallets/quickstart)).

### 3.4 Session keys, permissions and policy engine

- **On-chain permissions:** "one signer + multiple policies + one action". **Verified (docs)** ([permissions](https://docs.zerodev.app/sdk/permissions/intro)). Policies:
  - **Call Policy:** target contract, selector, `valueLimit`, and per-argument conditions (`EQUAL`, `LESS_THAN`, `LESS_THAN_OR_EQUAL`, `GREATER_THAN`, `NOT_EQUAL`, and so on). **Verified (docs)** ([call policy](https://docs.zerodev.app/smart-accounts/permissions/policies/call)).
  - Timestamp Policy (validity window), Rate Limit Policy, Gas Policy, Signature Caller Policy, and Sudo Policy (unrestricted; never for the platform key).
  - Custom policies can be written as modules.
- **Fit to Helm requirement 2 (Assumption, to be tested in a prototype):**
  - A permission scoped to `deposit(uint256 assets, address receiver)` on an allowlisted vault.
  - `assets` set to `LESS_THAN_OR_EQUAL` the cap.
  - `receiver` set to `EQUAL` the Member's own account address.
  - A Timestamp Policy for expiry.
  - An ERC-20 `approve` call to that vault only, with the amount capped.
  - No `transfer` selector granted.
  - Cumulative (rolling) caps are **not documented** for Call Policy. **Not verified**.
- **Agent-created session keys:** "the agent never had to share the private part of the session key with anyone". The platform generates the key in its HSM / KMS and the Member signs approval of the public address and permissions. **Verified (docs)** ([session keys](https://docs.zerodev.app/smart-accounts/permissions/session-keys)).
- **Revocation:** on-chain through `revokeSessionKey`, normally signed by the root (Member) signer. **Verified (docs)** (same source).
  - Kernel v4 acknowledges a known limitation (TOB-KERNEL-3): a revocation earlier in a bundle does not invalidate a later, already-validated operation in the same bundle. Operators should "treat revocations of compromised keys as racing the key until the revoking transaction is mined". **Verified (GitHub)** ([kernel README, Security](https://github.com/zerodevapp/kernel)).
- **Off-chain gas policies** on the paymaster: which operations ZeroDev will sponsor. **Verified (docs index)** ([gas policies](https://docs.zerodev.app/api-and-toolings/infrastructure/gas-policies)).
- **Treasury multi-approval:** the weighted multisig validator supports ECDSA and passkey signers with weights and a threshold, and signatures can be collected asynchronously. **Verified (docs)** ([multisig](https://docs.zerodev.app/advanced/multisig)). No audit was found for this validator. **Not verified**. Safe remains the more established treasury option (note 02 §3.5).

### 3.5 Gas sponsorship

- ZeroDev runs its own bundler and paymaster, plus ERC-20 gas payment. "Gas Sponsorship Premium: 8%" on all self-serve plans; custom for Enterprise. **Verified** ([pricing](https://zerodev.app/pricing)).

### 3.6 Chains (including Hyperliquid)

- "HyperEVM | 999" is listed under Regular EVM Networks. **Verified (docs)** ([chains](https://docs.zerodev.app/api-and-toolings/faqs/chains)).
- Privy's HyperEVM recipe names ZeroDev as a supported paymaster provider. **Verified (docs)** ([Privy HyperEVM](https://docs.privy.io/recipes/hyperliquid/hyperevm)).
- Per-chain bundler / paymaster status (for example, whether 7702 sponsorship works on HyperEVM) points to [chains.zerodev.app](https://chains.zerodev.app/), which did not render. **Not verified**.
- **HyperCore** (the order book): no ZeroDev documentation found. **Not verified**. HyperCore access would come from the signer (Turnkey or Privy).

### 3.7 Yield / DeFi

- **ZeroDev Earn (Beta)** turns an intent such as "deposit this USDC into a vault on another chain" into a quote. It has methods for Aave V3, Morpho, Fluid and Yearn plus generic ERC-4626 (`earn.erc4626.deposit`). Vault discovery uses vaults.fyi data. **Verified (docs)** ([Earn](https://docs.zerodev.app/onramp/earn)).
- "the owner submits the source-chain calls returned in `quote.transaction` or `quote.userOp`". A relayer handles bridging and destination execution. Fees and revenue share are **not documented**. **Not verified**.
- **Custody note (Assumption):** the cross-chain relayer leg must be included in the custody analysis. While funds are in transit, the relayer or solver contract is the counterparty.
- This is **lending** yield, not Staking (brief §3).

### 3.8 On-ramp

- **Smart Routing Address** (v1 live 2026-09-29): one deposit address that routes funds from a CEX or another chain to a destination chain. It is described as usable with "a fiat onramp with any chain". No fiat partner is named. ZeroDev states "funds sent to the address are never in anyone except the user's control" and relies on "permissionless, non-custodial smart contracts". **Vendor claim** ([Smart Routing Address](https://docs.zerodev.app/onramp/smart-routing-address), [blog](https://zerodev.app/blogs/smart-routing-address-v1-is-live)). Pricing is "Contact us for a custom quote" (**Verified**, [pricing](https://zerodev.app/pricing)).
- ZeroDev has **no fiat on-ramp of its own**. That is a positive here: there is no hidden Stripe or Coinbase dependency (**Assumption**). The fiat workstream (note 03 / 07) still needs a provider.

### 3.9 Security, audits, SOC 2

- **Published audit PDFs** in `release/v3.3/audits`: ChainLight (Kernel v3.0); Kalos (v1, v2.1, v2.2, v2.2 lite, v3 plugins, WebAuthn v1, recovery v1 / v2); a v3.1 incremental audit. **Verified (files present)** ([audits folder](https://github.com/zerodevapp/kernel/tree/release/v3.3/audits)). We did not read the PDF contents.
- **Kernel v4:** Certora formal-verification specs are in the repository (`certora/`), and the README references Trail of Bits finding IDs. No v4 report was found. **Not verified**.
- **SOC 2:** not mentioned on [zerodev.app/security](https://zerodev.app/security). **Not verified**. Offchain Labs' own certifications were not researched.
- **Key export (ZeroDev Wallet):** `useExportWallet` (seed phrase) and `useExportPrivateKey`, with the key material shown "inside a secure iframe and never touches your application code". **Vendor claim** ([export](https://docs.zerodev.app/wallets/export)).
- **Portability:** Kernel is MIT-licensed and works with permissionless.js (Pimlico) and other bundlers. **Verified** ([permissionless.js](https://docs.pimlico.io/references/permissionless)). A Helm Kernel account could therefore keep running on another bundler or paymaster if ZeroDev's hosted service were withdrawn. This is the strongest exit position of the vendors reviewed (**Assumption**).

### 3.10 Terms

- No MLM, pyramid, Ponzi or securities restriction, and no separate acceptable use policy. **Verified (by absence)** ([terms](https://zerodev.app/terms)).
- Suspension if "Customer, any Authorized User or any End User is using the Offchain IP for fraudulent or illegal activities" (§2.5(i)(c)). **Verified**.
- Termination by Offchain "if a continued relationship with Customer would cause material harm to the reputation of Offchain" (§9.2(a)(ii)). **Verified**.
- Offchain may "modify the pricing or cost of its services" (§6.5), with credits for material increases only within the current term. **Verified**.
- No liability cap was identified by our reading. **Not verified**; legal review needed.

---

## 4. Para (formerly Capsule)

### 4.1 Corporate status

| Claim | Label | Source |
|---|---|---|
| The contracting entity is **Capsule Labs Inc.** (California, per the terms). The ToS has no last-updated date. | Verified | [Terms](https://www.getpara.com/terms-of-service) |
| "Formerly known as Capsule". Backed by a16z crypto, Geometry, TCG Crypto and Spice Capital. | Vendor claim | [about](https://www.getpara.com/about), [homepage](https://www.getpara.com/) |
| Acquisition or payment-company ownership: none found. | Not verified (absence) | [blog](https://blog.getpara.com/) |
| "15M+ end users across 200+ companies". | Vendor claim | [homepage](https://www.getpara.com/) |

### 4.2 Key model: who can sign?

- **2-of-2 DKLS19 MPC.** "the private key is generated in a distributed process; it is never assembled in one place at any point in its lifecycle." **Vendor claim** ([key management](https://docs.getpara.com/v3/concepts/key-management.md)).
  - User share: on the device, protected by passkey / biometrics in the secure enclave.
  - Para share: in "Para's cloud hardware security modules (HSMs)".
  - "both shares participate in a cryptographic signing ceremony".
- **Recovery:** the user holds a recovery secret that "Para never has access to". Recovery rotates keys and has a 48-hour delay. If Para is unavailable, "as long as the Cloud Share sent during onboarding is not deleted by the user, they can always refresh keys, export, or sign transactions independently", and "Para cannot censor transactions." **Vendor claim** ([security](https://docs.getpara.com/v3/concepts/security.md)).
- **Server-side paths (platform-controlled):**
  - **REST API wallets:** "Para's enclave holds the key material; your server holds only an API key." Wallets created this way can later be claimed by a user with the same identifier. **Verified (docs)** ([llms.txt, §3 REST API](https://docs.getpara.com/llms.txt)).
  - **Pregenerated wallets (SDK):** "Your backend creates wallets, Para persists shares server-side, and signing happens over HTTP with your API key." **Verified (docs)** ([pregen](https://docs.getpara.com/v3/general/pregen.md)).
  - **Session export:** the client calls `exportSession()`; the server calls `importSession()` and "can now sign on behalf of the user". The maximum session length is 30 days, configurable per API key. **Verified (docs)** ([llms.txt, §10](https://docs.getpara.com/llms.txt), [sessions](https://docs.getpara.com/v3/react/guides/sessions.md)). The docs reviewed do not limit what an imported session may sign. **Not verified**. Treat it as broad authority.

### 4.3 Embedded login

Email, phone, social, passkey and biometrics; web, React Native, Flutter and server SDKs; white-labelling. **Vendor claim** ([pricing](https://www.getpara.com/pricing), [homepage](https://www.getpara.com/)).

### 4.4 Smart account standard

- "Para serves as the Signer and EOA (Externally Owned Account) for smart wallets and is not a smart wallet itself." It integrates with ZeroDev, Alchemy, Safe, Biconomy, Pimlico, thirdweb and Rhinestone. **Verified (docs)** ([account abstraction](https://docs.getpara.com/v3/general/account-abstraction.md)).
- Server examples include "Alchemy/ZeroDev EIP-7702". **Verified (docs index)** ([llms.txt](https://docs.getpara.com/llms.txt)).
- Para's own ERC-4337 / 7579 / 6900 support: not applicable. The smart-account partner provides it.

### 4.5 Permissions / policy engine

- **Transaction Permissions** were announced as generally available on 2026-09-24: "Para evaluates the transaction details against the applicable policies and usage before allowing the wallet to sign." They cover spending limits (including cumulative limits within time windows), recipient restrictions and human-approval requirements. "An approval applies only to the specific request, and the transaction must still satisfy every other enforced restriction." **Vendor claim** ([launch blog](https://blog.getpara.com/permissions-launch/)).
- **Policy language:** `compare` and `aggregate` conditions with `all` / `any` / `not`. Facts include `request.to`, `request.value.baseUnits`, `request.contract.address`, `request.method` and chain. `wallet.spend.erc20` caps direct ERC-20 transfers. Rolling windows use syntax such as `"window": "24h"`. **Verified (docs)** ([permissions reference](https://docs.getpara.com/v3/concepts/permissions-reference.md)).
  - Absolute expiry conditions are not described. **Not verified**.
  - Calldata-argument inspection (for example, an ERC-4626 `receiver` field) is not described. **Not verified**.
- **Two modes:** delegation for user-owned wallets (the user is asked for "standing access" and can revoke) and guardrails for app-owned wallets (no owner consent screen). Production policies are reviewed and published by Para. **Verified (docs)** ([permissions](https://docs.getpara.com/v3/concepts/permissions.md), [React permissions guide](https://docs.getpara.com/v3/react/guides/permissions.md)).
- **Open point:** the docs do not say which party produces the signature under standing access. The likely options are Para's enclave co-signing with a server-held share, or the app's session. **Not verified**. This decides the custody classification and must be asked.
- **Enforcement is off-chain** (in Para's infrastructure), not in the account contract. It can be layered under an on-chain Kernel or MAv2 session key (**Assumption**).
- **Treasury multi-approval:** "human approval requirements" exist (Vendor claim). An m-of-n quorum of named approvers is **Not verified**.

### 4.6 Gas sponsorship

None native: "Para does not provide gas sponsorship". Use ZeroDev, Alchemy, Pimlico or another partner. **Verified (docs)** ([account abstraction](https://docs.getpara.com/v3/general/account-abstraction.md)).

### 4.7 Chains (including Hyperliquid)

- "Para integrates seamlessly with all EVM chains, Solana, Cosmos chains, Stellar, and Sui". The networks table lists more than 50 chains. **Vendor claim** ([chain support](https://docs.getpara.com/v3/introduction/chain-support.md)).
- **HyperEVM / Hyperliquid:** not mentioned. **Not verified**. Generic EVM signing would probably work on HyperEVM (**Assumption**). Para's policy facts would not decode HyperCore actions (**Assumption**).

### 4.8 Yield / DeFi

- No packaged Earn API found. A partnership with Centrifuge "to Support Tokenized Asset Exposure" was announced 2026-08-27. **Vendor claim** ([blog](https://blog.getpara.com/)). Tokenized real-world-asset exposure is a different product category from lending yield. It would need its own legal analysis (brief §3).

### 4.9 On-ramp

- The `OnRampProvider` enum lists `RAMP`, `STRIPE`, `MOONPAY`, `COINBASE` (widget or Apple Pay) and `CDP`. **Verified (docs)** ([OnRampProvider](https://docs.getpara.com/v3/references/types/onrampprovider.md)).
- Stripe and Coinbase carry the MLM risks recorded in note 02. MoonPay and Ramp need their own policy checks (fiat workstream).

### 4.10 Terms

- No MLM, pyramid, Ponzi, gambling or securities prohibition. "Capsule" states it is "not a licensed or registered money transmitter, money service business, or custodian", and the customer is responsible for authorisations (§3.1). **Verified** ([terms](https://www.getpara.com/terms-of-service)).
- Immediate suspension for unauthorised use, overdue accounts or perceived security risk (§2.11). Liability cap: fees paid and payable in the prior 12 months (§11.2). **Verified**.

### 4.11 Security, audits, portability

- **SOC 2 Type II:** "Certified January 2025" (homepage). The compliance doc does not give the auditor or period. Reports are requested from security@getpara.com. **Vendor claim** ([homepage](https://www.getpara.com/), [compliance](https://docs.getpara.com/v3/concepts/compliance.md)).
- **Audits:** Least Authority (October 2023, January 2024); penetration test "scheduled March 2026". **Vendor claim** ([homepage](https://www.getpara.com/)). No public report was found; `/security` returns 404.
- **Key export:** "users are able to" export the full private key through Para Connect. Key material "only assembles on user devices during export". **Vendor claim** ([security](https://docs.getpara.com/v3/concepts/security.md), [security blog](https://blog.getpara.com/how-we-think-about-security-at-para/)).

### 4.12 Pricing

Published MAU tiers; no per-transaction fees. See §8. The pricing page does not show which tier includes Transaction Permissions. **Not verified**.

---

## 5. Pimlico (infrastructure, not a wallet)

| Item | Finding | Label | Source |
|---|---|---|---|
| Entity | Austerlitz Labs Limited (England and Wales); English law; ToS last updated 2023-12-12 | Verified | [ToS](https://www.pimlico.io/tos), [privacy](https://www.pimlico.io/privacy) |
| Ownership | Backers named: Ethereum Foundation, a16z crypto, Safe, Consensys, 1confirmation. No acquisition found. | Vendor claim | [pimlico.io](https://www.pimlico.io/) |
| Products | Alto (open-source ERC-4337 bundler), verifying paymaster, ERC-20 paymaster, permissionless.js (MIT; Safe, Kernel, Biconomy, SimpleAccount, TrustWallet and LightAccount accounts; ERC-7579 actions) | Verified (docs) | [docs](https://docs.pimlico.io/), [permissionless.js](https://docs.pimlico.io/references/permissionless) |
| Key model / login / session keys | None of its own. Pimlico works with external signers (Privy, Dynamic, Magic, Web3Auth, passkeys) and with the account's own modules. | Verified (docs) | [docs](https://docs.pimlico.io/) |
| HyperEVM | "Chain ID 999, slug hyper-evm". Bundler and paymaster on EntryPoint v0.6 and v0.7; **no EIP-7702**; no v0.8 / v0.9 | Verified (docs) | [supported chains](https://docs.pimlico.io/guides/supported-chains) |
| Gas sponsorship | 10% surcharge on mainnets (0% on testnets); Enterprise rates negotiated | Verified | [pricing](https://www.pimlico.io/pricing) |
| Security | "SOC 2 Type 1 Certified"; contracts audited by OpenZeppelin and Quantstamp; OFAC screening | Vendor claim | [pimlico.io](https://www.pimlico.io/) |
| Acceptable use | "multi-level" does not appear. There are generic bans on use that violates "any applicable law" (§2.3(v)) and on "unlawful or injurious" material (§2.3(viii)). | Verified (by absence) | [ToS](https://www.pimlico.io/tos) |
| Custody | Not a key holder. A paymaster or bundler cannot move Member funds; it only pays for or relays already-signed operations (**Assumption**, standard ERC-4337 design). | — | — |

**Role for Helm:** a secondary or fallback bundler / paymaster for HyperEVM 4337 accounts, and permissionless.js as a vendor-neutral SDK. It keeps a Kernel account operable if ZeroDev's hosted service is lost.

---

## 6. Custody classification

**Rule applied (note 02 §6, unchanged):** a model is *non-custodial* only if no party other than the Member (vendor, platform or co-signer) can, alone or together, move the Member's assets without the Member's per-action approval. Embedded wallets, MPC and smart accounts are mechanisms; who holds signing authority decides the classification.

| Model | Who controls signing | Classification (towards Members) | Why / implication |
|---|---|---|---|
| Openfort embedded wallet, **password or passkey recovery**, no session key | Device share + auth share (Member authenticates); the recovery share needs user entropy | **Non-custodial (vendor-dependent)** | Neither Openfort nor the platform holds two shares. Depends on Openfort releasing the auth share and on iframe integrity. |
| Openfort embedded wallet, **automatic recovery** | Openfort holds the auth share; the recovery share is encrypted with project + Openfort entropy | **Hybrid (vendor + platform could act together)** — Assumption | Platform and Openfort together appear able to reach the 2-of-3 threshold without the Member. Use passkey or password recovery for Member wallets, or get Openfort's written analysis. |
| Openfort smart / delegated account + **platform backend wallet as EIP-7715 session signer** (Earn-only, expiry, call limit) | Member, **or** platform within on-chain scope | **Hybrid** | Openfort's docs call this "non-custodial". Under the note 02 rule it is hybrid: the platform can move funds within scope without per-action consent. The on-chain scope is auditable and Member-revocable. |
| Openfort **backend wallet** holding Member funds | Platform (wallet secret) + Openfort TEE | **Custodial** | Operator-controlled. Acceptable for the operator treasury only. |
| ZeroDev Kernel (4337 or 7702) with Member root signer (Turnkey / Privy / Para), **no** session key | Member signer only | **Non-custodial (custody follows the signer vendor's model)** | Module installs and upgrades (KernelUUPS) also need the root signer. Check that no Sudo-policy permission or executor module is installed. |
| ZeroDev Kernel + **agent-created platform session key** (call policy on vault `deposit`, `receiver == account`, cap, timestamp) | Member, **or** platform within on-chain scope | **Hybrid** | The narrowest platform authority reviewed. It is still signing authority. Revocation races in-flight bundles (TOB-KERNEL-3). |
| ZeroDev remote key storage, or ZeroDev Wallet with keys held by the platform's API key | Platform (API key) | **Custodial** | "Whoever has access to this API key effectively controls all the private keys". |
| ZeroDev Earn cross-chain deposit | Member signs the source call; a relayer executes the destination leg | **Transit counterparty risk** (Not verified) | Funds in transit depend on the relayer / solver contracts. Include them in the custody and contract-risk analysis. |
| Para user-owned wallet (device share + Para HSM share), no permissions, no exported session | Member device + Para; neither alone | **Non-custodial (vendor-dependent)** | The device-held share gives the Member an independent factor (like Dynamic / Fireblocks NCW in note 02). |
| Para user-owned wallet + **standing-access permission** | Member, **or** the permitted party within Para's off-chain policy | **Hybrid** (who signs: Not verified) | Off-chain enforcement by Para. Combine with an on-chain session key, or avoid. |
| Para **imported session** on the platform server | Platform, for up to 30 days, apparently without scope | **Custodial in substance** | Equivalent to the platform holding the Member's signing power. Do not use for Member funds. |
| Para **REST / pregenerated wallets** (before claim) | Platform API key + Para enclave | **Custodial** | Operator-controlled until the user claims it. |
| Kernel weighted multisig / Safe as operator treasury | Operator approvers (threshold) | **Custodial (operator funds)** | Acceptable: treasury funds belong to the operator until Commissions are paid. |
| Pimlico / ZeroDev / Openfort paymaster or bundler | No signing authority over assets | n/a | Liveness dependency only. |

---

## 7. Comparison table (consistent with note 02 §5)

| Vendor | Key model | Platform can act for a Member? | Policy engine | AA (4337 / 7702) | Chains (incl. Hyperliquid) | Gas sponsorship | On-ramp | SOC 2 | Key export | Corporate status (Oct 2026) |
|---|---|---|---|---|---|---|---|---|---|---|
| **Openfort** | 2-of-3 Shamir (device, auth share on Openfort servers, recovery); backend wallets in a GCP TEE; OpenSigner self-hostable | Yes: backend wallet as EIP-7715 on-chain session signer (contract scope, expiry, call limit) | Off-chain, default-deny (backend signing + sponsorship) (Verified docs); on-chain session limits (Verified docs) | Both: own 4337 account + Calibur 7702 (Verified docs); 7579 NV | 9 EVM mainnets + Solana; **HyperEVM not supported**; HyperCore recipes, policy all-or-nothing (Verified docs) | Own paymaster, 10% / 5% surcharge (Verified) | Coinbase, Stripe named; full list NV | **NV** (5 audits, VC) | Yes (VC) | Independent: Alamas Labs Inc. (Verified); AUP bans "Ponzi or pyramid schemes" |
| **ZeroDev** | Signer-agnostic (ECDSA, passkey, multisig, Turnkey / Privy / Para); ZeroDev Wallet key model NV | Yes: agent-created on-chain session keys with call / timestamp / rate-limit policies (Verified docs) | On-chain (Kernel permissions) + off-chain gas policies (Verified docs) | Both; Kernel v4 = 4337 + 7579 + 7702 (Verified GitHub) | 50–130+ chains (VC); **HyperEVM listed** (Verified docs); HyperCore NV | Own paymaster, 8% premium (Verified) | No fiat on-ramp; Smart Routing Address (VC) | **NV**; Kernel v3.x audits published (Verified files) | ZeroDev Wallet export (VC); Kernel portable across bundlers (Verified) | **Offchain Labs product** (Verified via ToS); acquisition details NV |
| **Para** | 2-of-2 DKLS19 MPC (device share + Para HSM share) (VC) | Yes: Transaction Permissions "standing access" (GA 2026-09-24; signer NV); also session export / REST wallets (platform-controlled) | Off-chain, Para-enforced; spend windows, recipients, ERC-20 caps (Verified docs) | Signer only; via ZeroDev / Alchemy / Safe / Pimlico (Verified docs) | "All EVM chains", Solana, Cosmos, Stellar, Sui (VC); **HyperEVM NV** | **None native** (Verified docs) | Ramp, Stripe, MoonPay, Coinbase (Verified docs) | Type II (VC) | Yes, full key (VC) | Independent: Capsule Labs Inc., a16z-backed (VC) |
| **Pimlico** | None (infrastructure) | n/a (account modules) | Sponsorship policies (off-chain) | 4337 bundler / paymaster; 7702 on some chains, **not HyperEVM** (Verified docs) | 100+ chains; **HyperEVM v0.6 / v0.7** (Verified docs) | Yes, 10% surcharge (Verified) | None | Type 1 (VC) | n/a | Independent: Austerlitz Labs Ltd, UK (Verified) |
| *Benchmark:* **Turnkey + Alchemy** | Nitro enclaves (Turnkey) + MAv2 account | Yes: Turnkey scoped API key + Alchemy on-chain session keys | Turnkey off-chain (very granular) + on-chain session keys (Verified docs) | 7702 default; MAv2 (ERC-6900) | EVM, Solana, Hyperliquid (Turnkey, VC); HyperEVM paymaster via Alchemy per Privy recipe | Alchemy, 8% fee; Turnkey Enterprise | Not core | Turnkey Type II (VC); Alchemy NV | HPKE (VC) | Both independent |
| *Benchmark:* **Privy** | TEE + 2-of-2 Shamir | Yes: signers with Earn-specific override policies | TEE-enforced; Enterprise | Both | Broad; HyperCore + HyperEVM recipes | Native on ~27 chains; HyperEVM via third party | Stripe (default), MoonPay, Meld; Bridge fiat (MLM-prohibited) | Type I / II (VC) | Yes (VC) | Stripe-owned |

VC = Vendor claim; NV = Not verified.

**Requirement fit summary (Assumption, from the evidence above):**

| Requirement | Openfort | Turnkey + ZeroDev | Para (+ smart-account partner) | Turnkey + Alchemy |
|---|---|---|---|---|
| 1. Member-owned embedded wallet | Yes (prefer passkey / password recovery) | Yes (Turnkey) | Yes (strongest Member independence: device share) | Yes |
| 2. Scoped platform key: vault deposit only, cap, expiry, no transfer | Yes, on-chain (EIP-7715); argument-level `receiver` check NV | **Yes, on-chain, argument-level conditions documented** | Off-chain only from Para; on-chain via partner | Yes, on-chain |
| 3. Gas sponsorship | Yes (own) | Yes (own) | Partner | Yes |
| 4. Treasury multi-approval | Not found; use Safe | Weighted multisig (unaudited NV), or Safe / Turnkey quorum | Human approvals (VC); quorum NV | Turnkey quorum / Safe |
| 5. HyperEVM | **No** | **Listed** | NV | Via Alchemy (Privy recipe) |
| 6. No MLM-hostile parent | Independent; AUP wording risky | Offchain Labs; reputational-termination clause | Independent; on-ramps include Stripe / Coinbase | Independent |

---

## 8. Pricing evidence (USD unless stated; research date 2026-10-06)

| Vendor | Public pricing (verified) | Quote required | Source |
|---|---|---|---|
| Openfort | Free $0 (2,000 operations, rate-limited; $0.01 overage; 10% paymaster surcharge); Growth $99/month (25,000 ops; $0.008; 10%); Pro $249/month (100,000 ops; $0.006; 5%); Scale $599/month (500,000 ops; $0.004; 5%) | Enterprise (1M+ ops/month or self-hosted; SLA; self-hosted key management) | [pricing](https://www.openfort.io/pricing) |
| ZeroDev | Sandbox $0 (10,000 credits, testnet only); Launch $69/month (100,000 credits, mainnet); Scale $399/month (1,000,000 credits); wallet signature = 10 credits, UserOp = 20 credits; gas sponsorship premium 8%; Chain Abstraction SDK 10–20 bps | Enterprise; Smart Routing Address ("Contact us"); remote key storage (paid add-on) | [pricing](https://zerodev.app/pricing), [key storage](https://docs.zerodev.app/advanced/key-storage) |
| Para | Free (up to 1,200 MAU); Starter $200/month (2,500 MAU, $0.06/extra MAU); Growth $500/month (10,000 MAU, $0.05); Scale $1,000/month (25,000 MAU, $0.04); "No setup fees or per-transaction charges" | Enterprise; tier for Transaction Permissions NV; gas via partner | [pricing](https://www.getpara.com/pricing) |
| Pimlico | Pay-as-you-go $0/month (card required; 10,000,000 credits; $1 per 100,000 extra credits; ~$0.0075 per UserOp, ~$0.0105 sponsored; 10% mainnet sponsorship surcharge) | Enterprise (lower rates, SLA, ERC-20 gas in 300+ tokens) | [pricing](https://www.pimlico.io/pricing) |
| *Benchmarks (from note 02 §8)* | Turnkey: 25 free signatures then $0.10; Pro $99/month at $0.05. Alchemy: $0.525 per 1M CU, 8% gas fee. Privy: $299 / $499 / PAYG tiers. | Turnkey Enterprise; Alchemy wallet pricing; Privy Enterprise | note 02 §8 |

**Consultant note (Assumption, not vendor pricing):**

- Self-serve credits translate into roughly 10,000 sponsored UserOps per month on ZeroDev Launch (100,000 credits ÷ 20 per UserOp, with no signature credits counted) and 25,000 operations on Openfort Growth. How each vendor defines an "operation" differs and must be confirmed before any cost comparison.
- Gas itself is pass-through plus the surcharge (Openfort 5–10%, ZeroDev 8%, Pimlico 10%, Alchemy 8%, Coinbase 7% per note 02).
- Para's MAU pricing is higher per Member than Turnkey's per-signature model at low activity. It is lower if Members transact often. Budget ranges belong in the cost workstream.

---

## 9. Risks

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| S1 | Openfort's AUP ban on "Ponzi or pyramid schemes" and unlicensed "securities" or "money services" is applied to an MLM-distributed Yield Product. | High | Written clearance before build. Keep it ranked below Turnkey + ZeroDev / Alchemy. |
| S2 | Offchain Labs exercises the §9.2 "material harm to the reputation of Offchain" termination right, or Arbitrum-centric priorities change ZeroDev's roadmap. | Medium–High | Written confirmation. Design for bundler / paymaster portability (Kernel is MIT and works with Pimlico / Alto). Keep Alchemy as a ready alternative. |
| S3 | Kernel v4 is unreleased / has no published audit; the weighted multisig validator has no audit evidence. | Medium | Use audited Kernel v3.3 until a v4 report is reviewed. Use Safe (audited) for the treasury. |
| S4 | Session-key revocation races in-flight bundles (TOB-KERNEL-3). The same class of issue probably applies to other 4337 accounts (Assumption). | Medium | Short expiries. Low per-period caps. Monitoring and kill switch (revoke + pause the signer in Turnkey). |
| S5 | Openfort automatic recovery lets the platform and Openfort together reach the key threshold. | High (for custody claims) | Use passkey or password recovery for Member wallets. Classify honestly. |
| S6 | Para server paths (REST wallets, imported sessions of up to 30 days) are used for convenience and make the model custodial in substance. | High | Prohibit them for Member funds in the design. Use on-chain session keys instead. |
| S7 | HyperEVM sponsorship gaps: Openfort none; Pimlico without 7702; ZeroDev per-mode coverage NV. | Medium | Confirm with ZeroDev. Keep Pimlico v0.7 as a fallback paymaster. Treat HyperEVM as phase 2. |
| S8 | On-ramp routes bundled by Openfort and Para include Stripe and Coinbase (MLM-restricted per note 02). | Medium | Disable those routes. Source the on-ramp from the fiat workstream. |
| S9 | Cross-chain Earn / Smart Routing relayer legs add contract and counterparty risk outside the Member's account. | Medium | Same-chain vault deposits only in release 1. Review the relayer contracts and audits. |
| S10 | No SOC 2 evidence for Openfort or ZeroDev; Pimlico Type 1 only; Para Type II unverified. | Medium | Obtain reports under NDA during procurement. |

---

## 10. Open questions for vendors

**All four (Openfort, ZeroDev / Offchain Labs, Para, Pimlico)**

1. Will you onboard a business that distributes a lending-based Yield Product through an MLM network? Does your AUP or termination clause (Openfort "pyramid schemes"; Offchain §9.2 reputational harm) apply?
2. SOC 2 report (type, auditor, period) and the most recent penetration-test summary.

**Openfort**

1. Can the EIP-7715 permission check calldata arguments, for example ERC-4626 `deposit(assets, receiver)` with `receiver == account` and an `assets` cap? Are cumulative caps supported?
2. With automatic recovery, can Openfort and the developer together reconstruct a key without the user? Can passkey-only recovery be enforced project-wide?
3. Is there a quorum or multi-approval option for backend wallets (treasury)?
4. HyperEVM roadmap (bundler and paymaster). HyperCore policy granularity (distinguish withdrawals from orders).
5. Full funding-provider list. Can Stripe and Coinbase routes be disabled?
6. Ownership, funding and headcount. Smart-account audit report access (CertiK, Omniscia, Quantstamp).

**ZeroDev / Offchain Labs**

1. Acquisition date and structure. Is ZeroDev a separate legal entity or a division? Will the service and terms stay as they are?
2. Kernel v4 audit reports (Trail of Bits?) and Certora results. Recommended production version.
3. HyperEVM: bundler and paymaster availability for 7702 mode and 4337 mode, and on which EntryPoint version.
4. ZeroDev Wallet key infrastructure (TEE / MPC / third party) and who can sign.
5. Earn (Beta): fees or revenue share, same-chain vs cross-chain execution, relayer custody model, and use with session keys.
6. Cumulative (rolling) spend limits for Call Policy. Audit status of the weighted multisig validator.

**Para**

1. Under Transaction Permissions "standing access", which party produces the signature (Para enclave with a server-held share? the app?), and where is that share stored?
2. Which plan includes Transaction Permissions? Do they support calldata-argument conditions and absolute expiry?
3. What can an imported session sign? Can permissions constrain it?
4. HyperEVM support and HyperCore action decoding.
5. SOC 2 Type II report and Least Authority audit reports.

**Pimlico**

1. EIP-7702 and EntryPoint v0.8 on HyperEVM: timeline.
2. SOC 2 Type 2 timeline.

---

## 11. Evidence limitations

- **No web search was available** (quota exhausted). All evidence comes from fetching official URLs directly. Press coverage of the ZeroDev / Offchain Labs deal was not checked, so the acquisition date and terms remain **Not verified**. The operator relationship is verified from the ToS and offchain.io.
- **Pages were read through a fetch-and-summarise tool**, not in a browser. Quoted passages are as returned by that tool. The quotes material to the recommendation (Openfort AUP bullets, ZeroDev ToS §1, §2.5, §9.2, Para REST "enclave holds the key material") were requested verbatim, but should be re-checked against the live page before they are relied on in a client deliverable.
- **No audit PDF or SOC 2 report was opened.** ZeroDev's audit files were confirmed present on GitHub but not read. Openfort's reports sit in a Google Drive folder that was not accessed.
- Some pages did not render or returned 404: [chains.zerodev.app](https://chains.zerodev.app/), `getpara.com/security`, `getpara.com/blog` (the blog lives at blog.getpara.com), `openfort.io/about`, ZeroDev 7702 docs at an old path. Facts that depended on them are marked **Not verified**.
- Each vendor's product terms were checked. Order forms, enterprise MSAs and any separate KYB policies were not available.
- ZeroDev scale figures are inconsistent between the homepage and the docs. Both are reported as Vendor claims.
- Pricing pages change often. All figures were captured on 2026-10-06.
