# Helm Phase 0

Helm is the AlphaWave member platform. Phase 0 lets Members join through referrals, fund a wallet with crypto, participate in an approved vault and engage through games and points, while recording the full referral genealogy for Phase 1 compensation.

## Parties and systems

**Cyclone**:
The implementation company that builds the Helm Web App and integration backend.

**Helm Web App**:
The custom member and admin application, with its backend, that integrates the confirmed providers.

## Members and genealogy

**Member**:
A person with one stable Helm member ID, regardless of how many provider accounts or wallets are linked to it.
_Avoid_: User, account, affiliate, distributor

**Sponsor**:
The Member who introduced another Member, recorded once at acceptance.
_Avoid_: Upline (as a synonym), referrer

**Sponsor Edge**:
One accepted Sponsor → Member relationship, with provenance and effective time.

**Genealogy**:
The complete graph of accepted Sponsor Edges at every depth, independent of how many levels pay Commissions.
_Avoid_: Downline (as the whole graph), tree (when depth-limited)

**Referral Request**:
A proposed sponsor relationship captured at signup that is not yet accepted into the Genealogy.

## Money and value

**Wallet Funding**:
A transfer of a supported crypto asset into a Member's wallet. It is not an investment and creates no Commission eligibility.
_Avoid_: Deposit (unqualified), top-up

**Vault Deposit**:
A Member's confirmed deposit of an approved asset into the approved vault, in exchange for vault shares.
_Avoid_: Investment, staking

**Redemption**:
A Member's withdrawal of value from the vault by returning vault shares, following the vault's actual rules and stages.
_Avoid_: Unstaking, withdrawal (when the wallet is meant)

**Vault Position**:
The vault shares a Member holds, as established on-chain.

**Commission**:
A payment to a Member calculated from Genealogy activity under an approved compensation plan. Not assumed for Phase 0.

**Points**:
Non-cash engagement credits from the game and points system. Points are not money, vault shares or Commissions.
_Avoid_: Rewards (when money is meant), tokens

**Yield Product**:
Any product offering a return on deposited assets; the vault's strategy determines what kind.
_Avoid_: Staking (as a generic term)
