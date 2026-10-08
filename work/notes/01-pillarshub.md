# 01 — PillarsHub (MLM core): integration feasibility

- **Project:** Helm Phase 0 (Cyclone for AlphaWave)
- **Workstream:** Member identity in the MLM core, Sponsor Edges and Genealogy, compensation-plan fit, volume events, sync and reconciliation
- **Verification date:** 2026-10-08 (all "Verified capability" items below were read on this date)
- **Method:** Public documentation only. No login, sign-up, access request or API call with credentials. WebSearch was unavailable. Pages were read with WebFetch and plain HTTPS GET.

**Evidence labels**
- **Verified capability:** read directly in PillarsHub's own public documentation or published OpenAPI (Swagger) specification on 2026-10-08, with the URL. A field or endpoint in the specification proves that the interface exists. It does not prove how it behaves at runtime.
- **Provider correspondence:** stated in `inputs/Business.md`. Not verified.
- **Recommended design:** Cyclone's proposal.
- **Assumption/TBD:** not evidenced. Must be confirmed in staging or by PillarsHub.

Glossary terms used: **Member**, **Sponsor**, **Sponsor Edge**, **Genealogy**, **Referral Request**, **Vault Deposit**, **Wallet Funding**, **Commission**, **Points**, **Helm Web App**, **Cyclone** (see `GLOSSARY.md`). PillarsHub's own words are kept where quoted: "customer", "node", "tree", "enroller", "upline", "placement", "source", "bonus".

### Primary sources read

| Source | URL | Notes |
| --- | --- | --- |
| Swagger UI and its config | https://api.pillarshub.com/swagger/index.html, https://api.pillarshub.com/swagger/index.js | `index.js` lists 8 specifications. `/swagger/v1/swagger.json` returns 404. |
| OpenAPI specs (live) | `https://api.pillarshub.com/swagger/{CommissionV1,CustomerV1,AutoshipV1,InventoryV1,OrderV1,ReportV1,AccessControlV1,WebHookV1}/swagger.json` | All 8 downloaded (HTTP 200). They are the basis of the endpoint inventory. Each spec has one server, `https://api.pillarshub.com` ("Production Api Server"), and a `Bearer` apiKey scheme in the `Authorization` header. |
| Docs index | https://pillars-hub.readme.io/llms.txt | Full page list. Each page is also available as `.md`. |
| Auth and tokens | https://pillars-hub.readme.io/reference/authenticating, `/reference/access-control-tokens`, `/reference/managing-access-tokens`, `/reference/generating-an-access-token`, `/reference/keeping-your-api-credentials-secure`, `/reference/managing-user-tokens`, `/reference/single-sign-on` | |
| Webhooks | https://pillars-hub.readme.io/reference/getting-started-webhooks, https://pillars-hub.readme.io/reference/topics | |
| Guides and knowledge base | `/docs/introduction`, `/docs/step-2-creating-your-environment`, `/docs/step-3-configuring-your-environment`, `/docs/step-4-begin-using-your-environment`, `/docs/post-put-or-patch`, `/docs/invoice-dates-are-used-to-calculate-commissions`, `/docs/consider-using-an-inactive-tree-to-manage-long-term-absences`, `/docs/pillars-launch-timing-protocol`, `/docs/instantly-eliminate-duplicate-account-confusion`, `/docs/customer-fields`, `/docs/money-out-merchant-integration-guide`, `/docs/paymenture-tygapay` (all under https://pillars-hub.readme.io) | |
| Product and legal | https://www.pillarshub.com/ (and `/features`, `/faqs`, `/services`, `/integrations`, `/about-us`, `/terms`, `/privacy`) | `/pricing` and `/security` return 404. |

---

## 1. Summary

### What is verified

1. **Server-to-server authentication works with environment-bound Access Tokens.** The client sends `Authorization: Bearer {TOKEN}` to `https://api.pillarshub.com/api/v1/`. Access Tokens are created in the Pillars Portal per Application Environment. They "do not expire", "are never tied to a user" and "are always associated with an environment". A token can be created as Read Only. Tokens carry **Access** (permissions), an **Environment** and a **Scope** ("limited to a Node and its downline"). **Verified capability** ([authenticating](https://pillars-hub.readme.io/reference/authenticating), [access-control-tokens](https://pillars-hub.readme.io/reference/access-control-tokens), [generating-an-access-token](https://pillars-hub.readme.io/reference/generating-an-access-token), 2026-10-08).
2. **Sandbox and production are separate Application Environments on the same API host.** The token selects the environment. "Additional Environments can serve as sandboxes" ([step-2](https://pillars-hub.readme.io/docs/step-2-creating-your-environment), 2026-10-08). **Verified capability**.
3. **The customer record has a client-settable `id`, an `externalIds` array, `enrollerId`, `signupDate`, `status` and `customData`** in `CustomerCreate`. `CustomerUpdate` (PUT/PATCH) **does not contain `enrollerId`**. **Verified capability** (CustomerV1 spec, 2026-10-08).
4. **Genealogy is held as trees of nodes with an `uplineId` and dates.** Nodes have `nodeId`, `uplineId`, `uplineLeg`, `effectiveDate` and `placeDate`. Nodes can be listed for a whole tree with `offset`/`count` and an as-of `date`. `downline` is capped at **`levels` 1–10**. `upline` has no levels parameter. A separate **Placements** resource keeps dated `nodeId → uplineId` records. The marketing site claims "Time Travel Auditing … the entire historical tree structure at any point in time". **Verified capability** (CommissionV1 spec; [pillarshub.com](https://www.pillarshub.com/), 2026-10-08). The marketing claim is the vendor's own statement.
5. **Payable depth is a property of the compensation plan, not of the tree.** `BonusDefinition` → `generationBonuses[]` has `generation`, `percent` and `compressionKey`, and points to a `treeId`. The plan can be read through the API (`GET` only) but not written. **Verified capability** (schema, CommissionV1, 2026-10-08). That a tree can store unlimited depth while the plan pays 3 levels is a reasonable reading of the schema. **Assumption/TBD** until it is tested in staging.
6. **Custom volume events are supported through Source Groups and Sources.** Source Groups are created or updated with `PUT /api/v1/SourceGroups/{sourceGroupId}` (`sourceType`: `SumValue`/`LastValue`/`BonusOverride`; `dataType`: `Integer`/`Decimal`/`DateTime`/`String`). A Source requires `nodeId`, `sourceGroupId`, `date` and **`externalId`**. `POST /api/v1/Sources` documents a **409 Conflict** response. Sources can be queried by `externalId` and deleted. **Verified capability** (CommissionV1, 2026-10-08). This matches "generic commission-related volume types" in **Provider correspondence**. Orders, with `lineItems[].volume[]` and `invoiceDate`, are a second volume path. Commissions are calculated "as soon as Pillars receives the Invoice Date" ([invoice-dates KB](https://pillars-hub.readme.io/docs/invoice-dates-are-used-to-calculate-commissions), 2026-10-08).
7. **Webhooks exist, but they are not signed.** Ten documented topic/subtopic pairs include `Customer/Created|Updated|Deleted` and `Node/Created|Updated`. Delivery headers include `x-webhook-messageid`. Failed deliveries are retried "for 2 days", and the subscription is disabled after "multiple days" without a 2xx response. A delivery log is exposed at `GET /api/v1/WebHooks/Messages`. **No signature or HMAC header is documented.** **Verified capability** ([getting-started-webhooks](https://pillars-hub.readme.io/reference/getting-started-webhooks), [topics](https://pillars-hub.readme.io/reference/topics), 2026-10-08).
8. **Payouts are a separate step that Phase 0 can avoid.** Paying out requires releasing bonuses (`PUT /api/v1/Bonuses/Release`), payout batches (`/api/v1/Batches…`, NACHA), and a Money-Out integration (Paymenture/TygaPay, PayQuicker, MassPay or a custom merchant) configured in the Portal. Customer statuses carry `earningsClass` `Release`/`Hold`/`Forfeit`. **Verified capability** (CommissionV1, CustomerV1; [money-out guide](https://pillars-hub.readme.io/docs/money-out-merchant-integration-guide), [paymenture-tygapay](https://pillars-hub.readme.io/docs/paymenture-tygapay), 2026-10-08).

### What is not verified

- Whether `enrollerId` on customer create automatically places a node in the Unilevel tree, and how `enrollerId` relates to node `uplineId`.
- Whether Sponsor changes are possible through the API in practice, and how tree movement settings constrain them.
- What a 409 on Sources means. It is probably a duplicate `externalId`, but that is not documented.
- Whether creating a customer with an existing `id` is rejected.
- Whether negative Source values are allowed.
- Rate limits and page-size maximums.
- Whether Access Token permissions can be set per area.
- Whether a GraphQL endpoint is available.
- Bulk import tooling.
- Certifications such as SOC 2 or ISO 27001. None were found.
- Pricing. It is not public.
- The configuration of the provisioned Helm staging environment. Not accessed, by instruction.

### Top risks

**Phase 0**

1. **Volume sent to PillarsHub can create commissions immediately.** Commissions are computed in real time. If Helm posts Vault Deposit volume into a source group that the Unilevel plan's bonuses use, "Pending Commissions" may appear in back-office widgets and reports. That could read as a payout obligation. Mitigation: post no commissionable volume in Phase 0, or post into a source group the plan does not use. Confirm with Business. See §5.
2. **No idempotency key and no webhook signing.** Duplicate-safe writes rely on Helm-assigned IDs and `externalId` lookups. Webhooks are delivered at least once and are unauthenticated, so they must be treated as hints only.
3. **Over-privileged token.** The API can delete trees, nodes, placements and customers. Setting status to Deleted "will permanently delete the record … cannot be undone by anyone" ([inactive-tree KB](https://pillars-hub.readme.io/docs/consider-using-an-inactive-tree-to-manage-long-term-absences), 2026-10-08). Least-privilege tokens are essential, but how granular token permissions can be is TBD.
4. **Launch scheduling.** Pillars launches clients only Tuesday–Thursday, 9:00–16:00 MT. Exceptions need approval by their CEO and CTO two weeks ahead and are charged at a RUSH rate ([launch protocol](https://pillars-hub.readme.io/docs/pillars-launch-timing-protocol), 2026-10-08). **Verified capability**. Plan the go-live date around this.

**Phase 1 readiness**

5. **Correctness of the full-depth export is unproven.** The tree node list plus the as-of `date` should give a complete edge list, but this must be tested at volume.
6. **Enroller vs placement semantics.** If Phase 1 adds a second tree (for example a binary tree), `enrollerId` and placement `uplineId` will diverge. Helm's Sponsor Edge must map to the right one.
7. **Terms of Service clauses.** The Terms say the Site "is not designed to comply with … the Gramm-Leach-Bliley Act (GLBA)", and they forbid "systematically retriev[ing] data … without written permission" ([terms](https://www.pillarshub.com/terms), 2026-10-08). The reconciliation mirror needs written confirmation that it is permitted, and legal should review the GLBA clause for a financial-product context.

---

## 2. Capability table

| # | Requirement (PRD §4/§6) | Evidence | Label | MVP impact |
| --- | --- | --- | --- | --- |
| 1 | Server-to-server API auth | `Authorization: Bearer {TOKEN}`; Access Tokens from the Portal are non-expiring, environment-bound and can be Read Only ([authenticating](https://pillars-hub.readme.io/reference/authenticating), [generating token](https://pillars-hub.readme.io/reference/generating-an-access-token)) | Verified capability | Feasible. Store in a secret manager. Rotation is manual (create new token, replace, delete old). |
| 2 | Least-privilege permissions | `Permissions` object with per-area `TokenAccess` (`NoAccess`, `FullAccess`, `ReadOnly`, `WriteOnly`, `ScopeAccess`) on Roles and `AuthToken.access` (AccessControlV1). The Portal UI only mentions a Read Only choice for Access Tokens. | Verified (schema); per-area control for Access Tokens is **Assumption/TBD** | If a token is either full or read-only, a write token can delete trees and customers. Ask PillarsHub; consider two tokens (read-only for reconciliation, write for sync). |
| 3 | Sandbox vs production | Multiple Application Environments; the token is bound to one; one host `api.pillarshub.com` ([step-2](https://pillars-hub.readme.io/docs/step-2-creating-your-environment)) | Verified capability | Feasible. Use separate tokens and config per environment. Staging is reportedly provisioned (Provider correspondence). |
| 4 | Stable member identity mapping | `CustomerCreate.id` (settable string), `externalIds[]`; `GET /api/v1/Customers/Find?search=…&externalIds=true` | Verified capability | Feasible. Map the Helm member ID (see §5). Whether a duplicate `id` is rejected is TBD. |
| 5 | Sponsor captured at signup | `CustomerCreate.enrollerId`; absent from `CustomerUpdate` | Verified (schema) | Feasible. Set the Sponsor at create time only. Auto-placement into the tree is **TBD**. |
| 6 | Controlled Sponsor change | `PUT /api/v1/Trees/{treeId}/Nodes/{nodeId}` (Node with `uplineId`); `POST /api/v1/Placements`; Tree settings `enableCustomerMovements`, `movementDurationInDays`, `maximumAllowedMovementLevels`, `enableHoldingTank` | Verified (interface); runtime effect TBD | Possible through the API, so it must be gated in Helm (admin-only, audited). PRD default "no self-service change" is enforceable in Helm. Turning off customer movements in PillarsHub is **Recommended design**. |
| 7 | Full-depth Genealogy stored | Trees/Nodes model with `uplineId`; no depth limit appears in the spec | Verified (schema); unlimited storage depth is **Assumption/TBD** | Ask PillarsHub to confirm there is no depth cap. Test 15+ levels in staging. |
| 8 | Full-depth Genealogy retrievable | `GET /api/v1/Trees/{treeId}/Nodes?date&offset&count` (whole tree, as of a date); `…/downline?levels` (1–10 max); `…/upline` (no depth parameter) | Verified capability | Export the full graph by paging all nodes, not with `downline`. Whether omitting `nodeIds` returns every node is TBD (test). |
| 9 | Historical Genealogy (point in time) | `date` query on Nodes; `Node.effectiveDate`/`placeDate`; `Placements?start&end`; "Time Travel Auditing" (marketing) | Verified (interface) + vendor claim | Supports Phase 1 snapshots. Helm should still keep its own Sponsor Edge history. |
| 10 | Commission depth independent of Genealogy | `BonusDefinition.generationBonuses[].generation`, `treeId`, `compressionKey`; plan read-only via `GET /api/v1/CompensationPlans…` | Verified (schema); independence **Assumption/TBD** | Configure the 3-level Unilevel in the PillarsHub UI or with the Pillars team, not through the API. |
| 11 | Plan configuration (unilevel, ranks) | Plan templates (Binary, Unilevel, Affiliate, custom) assigned per environment ([step-3](https://pillars-hub.readme.io/docs/step-3-configuring-your-environment)); `Rank`, `RankRequirements` schemas | Verified capability | A simple Unilevel plan on staging is **Provider correspondence**. Its contents are unverified. |
| 12 | Custom volume type (e.g. Vault Deposit) | `PUT /api/v1/SourceGroups/{sourceGroupId}`; `POST /api/v1/Sources` (`externalId` required) | Verified capability | Feasible. Whether it feeds commissions depends on plan `volumeKey` mapping (TBD). Phase 0 posting is a Business decision (§5). |
| 13 | Corrections / reversals / refunds | `DELETE /api/v1/Sources/{sourceId}`; Orders `PATCH`/`PUT`/`DELETE /api/v1/Orders/{id}`; `DELETE /api/v1/HistoricalValues/{id}` | Verified (interface) | Reversal by delete is available. Negative values, effect on closed periods and audit trail are **TBD**. |
| 14 | Idempotency | No Idempotency-Key in any spec. Docs: POST "is *not* idempotent"; PUT "*is* idempotent" ([post-put-or-patch](https://pillars-hub.readme.io/docs/post-put-or-patch)). Sources POST returns 409 (meaning undocumented). | Verified (absence of key); 409 semantics TBD | Use Helm-assigned IDs plus lookup-before-retry (§5). |
| 15 | Notifications | Webhook topics `Customer`, `ValueUpdated`, `BonusEarned`, `Order`, `OrderStatusUpdated`, `Node` ([topics](https://pillars-hub.readme.io/reference/topics)); retries for 2 days; `x-webhook-messageid` for deduplication; no signature documented | Verified capability | Use as an optional trigger. Polling and reconciliation stay authoritative. |
| 16 | Pagination | `offset`/`count` (int32) on list endpoints; reports return `totalRows` and `moreRows` | Verified capability | Feasible. Maximum `count` is TBD. |
| 17 | Rate limits | Only throttling of repeated failed authentication is documented ([authenticating](https://pillars-hub.readme.io/reference/authenticating)); the Portal shows request counts and response times ([introduction](https://pillars-hub.readme.io/docs/introduction)) | Partially verified; numeric limits **TBD** | Use client-side backoff on 429/5xx. Ask PillarsHub. |
| 18 | Bulk import of existing members | No bulk customer or node endpoint. Per-record `POST /api/v1/Customers` (settable `id`, `signupDate`, `enrollerId`); `PUT …/Nodes/{nodeId}` (with dates); `POST /api/v1/HistoricalValues`, `POST /api/v1/HistoricalBonuses` | Verified (absence of bulk API in spec) | Import record by record, Sponsors first. PillarsHub may offer assisted migration ("migration of your existing data", [FAQ](https://www.pillarshub.com/faqs)). Not needed if Phase 0 starts empty. |
| 19 | Exports and reporting | `GET /api/v1/Reports/{reportId}/json|csv|pdf`; "25 standard reports", "Custom Reports Builder … GraphQL reports" ([features](https://www.pillarshub.com/features)) | Verified capability | Use for operations. Helm's reconciliation uses the raw Nodes and Sources APIs. |
| 20 | Avoid payouts in Phase 0 | Release, batch and money-out integrations are separate; `earningsClass` `Hold`/`Forfeit` on statuses | Verified capability | Feasible: do not connect a Money-Out integration, deny `bonuses`/`batches` to Helm's token, and decide whether bonuses accrue at all. |
| 21 | Member SSO to PillarsHub back office | `GET /Authentication/UserToken?username=` with Access Token; `https://app.pillarshub.com?token={userToken}` ([single-sign-on](https://pillars-hub.readme.io/reference/single-sign-on)) | Verified capability | Not needed in Phase 0. If used later, note that the token travels in the query string. |
| 22 | Security docs / certifications | Security guidance for tokens only; Azure hosting ([money-out guide](https://pillars-hub.readme.io/docs/money-out-merchant-integration-guide)); data "processed in the United States" ([terms](https://www.pillarshub.com/terms)); no SOC 2/ISO page found; `/security` 404 | Not verified | Request security documentation before production. Holding PII plus referral data is a compliance item. |
| 23 | Pricing | No public pricing (`/pricing` 404) | Not verified | TBD. Contract item. |

---

## 3. Endpoint inventory (as published in the live Swagger specs, 2026-10-08)

Base URL: `https://api.pillarshub.com`. Every operation uses `Authorization: Bearer …`. The specs contain no summaries or descriptions, so the semantics are inferred from names and schemas only. Only endpoints relevant to Helm are listed. Inventory, Autoship, Tax, Appointments, Documents and Products endpoints exist but are out of scope.

### Access Control (`/swagger/AccessControlV1/swagger.json`)
| Method | Path | Relevance |
| --- | --- | --- |
| GET | `/Authentication/token/{token}` | Validate a token (also used to validate money-out callbacks). Returns `AuthToken {token, environmentId, scope, access}` |
| GET | `/Authentication/token/{token}/Environments` | List environments for a token |
| GET | `/Authentication/refresh/{token}` (`environmentId`) | Refresh a User Token |
| GET | `/Authentication` (`username`, `password`, `environmentId` as **query parameters**) | User login. **Helm should not use it** (credentials in the URL). |
| GET | `/Authentication/UserToken` (`username`) | Server mints a User Token for a customer-associated user (needs an Access Token). Not for admins. |
| GET | `/Authentication/GetAuthorizationCode`, `/Authentication/AuthorizeCode` | Code-based token exchange (undocumented behaviour) |
| GET/POST, GET/PUT/DELETE | `/api/v1/Roles`, `/api/v1/Roles/{id}` | Roles with `Permissions` |
| GET, GET/POST, GET/PUT/DELETE | `/api/v1/Users/Find`, `/api/v1/Users`, `/api/v1/Users/{id}` | Back-office users |

### Customers (`/swagger/CustomerV1/swagger.json`)
| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/v1/Customers/Find` | `search` (required), `count`, flags `externalIds`, `fullName`, `phoneNumbers`, `emailAddress`, `webAlias` |
| GET | `/api/v1/Customers` | `ids[]`, `offset`, `count` |
| POST | `/api/v1/Customers` | Body `CustomerCreate`: `id`, `externalIds[]`, `customerType`, `signupDate`, `status`, `enrollerId`, names, `emailAddress`, `customData`, … → 201 `Customer` / 400 |
| GET / PUT / PATCH / DELETE | `/api/v1/Customers/{id}` | PUT body `CustomerUpdate` (no `enrollerId`); PATCH body `{operations:[{op,path,from,value}]}` |
| GET/POST, GET/PUT/DELETE | `/api/v1/Statuses`, `/api/v1/Statuses/{statusId}` | `Status {id, name, statusClass: Active|Inactive|Deleted, earningsClass: Release|Hold|Forfeit, treeSettings[{treeId, compress}]}` |
| GET/POST, PUT/GET | `/api/v1/Batches`, `/api/v1/Batches/{id}` | Payout batches. Also `POST /api/v1/Batches/Create`, `POST /api/v1/Batches/validate`, `POST /api/v1/Batches/{id}/process`, `GET /api/v1/Batches/{id}/Nacha`, `GET|PUT /api/v1/Batches/Settings`. **Out of Phase 0.** |

### Commission service: Genealogy, volume and plan (`/swagger/CommissionV1/swagger.json`)
| Method | Path | Notes |
| --- | --- | --- |
| GET / POST | `/api/v1/Trees` | `Tree {id, name, buildPattern, buildRule, legNames, legVolumeKey, requiredValue, isPrivate, enableCustomerLegPreference, enableHoldingTank, holdingTankDurationInDays, enableCustomerMovements, customerMovementWarning, customerMovementConfirmation, movementDurationInDays, maximumAllowedMovementLevels}`. POST → 202 |
| GET / PUT / PATCH / DELETE | `/api/v1/Trees/{treeId}` | Tree config. **Deny writes to Helm.** |
| GET | `/api/v1/Trees/{treeId}/Nodes` | `nodeIds[]`, `date`, `offset`, `count` → `[Node {nodeId, uplineId, uplineLeg, effectiveDate, placeDate}]` |
| GET / PUT / DELETE | `/api/v1/Trees/{treeId}/Nodes/{nodeId}` | GET supports `date`. PUT body `Node` → 201 |
| DELETE | `/api/v1/Trees/{treeId}/Nodes/{nodeId}/compress` | Remove and compress |
| GET | `/api/v1/Trees/{treeId}/Nodes/{nodeId}/downline` | `levels` **required, min 1, max 10**, `offset`, `count` → `[NodeL {…, level}]` |
| GET | `/api/v1/Trees/{treeId}/Nodes/{nodeId}/upline` | → `[Node]` |
| GET / POST | `/api/v1/Placements` | GET filters `nodeId`, `uplineId`, `start`, `end`. POST body `Placement {nodeId*, uplineId*, date}` → 201 |
| GET / DELETE | `/api/v1/Placements/{placementId}` | |
| GET | `/api/v1/NodeSettings`, `/api/v1/NodeSettings/{nodeId}`; PUT `/api/v1/NodeSettings/{nodeId}` | `treePreferences[{treeId, buildRule, holdingTank}]` |
| GET | `/api/v1/SourceGroups` | |
| GET / PUT / DELETE | `/api/v1/SourceGroups/{sourceGroupId}` | PUT body `SourceGroup {id, sourceType*: SumValue|LastValue|BonusOverride, dataType: Integer|Decimal|DateTime|String, acceptedValues[]}` → 202. No POST exists. |
| GET | `/api/v1/Sources` | Filters `sourceIds[]`, `nodeId`, `sourceGroupId`, `externalId`, `start`, `end` |
| POST | `/api/v1/Sources` | Body `Source {nodeId*, sourceGroupId*, date*, externalId*, value, uplineId, postDate}` → 202 / 400 / 404 / **409** |
| GET / DELETE | `/api/v1/Sources/{sourceId}` | |
| GET | `/api/v1/CompensationPlans`, `/api/v1/CompensationPlans/{compensationPlanId}` | Read-only plan: `ranks`, `definitions`, `bonusDefinitions[{volumeKey, treeId, generationBonuses[{generation, percent, compressionKey, qualifications}], …}]`, `incrementType: Day|Month|Week|SemiMonth` |
| GET / GET / PUT | `/api/v1/CompensationPlans/{compensationPlanId}/Periods`, `…/Periods/{periodId}` | PUT body `{status}` (period control. **Deny to Helm.**) |
| GET | `…/Periods/{periodId}/Values`, `…/Values/Details`, `…/Bonuses`, `…/Bonuses/Details`, `…/RankAdvance`, `…/HistoricalValues`, `…/HistoricalBonuses` | Period results |
| GET/POST, GET/DELETE | `/api/v1/Snapshots`, `/api/v1/Snapshots/{snapshotId}` | `Snapshot {compensationPlanId, periodId, status: Processing|Ready|Committed}`. Also `GET /api/v1/Snapshot/{snapshotId}/{Bonuses|Values|RankAdvance|HistoricalValues|HistoricalBonuses}` |
| POST; GET/DELETE | `/api/v1/HistoricalValues`, `/api/v1/HistoricalValues/{id}` | Import of historical values `{key, periodId, nodeId, sumValue, lastValue, postDate}` |
| POST; GET/DELETE | `/api/v1/HistoricalBonuses`, `/api/v1/HistoricalBonuses/{id}` | Import of historical bonuses |
| GET | `/api/v1/Bonuses`, `/api/v1/Bonuses/Details`, `/api/v1/Bonuses/Titles`, `/api/v1/Bonuses/Unreleased`, `/api/v1/Bonuses/Released` | Read bonuses |
| PUT | `/api/v1/Bonuses/Release` (`batchId`) | **Payout release. Deny to Helm in Phase 0.** |
| GET/POST, GET/DELETE | `/api/v1/Bonuses/Manual`, `/api/v1/Bonuses/Manual/{id}` | Manual bonuses. **Deny.** |

### Orders (`/swagger/OrderV1/swagger.json`), as an alternative volume path
| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/v1/Orders/Find` | `search`*, `customerIds[]`, `count`, flags `externalId`, `products`, `tracking` |
| GET / POST | `/api/v1/Orders` | GET filters `ids[]`, `customerId`, `status`, `countryCode`, `offset`, `count`. POST body `Order {id, externalIds[], customerId, orderDate, invoiceDate, orderType, …, lineItems[{productId, price, quantity, volume[{volumeId, volume, uplineId}]}], customData}` → 201 |
| GET / PUT / PATCH / DELETE | `/api/v1/Orders/{id}` | Corrections |

### Reports (`/swagger/ReportV1/swagger.json`)
| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/v1/Reports`, `/api/v1/Reports/Categories`, `/api/v1/Reports/{reportId}` | Report metadata (`query`, `rootPath`, `filters`) |
| GET | `/api/v1/Reports/{reportId}/json` (`offset`, `count`, `filters`), `/csv`, `/pdf` | Exports. JSON gives `totalRows`, `moreRows`, `hash` |

### Webhooks (`/swagger/WebHookV1/swagger.json`)
| Method | Path | Notes |
| --- | --- | --- |
| GET / POST | `/api/v1/WebHooks` | Body `WebHookSubscription {topic, subTopic, url}` (`id` and `version` are read-only) → 202 |
| GET / DELETE | `/api/v1/WebHooks/{subscriptionId}` | |
| GET | `/api/v1/WebHooks/Messages` (`subscriptionId`, `offset`, `count`) | `WebHookMessage {messageId, topic, subTopic, data, enqueueDate, processDate, status, responseDate, responseCode, subscriptionId, url}`. Delivery log for reconciliation |

Documented topics ([topics](https://pillars-hub.readme.io/reference/topics)): `Customer`/`Created`, `Customer`/`Updated`, `Customer`/`Deleted`, `ValueUpdated`/`{Value Id}`, `BonusEarned`/`{Bonus Title}`, `Order`/`Updated`, `Order`/`Created`, `OrderStatusUpdated`/`{Order Status}`, `Node`/`Created`, `Node`/`Updated`. There is no Placement or Source topic. Delivery headers: `x-webhook-messageid`, `x-webhook-topic`, `x-webhook-subtopic`, `x-webhook-subscriptionid`, `x-webhook-version`.

**Version note:** The readme.io reference pages carry `updatedAt: 2025-03-07`. They are older than the live Swagger. For example, the readme `BuildRule` enum lacks `Highest`/`Lowest`, which the live spec has. Use the live spec as the source for field names.

---

## 4. Recommended integration pattern (Recommended design)

### Authority and identifiers
- **Helm owns** the Member record, the provider-ID mapping, Referral Requests (pending, rejected) and an append-only Sponsor Edge audit log.
- **PillarsHub is the authority for accepted Genealogy** (customer `enrollerId` plus node `uplineId` in the Unilevel tree) and, from Phase 1, for Commission calculation.
- **Identifier mapping:** create the PillarsHub customer with `id` = a deterministic value derived from the Helm member ID (or the ID itself, if format rules allow; TBD) **and** `externalIds = ["helm:<memberId>"]`. A retry can then be checked with `GET /api/v1/Customers/{id}` or `Customers/Find?search=<memberId>&externalIds=true` before re-POSTing. This replaces the missing idempotency key. Never put Privy IDs or wallet addresses in PillarsHub unless Phase 1 needs them.

### Signup and referral flow
1. The Helm backend validates the Referral Request: the Sponsor exists and is accepted in PillarsHub, it is not a self-referral, and it creates no cycle. A new node cannot create a cycle, but imports and corrections can. The request stays `pending` until accepted.
2. Sync job (outbox pattern, one job per Member): look up by `id` → if absent, `POST /api/v1/Customers` with `enrollerId` = the Sponsor's PillarsHub id and `signupDate` = Helm's acceptance timestamp → `GET /api/v1/Trees/{treeId}/Nodes/{nodeId}` to confirm placement and `uplineId == enrollerId`. If the node is not auto-created (TBD), `PUT /api/v1/Trees/{treeId}/Nodes/{nodeId}` with `uplineId`, `placeDate` and `effectiveDate`.
3. Mark the Sponsor Edge `accepted` only after the read-back matches. On 4xx, park it in an operations exception queue. On 5xx or timeout, retry with backoff, always look up before re-creating, and keep a dead letter after N attempts.
4. **Sponsor change:** admin-only in Helm, with a reason, approval and audit entry, followed by a PillarsHub node/placement update and read-back. Recommend disabling `enableCustomerMovements` on the tree so the PillarsHub back office cannot drift from Helm (needs PillarsHub configuration).

### Volume (only if Business approves; see §5)
- Create a dedicated Source Group (for example `VAULT_DEPOSIT_USD`; the name is Helm's choice) with `PUT /api/v1/SourceGroups/{id}`.
- After a Vault Deposit is **confirmed on-chain**, `POST /api/v1/Sources` with `externalId` = `<chainId>:<txHash>:<logIndex>` (globally unique), `nodeId`, `date` = confirmation time and `value`. On 409 or timeout, `GET /api/v1/Sources?externalId=…` to confirm before retrying.
- For a Redemption or other reversal, `DELETE /api/v1/Sources/{sourceId}` or post a compensating Source (negative value is TBD), recorded in Helm's event log. How a reversal affects a closed period is TBD.

### Webhooks vs polling
- Subscribe to `Customer/*` and `Node/*` as **change hints only**. Webhooks are not signed. Recommended: a secret, unguessable path segment in the subscription URL, deduplication on `x-webhook-messageid`, and re-fetching the resource through the API before acting. Never trust the payload.
- **Reconciliation job (authoritative):** nightly, plus on demand. Page `GET /api/v1/Trees/{treeId}/Nodes?offset&count` (and `date` for as-of checks) and `GET /api/v1/Sources?start&end`. Compare with Helm's accepted Sponsor Edges and posted events. Report missing, extra and mismatched records to the operations queue. Use `GET /api/v1/WebHooks/Messages` to detect failed deliveries before the 2-day retry window ends and the subscription is disabled.

### Tokens and environments
- One PillarsHub environment for staging/test and one for production, each with its own Access Token in the secret manager. Tokens never go to the browser.
- Ideally two tokens per environment: a **read-only** token for reconciliation and reporting, and a **write** token limited to Customers, Nodes, Placements and Sources. Deny Trees, Periods, Snapshots, Bonuses, Batches, Users, Roles and DELETE wherever possible. The granularity available is TBD.

---

## 5. Phase 0 decisions this note informs

| Decision | Recommended default | Why |
| --- | --- | --- |
| Is a 3-level Commission calculated in Phase 0? | **No accrual, no payout** unless Terrel's PRD or Business requires it | Real-time calculation means posted volume creates visible pending bonuses. Payouts need a Money-Out integration, which Phase 0 does not need. |
| Post Vault Deposit volume in Phase 0? | **Record in Helm; post to PillarsHub into a non-commissionable Source Group**, or defer posting. Helm's event log can backfill later with original dates (`date`/`postDate`, `HistoricalValues`). | Keeps data for Phase 1 without creating an implied obligation. Backfill viability is TBD in staging. |
| Genealogy authority | PillarsHub (per PRD), with Helm keeping pending requests, the audit log and a reconciled copy | The API supports create, read-back and full-tree export. |
| Member back office in PillarsHub? | Not in Phase 0. Helm Web App only. | Avoids SSO token-in-URL handling and exposure of pending commission widgets. |

---

## 6. Open questions for PillarsHub

1. In the Helm staging plan, which tree(s) exist? Does `POST /api/v1/Customers` with `enrollerId` automatically create the node in the Unilevel tree, and is `enrollerId` always equal to the node's `uplineId` there?
2. Is there any limit on Genealogy depth stored or calculated? Does `GET /api/v1/Trees/{treeId}/Nodes` without `nodeIds` return every node in the tree, and what is the maximum `count`?
3. Can `enrollerId` be changed after creation (it is absent from `CustomerUpdate`)? What is the supported way to make an audited Sponsor correction: Node PUT, Placements POST, or both? Can customer and admin "movements" be disabled?
4. What does `409 Conflict` on `POST /api/v1/Sources` mean? Is `externalId` unique per environment? Is a duplicate customer `id` rejected?
5. Are negative Source values accepted? How do deletes and corrections behave once a period is closed or a snapshot is `Committed`?
6. How is a Source Group linked to bonus `volumeKey`s? Can a Source Group exist that no bonus uses?
7. Can Access Tokens be limited per area (the `Permissions` object), not just Read Only? Can DELETE be denied?
8. What are the API rate limits and burst limits per environment? Which status code is returned when they are exceeded?
9. Can webhooks be signed or authenticated? What are the payload schema and the `x-webhook-version` values per topic? Is there a Placement or Source topic?
10. Is there a bulk or assisted import for existing members with Sponsors and historical dates?
11. Is there a supported GraphQL endpoint for API clients, given the `graphQL` permission and "GraphQL reports"?
12. Security: SOC 2 / ISO 27001 or a penetration-test summary, data residency (Terms say US processing; Azure hosting), backup/RPO/RTO, environment isolation, data export on termination, and DPA availability.
13. Commercial: pricing, staging vs production environment fees, and RUSH rate. Is launch-window timing (Tue–Thu MT) a constraint for Helm's go-live?
14. Confirm in writing that API-based reconciliation and mirroring of Genealogy is permitted, given the Terms' "systematically retrieve data" clause. Explain how the GLBA disclaimer applies to a customer whose Members hold vault positions.

---

## 7. Evidence limitations

- **Staging not accessed** (by instruction). Plan contents, tree setup, token permissions and runtime behaviour are unverified. Staging and the Unilevel plan are **Provider correspondence** only.
- **The specs have no operation descriptions.** Endpoint semantics such as Node PUT effects, 409 meaning and delete side effects are inferred from names and schemas only.
- **The readme.io reference is older (2025-03-07) than the live Swagger.** Field lists were taken from the live spec.
- **No public pricing, rate limits or security certifications** were found. `/pricing` and `/security` return 404.
- **WebSearch was unavailable.** No third-party reviews, status page or incident history were checked.
- **The marketing site contains template placeholder testimonials** (named "Gem template", "Alexus Reed"). Marketing claims such as "Time Travel Auditing" and "300 companies" are treated as vendor statements, not verified facts.
