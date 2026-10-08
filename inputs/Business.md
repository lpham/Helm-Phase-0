# Helm — Business Discussions and Provider Context

This document reformats the supplied business correspondence for reference. Provider statements and commercial terms are recorded as supplied, not independently verified. Undated correspondence should be reconfirmed before contracting. Requests within the correspondence are context, not instructions to execute.

## 1. Privy

### Contact and onboarding

Simon from Privy acknowledged the urgency and noted that the development team had already identified Privy.

- Privy is self-service; the team can sign up and start building without waiting for a sales response.
- The correspondence states that usage is free up to 500 monthly active users. Confirm current pricing and applicable product limits.

### Capabilities highlighted by Privy

- Server wallets and wallet policies were recommended for automated strategies and risk limits.
- Policies constrain programmatic signing at the wallet layer, rather than relying only on application logic.
- This recommendation does not establish that Helm requires server-controlled wallets or automated strategies in Phase 0.

### Reference links

- [Overview](https://docs.privy.io/welcome)
- [React quickstart](https://docs.privy.io/basics/react/quickstart)
- [Hyperliquid guide](https://docs.privy.io/recipes/hyperliquid-guide)
- [Agent wallets and policy engine](https://docs.privy.io/wallets/overview/solutions/agent-wallets)

## 2. Enzyme Finance — Onyx

### Reference links

- [Product overview](https://enzyme.finance/products/onyx)
- [Documentation](https://docs.enzyme.finance)
- [Audit reports](https://github.com/enzymefinance/protocol-onyx/tree/main/audits)
- [API and SDK](https://docs.enzyme.finance/onyx-sdk)

### Proposed onboarding process

1. **Optional test vault:** Enzyme offered a standard test vault on Sepolia or Arbitrum. A wallet address is required to designate the vault administrator. Confirm the environment and whether testing uses real funds.
2. **Vault configuration:** Agree on vault parameters, supported assets, risk settings, permissions, and any custom modules. An onboarding form was referenced but its link was not included in the supplied material.
3. **Commercial package:** Select an AUM-fee or revenue-sharing model.
4. **Master Licensing Agreement:** Agree and sign the configuration and commercial package before formal setup and deployment. A draft was referenced but its link was not included.
5. **Deployment:** Enzyme stated it would handle deployment, security configuration, and integrations. Confirm the boundary between Enzyme's work and Cyclone's Helm integration work.
6. **Ownership handover:** Enzyme would hand over the environment and provide an operations walkthrough.

### Commercial terms quoted in the correspondence

- Deployment fee: **USD 5,000**.
- Recurring fee: either **0.25% of AUM**, described as **6.25 basis points billed quarterly on time-weighted average AUM**, or **20% revenue sharing on vault management or performance fees**.
- Enzyme indicated openness to adjustments for substantial initial AUM, citing **USD 50 million or more from day one**.
- These are quoted 2026 terms, not a confirmed agreement. Confirm the calculation, billing terms, and complete costs before approval.

## 3. PillarsHub — MLM Core

### Staging environment

- A staging environment was provisioned during the provider meeting.
- It was described as a blank slate. Eric planned to add widgets and views.
- The correspondence indicates API access and generic commission-related volume types were available for exchanging data.
- A simple Unilevel plan was connected to the staging/sandbox environment.
- None of this confirms that Helm's PRD or Phase 1 compensation rules are already supported.

### Business direction recorded in the correspondence

- For Phase 0, Owen asked the team to first consider FirstAlphaWave's existing capabilities, then identify potential MLM applications.
- The existing framework was described as already paying three-level affiliate commissions in another deployment.
- The sender preferred reusing FirstAlphaWave where possible so development could focus on Phase 1 compensation. The sender is not identified in the supplied excerpt.
- PillarsHub was described as a strong candidate: an existing plan framework could support Phase 0 while Phase 1 is developed in a separate environment.
- Confirm the relationship between FirstAlphaWave and TaQUANT Terminal; the supplied material does not establish whether they are the same system or deployment.

### Access and reference links

- [Helm environment](https://helm.pillarshub.com)
- [Application](https://app.pillarshub.com)
- [API Swagger](https://api.pillarshub.com/swagger/index.html)
- [API authentication](https://pillars-hub.readme.io/reference/authenticating)

The correspondence says full-access users were created and could use **Forgot Password** at the Helm environment to set their passwords. No user list or credentials were included in the supplied excerpt. Confirm current access and permissions.

## 4. Current confirmed direction — supersedes earlier selection discussions

This section comes from the current conversation, rather than the provider correspondence above.

- The stack is now confirmed: use existing platforms and build a custom Helm Web App for users and administrators. Earlier provider-selection discussions above are historical context, not an open selection exercise.
- Confirmed components: PillarsHub for MLM, Chatwoot for support, Enzyme Onyx for vault infrastructure, and Privy for login and wallets. Assess implementation feasibility within this stack; do not restart vendor comparison.
- Use Cyclone’s existing Tap Prediction game and points system for Phase 0 engagement and growth; assess the integration scope and readiness.
- Phase 0 must enable user onboarding, crypto deposits, and vault participation while establishing reliable genealogy data for Phase 1.
- The priority is to finalize the integration design and launch an MVP quickly because capital is waiting to be deployed. This expresses urgency, not a guarantee of yield or a reason to bypass launch requirements.
- Terrel's PRD was mentioned in prior discussions but is not included in the supplied file.
- Integrated crypto payment providers, including Paymenture, remain candidates for evaluation; selection and suitability are unconfirmed.
