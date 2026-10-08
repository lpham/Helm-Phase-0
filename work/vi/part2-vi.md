# Phần II: Triển khai kỹ thuật {.unnumbered}

# PRD high-level đã chỉnh sửa

## Mục tiêu

1. Onboard Member với một identity ổn định duy nhất và một wallet self-custodial dùng được ngay.
2. Hỗ trợ Wallet Funding trực tiếp bằng crypto và tham gia một vault đã được duyệt, kèm một luồng Redemption dùng được trong thực tế.
3. Tái sử dụng game Tap Prediction và Points hiện có để tăng engagement.
4. Ghi nhận Genealogy đầy đủ, portable ngay từ lượt signup đầu tiên, để Commission ở Phase 1 không phải dựng lại identity.

## Personas

- **Member:** tham gia qua Referral, nạp tiền vào wallet, deposit, chơi game, redeem, liên hệ support.
- **Operations administrator:** xử lý exception về Referral và Wallet Funding, quản lý allowlist của vault, theo dõi queue và reconciliation, xử lý escalation. Dùng Helm admin và dashboard của các provider.
- **Vault operator** (do Business chỉ định): cập nhật valuation của vault, execute deposit queue và redeem queue, quản lý thanh khoản. Dùng Onyx Admin App.
- **Support agent:** trả lời Member trên Chatwoot; không được chuyển tiền, đổi Sponsor hay cộng Points.
- **Business reviewer:** xem báo cáo funnel, mức tham gia, Referral và engagement.

## Functional requirements và acceptance criteria

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-1 | Xác thực bằng Privy và resolve về một Helm member duy nhất | Login lại bằng bất kỳ phương thức đã link nào đều resolve về cùng một Helm member ID; backend verify mọi Privy token; trường hợp trùng người được đưa vào admin queue |
| FR-2 | Tạo một embedded EVM wallet cho mỗi Member | Wallet có sẵn sau lần login đầu tiên; địa chỉ được đọc từ Privy ở server-side; Member ký được một transaction thử; app giải thích cơ chế recovery và key export |
| FR-3 | Ghi nhận Referral Request khi signup | Invite code hoặc link được lưu trước khi login và gắn với Member mới; self-referral bị từ chối; Sponsor thiếu hoặc không hợp lệ xử lý theo rule D8 |
| FR-4 | Accept Sponsor Edge trong PillarsHub | Customer được tạo với ID do Helm định nghĩa và Sponsor; node được read-back với upline đúng như kỳ vọng; edge chỉ được đánh dấu accepted sau khi read-back; retry không bao giờ tạo bản trùng |
| FR-5 | Hiển thị network và asset được hỗ trợ để nạp tiền | Chỉ cung cấp một network và một asset; có cảnh báo sai network; Wallet Funding đi qua các trạng thái submitted → confirmed (N block) → credited; transfer lỗi hoặc không được hỗ trợ chuyển sang exception |
| FR-6 | Screening địa chỉ | Wallet của Member khi tạo, mỗi funding source và mỗi địa chỉ đích của Redemption đều được screening; nếu có hit thì việc đưa vào allowlist của vault hoặc action tương ứng bị chặn và một case được mở |
| FR-7 | Gate quyền truy cập vault | Member phải chấp nhận vault terms hiện hành (có version) và qua eligibility check; chỉ khi đó wallet mới được thêm vào allowlist của Onyx |
| FR-8 | Vault Deposit | Member ký approval đúng số tiền và deposit request; Helm theo dõi approval → request → pending → executed hoặc cancelled; position chỉ được tính sau khi execute |
| FR-9 | Hiển thị position | Số share và giá trị theo lần valuation gần nhất của vault, kèm timestamp của valuation; khớp với state on-chain |
| FR-10 | Redemption | Member ký redemption request; Helm hiển thị pending, awaiting liquidity, executed, cancelled; asset về wallet của Member; position và business event được điều chỉnh tương ứng |
| FR-11 | Game và Points | Game account được link; event đã verify chỉ cộng Points một lần; rule và daily limit được hiển thị; Points tách biệt với tiền |
| FR-12 | Support | Identity trong chat đã được verify; agent chỉ thấy Helm member ID và status không nhạy cảm; logout sẽ reset chat |
| FR-13 | Admin và reconciliation | Reconciliation hằng ngày cho Genealogy, Wallet Funding, Vault Position và Points; sai lệch xuất hiện trong exception queue kèm audit trail |
| FR-14 | Reporting | Số signup, số Member đã funding, mức tham gia vault đã confirmed, độ đầy đủ của Referral và engagement, có hiển thị độ mới của dữ liệu và không đếm trùng Wallet Funding với Vault Deposit |

**Commission ba tầng:** không bắt buộc khi launch, trừ khi PRD của Terrel yêu cầu khác (quyết định D2). Dù vậy, Genealogy vẫn được ghi nhận ở mọi độ sâu.

## Operational requirements

- Mọi integration write đều idempotent từ phía Helm, có retry với backoff và được reconciliation hằng ngày.
- Không private key, seed phrase hay credential đặc quyền nào của provider được lọt vào browser, log hoặc payload gửi cho support.
- Môi trường test và production tách riêng cho mọi provider, với credential riêng.
- Monitoring và alert cho: valuation của vault quá cũ, deposit hoặc redemption request pending quá target, reconciliation bị lệch, sync lỗi, screening có hit.

## Success metrics (target TBD)

Thời gian đến live deposit đầu tiên được duyệt; tỷ lệ hoàn tất signup; conversion từ signup sang funded và từ funded sang deposited; độ đầy đủ của referral attribution (target 100% signup được accept); số reconciliation exception mỗi tuần; mức tham gia game và engagement lặp lại; first-response time và resolution time của support.

# Solution architecture

```{.mermaid #fig-architecture caption="Kiến trúc kỹ thuật và các trust boundary."}
flowchart TB
  subgraph Browser
    APP[Helm Web App + Privy SDK + Chatwoot widget]
  end
  subgraph Helm backend - Cyclone
    API[API và auth verification]
    DB[(Member DB, referral và event ledger)]
    INT[Integration worker: outbox, retry]
    IDX[Chain indexer]
    REC[Reconciliation và alert]
    ADM[Admin console]
  end
  APP -->|Privy token| API
  APP -->|ký transaction| CHAIN[(Arbitrum: USDC, Onyx vault contract)]
  API --> DB
  INT --> PH[PillarsHub API]
  INT --> GAME[Cyclone game và points API]
  INT --> SCR[Sanctions screening API]
  INT -->|cập nhật allowlist qua list-owner key| CHAIN
  IDX --> CHAIN
  REC --> ONYXAPI[Onyx public read API]
  API --> PRIVY[Privy API]
  APP --> CW[Chatwoot Cloud]
```

## Các component và lý do cần có

| Component | Trách nhiệm | Lý do phải tự build |
|---|---|---|
| Helm Web App | UI cho Member và admin; login Privy; ký bằng embedded wallet của Member; Chatwoot widget | Một trải nghiệm Member thống nhất trên mọi provider |
| API và auth | Verify Privy access token; resolve Helm member ID; phục vụ app | Các provider không tự dùng chung một identity được |
| Member DB và ledger | Member, mapping provider ID, wallet, Referral Request, Sponsor Edge và các correction, business event, consent record, audit log | Một nơi duy nhất để reconcile identity và các money event |
| Integration worker | Outbox job tới PillarsHub, game service, screening và allowlist; retry và dead letter | Không provider nào có idempotency key cho tất cả các call |
| Chain indexer | Index các USDC transfer vào wallet của Member cùng các event queue, share và valuation của Onyx ở confirmation depth | Webhook production của Privy cần gói Enterprise; Onyx không có webhook. Verified |
| Reconciliation | Check hằng ngày với chain, Onyx API, tree của PillarsHub và Points | Dữ liệu provider có thể bị lệch; phải chứng minh được |
| Admin console | Exception, screening case, trạng thái allowlist, Sponsor correction có approval | Tối giản; phần còn lại dùng dashboard của provider |

## Data authority

| Object | Source of truth | Helm lưu |
|---|---|---|
| Helm member identity và mapping provider ID | Helm DB | Master |
| Login identity | Privy user (DID) | Chỉ mapping |
| Wallet address | Privy (đọc server-side) và chain | Liên kết kèm thời điểm first-seen |
| Genealogy đã accept | Tree của **PillarsHub** (enroller của customer và upline của node) | Request đang pending, bản copy các edge đã accept, audit log các correction |
| Wallet Funding | Blockchain | Event đã index và confirmed |
| Vault deposit request, position, Redemption | Blockchain (Onyx contract) | Event đã index; Onyx API dùng để cross-check |
| Vault valuation | Valuation contract của Onyx (do vault operator cập nhật) | Hiển thị kèm timestamp |
| Points balance | Cyclone points service | Bản copy để hiển thị |
| Conversation | Chatwoot | Link tới member ID |
| Terms acceptance, kết quả screening, eligibility | Helm DB | Master |

## Ranh giới về credential, signing và custody

| Actor | Được ký hoặc thực hiện | Không được | Ghi chú |
|---|---|---|---|
| Member | Transfer từ wallet, approval cho vault, deposit request và redemption request, cancel | Admin action | Privy embedded wallet; Onyx yêu cầu chính địa chỉ của Member ký request. Verified |
| Helm backend | Write vào PillarsHub (customer, node, source) bằng token giới hạn quyền; game API; screening API; cập nhật allowlist của vault qua list-owner key | Chuyển tiền của Member; vault admin action | List-owner key nằm trong key management service; chỉ sở hữu allowlist contract (cần xác nhận với Enzyme) |
| Vault Owner (Business) | Thêm và gỡ Admin; mọi admin action | — | Recommended: Safe multisig với signer thuộc Business |
| Vault Admin / operator (Business) | Cập nhật valuation; execute queue; chuyển asset sang strategy wallet; set fee | — | Được protocol tin cậy hoàn toàn. Verified |
| Strategy Manager (do Business chỉ định) | Chạy strategy bên ngoài Onyx; trả lại thanh khoản | — | Custody của strategy wallet nằm ngoài Onyx. Verified |
| Enzyme | Deploy; upgrade contract (global owner) | — | Upgrade governance phải được quy định trong MLA. Verified |
| Privy | Vận hành signing enclave | Ký thay Member | Privy "is never an authorized signer". Verified |
| Support agent | Trả lời trên Chatwoot; xem member status ở chế độ read-only | Tiền, Sponsor, Points | Được enforce trong Helm admin |

Token PillarsHub gắn với từng môi trường và không hết hạn; có thể cấu hình read-only. Recommended: một token read-only cho reconciliation và một write token riêng, chặn các khu vực destructive nếu PillarsHub hỗ trợ (TBD). Trong Phase 0, Helm tuyệt đối không gọi các endpoint payout, period và bonus-release.

# Data flow end-to-end

Mọi flow đều phân biệt **submitted** (Helm đã có request hoặc transaction hash), **confirmed** (provider đã acknowledge hoặc đã đủ số block confirmation) và **synchronised** (bản copy của Helm khớp với source of truth sau reconciliation). Webhook chỉ được coi là tín hiệu; polling và indexing mới là source of truth.

```{.mermaid #fig-flow-signup caption="Invite, signup, wallet và Genealogy đã accept."}
sequenceDiagram
  participant M as Member app
  participant P as Privy
  participant H as Helm backend
  participant X as PillarsHub
  M->>M: lưu invite code
  M->>P: login
  P-->>M: access token, embedded wallet
  M->>H: register(token, invite code)
  H->>P: verify token, đọc wallet address
  H->>H: tạo member, Referral Request (pending), screening địa chỉ
  H->>X: tìm customer theo Helm ID
  H->>X: tạo customer (id, externalIds, enrollerId)
  H->>X: đọc node và upline
  H->>H: Sponsor Edge accepted
  H-->>M: referral đã confirmed
```

```{.mermaid #fig-flow-funding caption="Wallet Funding trực tiếp."}
sequenceDiagram
  participant E as Sàn hoặc wallet
  participant C as Arbitrum
  participant I as Helm indexer
  participant H as Helm backend
  participant M as Member app
  E->>C: USDC transfer tới địa chỉ Member
  I->>C: thấy Transfer event (submitted)
  I->>I: chờ N confirmation
  I->>H: funding confirmed (chain, tx, log index)
  H->>H: screening địa chỉ nguồn, ghi event
  H-->>M: cập nhật balance
```

```{.mermaid #fig-flow-deposit caption="Vault Deposit, execution và position."}
sequenceDiagram
  participant M as Member app
  participant H as Helm backend
  participant C as Onyx contracts
  participant O as Vault operator
  M->>H: chấp nhận vault terms (version)
  H->>C: thêm wallet vào allowlist
  M->>C: approve đúng số tiền
  M->>C: requestDeposit
  C-->>H: DepositRequest(requestId) qua indexer
  O->>C: cập nhật valuation, execute deposit request
  C-->>H: DepositRequestExecuted(requestId, shares)
  H->>H: position confirmed, ghi business event
  H-->>M: hiển thị position và ngày valuation
```

```{.mermaid #fig-flow-game caption="Từ hoạt động game đến Points."}
sequenceDiagram
  participant M as Member app
  participant G as Game và points service
  participant H as Helm backend
  M->>G: chơi (đã link Helm member)
  G->>G: validate kết quả, áp dụng limit
  G->>H: signed event (event id, member, Points)
  H->>H: verify signature, dedupe theo event id
  H-->>M: Points balance (lấy từ service)
```

```{.mermaid #fig-flow-redemption caption="Từ redemption request đến settlement."}
sequenceDiagram
  participant M as Member app
  participant H as Helm backend
  participant C as Onyx contracts
  participant O as Vault operator
  M->>H: screening địa chỉ đích (wallet của chính Member)
  M->>C: requestRedeem(shares)
  C-->>H: RedeemRequest(requestId) qua indexer
  O->>C: cập nhật valuation, bảo đảm thanh khoản
  O->>C: execute redeem request
  C-->>H: RedeemRequestExecuted(requestId, assets)
  H->>H: giảm position, ghi business event
  H-->>M: USDC về wallet, hoàn tất các stage
```

```{.mermaid #fig-flow-support caption="Support và xử lý exception phía admin."}
sequenceDiagram
  participant M as Member app
  participant H as Helm backend
  participant W as Chatwoot
  participant A as Agent
  participant D as Helm admin
  M->>H: yêu cầu chat identity
  H-->>M: member ID + identity hash
  M->>W: mở conversation đã verify
  W->>A: conversation kèm member ID
  A->>D: tra cứu status (read-only)
  D->>D: ops xử lý exception có approval và audit
  A->>W: trả lời Member
```

## Flow matrix

| Flow | Nguồn → đích | Dữ liệu tối thiểu | Source of truth | Deduplication key | Lỗi và retry | User thấy |
|---|---|---|---|---|---|---|
| Signup và Referral | App → Helm → PillarsHub | Privy DID, wallet address, invite code, member ID của Sponsor | Tree của PillarsHub (edge đã accept) | Helm member ID (customer ID trong PillarsHub) | Lookup trước khi create; backoff; dead letter chuyển cho ops; tree reconciliation hằng đêm | "Referral pending" rồi "confirmed" |
| Wallet Funding | Sàn → chain → Helm indexer | Chain, tx hash, log index, amount, from, to | Chain | (chain, tx hash, log index) | Re-index từ safe block gần nhất; xử lý reorg dựa trên confirmation depth | Balance pending → confirmed |
| Vault Deposit | App → Onyx contract; indexer → Helm | Request ID, amount, wallet, version của terms | Chain (queue và share) | (chain, queue address, request ID) | Transaction bị revert hiển thị kèm lý do; alert khi pending quá lâu; cross-check với Onyx API | Approval → requested → processing → position |
| MLM volume đủ điều kiện (Phase 1 hoặc nếu được duyệt) | Helm → source của PillarsHub | Node của Member, amount đã execute, ngày | Business event của Helm; source trong PillarsHub | Source externalId = chain:tx:log | Lookup theo externalId khi conflict hoặc timeout | Không hiển thị trong Phase 0 |
| Game sang Points | Game service → Helm | Event ID, member ID, Points, rule ID | Points service | Event ID | Signed event; replay protection; daily limit | Points balance và lịch sử |
| Redemption | App → Onyx; indexer → Helm | Request ID, share, địa chỉ đích | Chain | (chain, queue address, request ID) | Alert awaiting liquidity; cho cancel sau thời gian tối thiểu | Requested → awaiting liquidity → paid |
| Support | App → Chatwoot; agent → Helm admin | Member ID, identity hash, status không nhạy cảm | Chatwoot (conversation); Helm (action) | Conversation ID | Reset widget khi logout; log các Chatwoot webhook có chữ ký | Chat thread |

**Khi provider không khả dụng:** nếu PillarsHub down, signup vẫn chạy với Referral ở trạng thái pending và sync sau. Nếu indexer bị chậm, balance hiển thị "đang cập nhật". Nếu Onyx API không khả dụng, Helm đọc trực tiếp từ chain. Nếu game service down, tính năng chơi bị tắt và không mất Points.

# Genealogy và mức sẵn sàng cho Phase 1

## Data model tối thiểu

| Table | Field chính | Mục đích |
|---|---|---|
| member | helm_member_id, status, created_at, country attestation | Identity ổn định |
| provider_identity | helm_member_id, provider (privy, pillarshub, chatwoot, game), external_id, linked_at | Mapping tường minh |
| wallet | helm_member_id, chain_id, address, source (embedded), first_seen_at, screening_status, allowlist_status | Một vault wallet cho mỗi Member |
| referral_request | id, helm_member_id, sponsor_member_id, invite_code, channel, captured_at, status, rejection_reason | Referral đang pending và bị từ chối |
| sponsor_edge | id, member_id, sponsor_member_id, effective_at, accepted_at, provenance (signup, import, correction), pillarshub_sync_status, superseded_by | Toàn bộ graph ở mọi độ sâu |
| edge_correction | id, edge_id, old_sponsor, new_sponsor, reason, requested_by, approved_by, approved_at | Thay đổi có audit |
| business_event | id, type (funding, deposit_executed, redemption_executed, points_awarded), member_id, amount, asset, chain reference, occurred_at, idempotency_key | Backfill volume cho Phase 1 và reporting |
| integration_outbox | id, target, payload hash, attempts, status, last_error | Sync tin cậy |

Chỉ thu thập dữ liệu có mục đích rõ ràng. Không ghi dữ liệu Sponsor hay Member lên chain.

## Rules

- **Self-referral:** bị từ chối ngay lúc capture (cùng member, cùng wallet, cùng email hoặc số điện thoại đã verify).
- **Sponsor không hợp lệ hoặc bị thiếu:** gắn vào root account của công ty với provenance "no sponsor" và flag để review (quyết định D8).
- **Cycle:** không thể xảy ra với Member mới; được check ở mỗi lần correction và import.
- **Đổi Sponsor:** không bao giờ cho self-service. Chỉ admin được làm, kèm lý do, approval thứ hai và audit entry, sau đó update node trong PillarsHub và read-back. Recommended: tắt customer movement trong cấu hình tree của PillarsHub để hai hệ thống không bị lệch nhau.
- **Merge account:** là quy trình admin; giữ edge được accept sớm nhất; trỏ lại các child edge kèm audit entry; retire identity bị trùng.
- **Import user hiện có** (chỉ khi phải chuyển member của FirstAlphaWave hoặc TaQUANT): import Sponsor trước rồi mới đến cấp dưới, giữ ngày signup gốc và provenance "import"; không có bulk API nên phải import từng record. Verified.

## Chứng minh tính đúng đắn

- **Full export:** phân trang qua mọi node của tree với một as-of date, không dùng endpoint downline vì endpoint này bị giới hạn ở 10 tầng. Verified.
- **Nightly reconciliation:** so sánh các edge đã accept của Helm với node trong PillarsHub (số lượng, khớp upline theo từng edge, checksum). Mọi sai lệch đều là exception.
- **Test trên staging trước khi launch:** một tree synthetic sâu ít nhất 15 tầng và đủ rộng để phải phân trang, được tạo, export và so sánh.
- **Snapshot cho Phase 1:** PillarsHub nhận as-of date và lưu placement theo ngày, còn Helm lưu effective timestamp, nên có thể dựng lại Genealogy trong quá khứ. Phase 0 không cần snapshot store riêng.

## Volume trong Phase 0

PillarsHub tính Commission real-time từ volume được post. Verified. Nếu post Vault Deposit vào một volume type có tính Commission, Member sẽ thấy Commission đang pending. **Recommended:** chỉ ghi các deposit và Redemption đã execute thành business event trong Helm; sang Phase 1, backfill vào PillarsHub với ngày gốc sau khi compensation plan được duyệt. Việc PillarsHub có nhận volume backdate cho các period đã đóng hay không cần được xác nhận trên staging.

# Backlog, phụ thuộc và lịch trình

## Backlog theo thứ tự ưu tiên

| Mức ưu tiên | Work item | Phụ thuộc vào |
|---|---|---|
| **Bắt đầu ngay** | App shell và design system; Privy login và embedded wallet; member DB và ledger; capture và validate Referral; sync PillarsHub trên staging có read-back; chain indexer (Sepolia); deposit và redemption qua Onyx SDK trên Sepolia; Chatwoot widget có identity validation; admin skeleton; screening hook với sanctions API miễn phí; CI, các môi trường, secret | Quyền truy cập test của provider |
| **Thin slice (tuần 1–3)** | Demo end-to-end trên testnet, gồm một flow game sang Points | Tài liệu game API |
| **Trước khi nhận tiền thật** | Vault terms và disclosure với acceptance có version; tự động hóa allowlist; reconciliation job và alert; exception queue; các stage và target của Redemption; eligibility theo quốc gia; Member terms và privacy notice; môi trường production; fix các finding từ security review; operations runbook và diễn tập | Strategy, MLA, ownership, câu trả lời từ legal |
| **Có thể hoãn** | Top-up tích hợp; thêm chain và asset; accrual và payout Commission; Telegram và WhatsApp; audit log và SSO của Chatwoot; transaction monitoring thương mại; native mobile | Nhu cầu của Business |

## Critical path

1. Các quyết định D1–D8 trong buổi họp.
2. **Vault sẵn sàng:** strategy và Manager → cấu hình vault (asset, async queue, external allowlist, share không chuyển nhượng được, fee) → ký MLA → deploy production → bàn giao ownership cho multisig của Business.
3. **Câu trả lời từ legal:** pháp nhân, các quốc gia launch, KYC tier, vault terms.
4. **Security review** phần integration của Helm và cấu hình vault.
5. **Diễn tập vận hành:** valuation, execute queue và thanh khoản cho Redemption với một khoản tiền nhỏ.
6. Launch slot production của PillarsHub (thứ Ba đến thứ Năm).

Phần engineering chạy song song với mục 2–3; ngày launch phụ thuộc vào hạng mục nào xong sau cùng.

# Sẵn sàng launch và vận hành

## Launch gate để nhận tiền thật

Tất cả điều kiện phải đạt; không bỏ qua điều kiện nào chỉ để kịp deadline.

1. Vault strategy, Manager, fee và Member terms được Business và luật sư duyệt.
2. MLA đã ký; Enzyme xác nhận version đã deploy và audit coverage; upgrade governance có văn bản.
3. Multisig của Vault Owner đã sẵn sàng; Admin key và list-owner key nằm trong managed custody; backend của Helm không giữ Owner key hay Admin key nào.
4. Deposit và Redemption đã được chứng minh trên production với một khoản tiền nhỏ do operator cấp.
5. Reconciliation hằng ngày pass; monitoring và alert đã chạy; có đầu mối incident ở từng provider.
6. Screening và eligibility đã chạy cho tier được luật sư duyệt.
7. Security review hoàn tất và các finding mức high đã được fix.
8. Các provider (Privy, Enzyme, PillarsHub) chấp nhận mô hình kinh doanh bằng văn bản.
9. Có support runbook và quy trình escalation, gồm cả cách xử lý user bị flag.

## Security boundary

- **Audit coverage.** ChainSecurity đã audit Onyx core (tháng 12/2025), cross-chain wallet (tháng 5/2026) và Chainlink compliance integration (tháng 7/2026). Một deployment helper thêm vào sau lần audit cuối không nằm trong audit scope nào tìm được. Verified. Enzyme phải xác nhận vault của Helm dùng những component nào và chúng đã được audit.
- **Rủi ro upgrade.** Global owner của Enzyme có thể upgrade toàn bộ vault contract; báo cáo audit mô tả role này có thể "fully drain the system", và không thấy timelock nào. Verified. MLA phải quy định về thông báo trước và governance.
- **Gas sponsorship.** Gas sponsorship native của Privy upgrade wallet của Member bằng EIP-7702; delegation contract thuộc phạm vi security review. Verified.
- **Webhook PillarsHub không có chữ ký.** Chỉ coi là tín hiệu và fetch lại qua API. Verified.
- **Tách biệt test và production** cho mọi provider, với credential riêng và không có production key trên máy developer.

## Compliance responsibility matrix

Các bộ phận chịu trách nhiệm chỉ là đề xuất; owner cụ thể là TBD.

| Control | Câu hỏi về khả năng áp dụng | Accountable (đề xuất) | Phần việc của Cyclone | Capability của provider được dựa vào | Ảnh hưởng tới launch |
|---|---|---|---|---|---|
| Phân loại pháp nhân và custody | Có pháp nhân nào nắm "control" đối với tài sản của Member không (vault role, allowlist key)? | Business + luật sư | Ghi lại signing authority và key flow | Self-custody của Privy (verified); role của Onyx (verified) | **Blocker** |
| Quốc gia launch và giới hạn địa lý | Những quốc gia nào được phép? | Business + luật sư | Country attestation, IP check, block list | Không có sẵn | **Blocker** |
| Xác định bản chất sản phẩm vault | Vault có phải là sản phẩm chịu quản lý tại các quốc gia launch không? | Business + luật sư | Màn hình terms, fee và rủi ro kèm acceptance record | Strategy và fee của Onyx (TBD) | **Blocker** |
| KYC tier | Có cho phép tier không KYC không; ở ngưỡng nào? | Business compliance + luật sư | Field và gate theo tier làm ngay; tích hợp vendor nếu bắt buộc | Không có sẵn (Privy KYC qua Bridge không khả dụng) | Trước khi nhận tiền |
| Sanctions: địa chỉ | Danh sách nào và khi nào? | Business compliance | Screening wallet, funding source, địa chỉ đích của Redemption | Chainalysis free API (verified, discovery) | Trước khi nhận tiền |
| Sanctions: cá nhân | Có bắt buộc name screening không? | Business compliance + luật sư | Hook vào identity tier | Vendor TBD | Trước khi nhận tiền nếu bắt buộc |
| Vault admission | Chỉ Member đủ điều kiện mới được deposit | Business + Enzyme | Tự động hóa allowlist sau khi check | Deposit allowlist của Onyx (verified) | Trước khi nhận tiền |
| AML monitoring và escalation | Những nghĩa vụ monitoring và báo cáo nào được áp dụng? | Business (compliance officer) | Ngưỡng, exception queue, case log | Không có sẵn | Trước khi nhận tiền (tối thiểu làm thủ công) |
| User và transaction bị flag | Helm được phép từ chối hoặc tạm giữ những gì một cách hợp pháp? | Luật sư + Business | Các trạng thái restricted trong Helm; không mặc định có quyền freeze | Quyền quyết định và policy của Onyx admin (verified) | Trước khi nhận tiền |
| Terms, privacy, consent, retention | Cần những notice và consent chia sẻ dữ liệu nào? | Business (legal) | Consent có version; data map theo từng provider | Chatwoot Cloud host tại Mỹ (verified) | Trước khi nhận tiền |
| Mô hình Referral và Points | Phần thưởng Referral và Points có được công bố và hợp pháp không? | Business + luật sư | Trang rule; không đưa ra cam kết thu nhập; Points tách biệt với tiền | PillarsHub, game service | Trước khi nhận tiền (disclosure) |
| Provider acceptance | Các provider có chấp nhận mô hình khi được công bố đầy đủ không? | Business | Tránh các tính năng Stripe và Bridge trong Privy | Xác nhận bằng văn bản | Trước khi nhận tiền |

# Quyết định triển khai và các gap về tính khả thi

| Quyết định | Phương án Recommended | Bằng chứng | Phụ thuộc chưa giải quyết | Bộ phận chịu trách nhiệm (đề xuất) | Ảnh hưởng tới launch |
|---|---|---|---|---|---|
| Network và asset | Arbitrum One, native USDC; Sepolia để test | Onyx và Privy hỗ trợ Arbitrum; bản deploy test của Onyx chạy trên Sepolia (verified) | Enzyme xác nhận chain và asset cho production | Business + Tech | Cao |
| Wallet model | Privy embedded wallet do user sở hữu, không có app signer, gas được sponsor, bật export | Tài liệu Privy (verified) | Privy chấp nhận mô hình kinh doanh; volume limit trên $1M mỗi tháng | Tech | Trung bình |
| Cấu hình vault | Async deposit queue; external allowlist do một list-owner key chuyên dụng sở hữu; share không chuyển nhượng được; một asset | Contract và tài liệu Onyx (verified) | Enzyme xác nhận ownership của external list khi deploy | Business + Enzyme | Cao |
| Vault role | Safe multisig của Business làm Owner; Admin wallet riêng; admin giới hạn quyền cho việc cập nhật valuation | Role của Onyx (verified) | Signer của Business; việc chỉ định Manager | Business | **Blocker** |
| Target cho Redemption | Công bố một target vận hành; hiển thị các stage | Không có SLA ở cấp protocol (verified) | Liquidity policy từ Manager | Business | Cao |
| Genealogy authority | PillarsHub, kèm request pending và bản copy đã reconcile trong Helm | Customer API và tree API (verified) | Cơ chế auto-placement và cách correction trên staging | Tech + PillarsHub | Trung bình |
| Commission ở Phase 0 | Không accrue, không chi trả; event lưu trong Helm để backfill | Tính toán real-time và bước payout riêng (verified) | PRD của Terrel; xác nhận của Business | Business | Trung bình |
| Funding path | Crypto trực tiếp; không dùng top-up provider | Paymenture không công bố asset, quốc gia hay fee và cấm "pyramid schemes" (verified) | Yêu cầu của Business | Business | Thấp |
| Points | Không có giá trị tiền mặt; không gắn với số tiền deposit | Chưa nhận được tài liệu game | Tài liệu game API; luật sư review | Business + Cyclone | Trung bình |
| Identity check | Build gate ngay từ bây giờ; tier do luật sư quyết định; screening địa chỉ từ ngày đầu | Stack hiện không có KYC (verified) | Quyết định của luật sư | Business + luật sư | Cao |

**Điều gì sẽ thay đổi các phương án mặc định này:** nếu cần top-up tích hợp ngay khi launch thì phải thêm một payment provider vào critical path; nếu phải chi trả Commission ba tầng ngay khi launch thì cần thêm money-out integration và các control cho payout; nếu luật sư yêu cầu KYC đầy đủ thì cần thêm một identity vendor và một gate trước khi truy cập vault.

# Phụ lục A: Bằng chứng {.unnumbered}

Tất cả link được đọc vào ngày 8/10/2026.

**PillarsHub:** [API authentication](https://pillars-hub.readme.io/reference/authenticating) · [Access token](https://pillars-hub.readme.io/reference/access-control-tokens) · [Swagger UI](https://api.pillarshub.com/swagger/index.html) · [Customer API spec](https://api.pillarshub.com/swagger/CustomerV1/swagger.json) · [Commission API spec](https://api.pillarshub.com/swagger/CommissionV1/swagger.json) · [Webhook](https://pillars-hub.readme.io/reference/getting-started-webhooks) · [Webhook topic](https://pillars-hub.readme.io/reference/topics) · [Invoice date và real-time commission](https://pillars-hub.readme.io/docs/invoice-dates-are-used-to-calculate-commissions) · [Launch timing protocol](https://pillars-hub.readme.io/docs/pillars-launch-timing-protocol) · [Money-out integration](https://pillars-hub.readme.io/docs/money-out-merchant-integration-guide) · [Terms](https://www.pillarshub.com/terms)

**Privy:** [Bảng giá](https://www.privy.io/pricing) · [Security FAQ](https://docs.privy.io/security/security-faqs) · [Hỗ trợ user](https://docs.privy.io/user-management/users/managing-users/supporting-your-users) · [Webhook](https://docs.privy.io/api-reference/webhooks/overview) · [React quickstart](https://docs.privy.io/basics/react/quickstart) · [Acceptable use policy](https://www.privy.io/acceptable-use-policy)

**Enzyme Onyx:** [Sản phẩm và bảng giá](https://enzyme.finance/products/onyx) · [Kiến trúc](https://docs.enzyme.finance/onyx-user-documentation/getting-started/quickstart/architecture) · [Deposit control và allowlist](https://docs.enzyme.finance/onyx-user-documentation/enzyme-vault/subscription/control) · [Redemption](https://docs.enzyme.finance/onyx-user-documentation/enzyme-vault/subscription/redemptions) · [User role](https://docs.enzyme.finance/onyx-protocol/user-roles) · [Deploy và upgrade](https://docs.enzyme.finance/onyx-protocol/architecture/deployments-and-upgrades) · [Rủi ro và hạn chế](https://docs.enzyme.finance/onyx-protocol/security/risks-and-limitations) · [SDK](https://docs.enzyme.finance/onyx-sdk) · [Public API](https://api.onyx.enzyme.finance/reference) · [Contract](https://github.com/enzymefinance/protocol-onyx) · [Báo cáo audit](https://github.com/enzymefinance/protocol-onyx/tree/main/audits)

**Chatwoot:** [Tài liệu developer](https://developers.chatwoot.com/introduction) · [Bảng giá](https://www.chatwoot.com/pricing)

**Funding và compliance:** [Paymenture](https://paymenture.com/) · [Bridge developer agreement](https://www.bridge.xyz/legal/developer-agreement) · [Chainalysis sanctions oracle](https://go.chainalysis.com/chainalysis-oracle-docs.html) · [Hướng dẫn năm 2021 của FATF](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html)

Ghi chú chi tiết kèm mọi nguồn và trích dẫn nằm trong `work/notes/01-pillarshub.md`, `02-enzyme-onyx.md`, `03-privy.md` và `04-chatwoot-funding-compliance.md`.

# Phụ lục B: Giả định và gap {.unnumbered}

- **Chưa nhận được PRD của Terrel.** Các nội dung chưa được đối chiếu: rule và độ sâu của Commission, định nghĩa rank, các tính năng back office bắt buộc, yêu cầu (nếu có) để Member xem back office của PillarsHub, việc migrate member hiện có (nếu có).
- **Game và Points:** chưa nhận được tài liệu API. Cần có: cách link account, event schema và cách ký, chống trùng lặp và replay, abuse control, Points rules engine, Points có được quy đổi ra thứ gì hay không.
- **Chưa verify với provider:** auto-placement, giới hạn độ sâu, cách correction Sponsor, mức chi tiết của token permission, rate limit, ý nghĩa của mã 409, bảng giá và chứng nhận bảo mật của PillarsHub; volume limit ở gói trả phí và việc chấp nhận mô hình kinh doanh của Privy; lead time, version đã deploy, ownership của external allowlist và điều khoản thương mại của Enzyme; cơ chế retry webhook của Chatwoot.
- **Bảng giá:** giá công khai của Enzyme khác với giá trong correspondence; bảng giá của PillarsHub không công khai.
- **Năng lực team, ngân sách và launch cohort** chưa được cung cấp; các khoảng thời gian trong lịch trình giả định khoảng năm engineer.

# Phụ lục C: Câu hỏi cho các provider {.unnumbered}

**PillarsHub**

1. Khi tạo customer kèm enroller, node có được tự động đặt vào Unilevel tree với upline chính là enroller không?
2. Độ sâu Genealogy có giới hạn không? List tree node mà không truyền node ID có trả về mọi node không, và page size tối đa là bao nhiêu?
3. Cách correction Sponsor được hỗ trợ và có audit là gì? Có tắt được customer movement không?
4. Mã 409 khi post một source có nghĩa là gì? externalId có unique trong mỗi môi trường không? Customer ID trùng có bị reject không?
5. Có thể có một source group không được bonus nào dùng không? Volume backdate cho các period đã đóng có được chấp nhận không?
6. Có giới hạn access token theo khu vực và chặn thao tác delete được không? Rate limit là bao nhiêu?
7. Webhook có ký được không? Có topic cho placement hoặc source không?
8. Đề nghị xác nhận bằng văn bản rằng reconciliation Genealogy qua API được phép theo Terms, và giải thích GLBA disclaimer trong bối cảnh này.
9. Tài liệu bảo mật, data residency, bảng giá và cách book launch slot.

**Privy**

1. Privy có chấp nhận mô hình kinh doanh này khi được công bố đầy đủ không, và embedded wallet, gas sponsorship và token verification có cần tài khoản Stripe hay Bridge nào không?
2. Transaction volume $1M mỗi tháng được đo thế nào, và vượt mức đó thì gói trả phí áp dụng gì?
3. Có thể thêm production webhook hoặc SLA mà không cần gói Enterprise không?
4. Tài liệu security review cho EIP-7702 delegation dùng trong gas sponsorship.

**Enzyme**

1. Upgrade governance: ai kiểm soát upgrade, thông báo trước bao lâu, và vault của Helm có opt out được không?
2. Version và địa chỉ đã deploy; audit coverage của mọi component Helm dùng, kể cả deployment helper.
3. Xác nhận dùng Sepolia cho test vault, quyền truy cập Admin App trên đó và việc API index Sepolia.
4. Chain production và deposit asset được khuyến nghị cho Arbitrum.
5. Có gắn được một external allowlist do list-owner key của Helm sở hữu ngay lúc deploy không? Độ trễ của indexer?
6. Cấu hình share ở dạng không chuyển nhượng được.
7. Redemption: module notice period hoặc gate; cadence khuyến nghị; cách xử lý một batch bị revert vì một request.
8. Tự động hóa valuation: lead time, chi phí, subscription với data provider.
9. Điều khoản thương mại (deployment fee, phương án theo AUM so với public plan, mức tối thiểu $6,000), bản draft MLA, onboarding form, lead time.
10. Có tắt được investor interface mặc định của Enzyme để Member chỉ dùng Helm không?

**Chatwoot**

1. Cơ chế retry và xử lý lỗi của webhook.
2. Các lựa chọn data residency cho bản Cloud; audit log ở các gói dưới Enterprise.

**Cyclone game team**

1. Tài liệu API, event signing, replay protection, abuse control và Points rules engine.
