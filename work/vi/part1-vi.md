---
title: "Helm Phase 0: Solution Architecture & MVP Delivery Plan"
subtitle: "Client meeting, ngày 9/10/2026"
author:
  - Cyclone
date: "Draft để thảo luận · v0.1 · evidence verified ngày 8/10/2026"
lang: vi
toc: true
toc-depth: 1
---

# Cách đọc tài liệu {.unnumbered}

**Phần I** (mục 1–8) dành cho Business và khách hàng. Phần này nêu Member làm được gì, platform nào cung cấp từng capability, Cyclone build những gì, MVP có thể launch nhanh đến đâu một cách thực tế và những quyết định cần chốt tại buổi họp. Không cần đọc các mục kỹ thuật.

**Phần II** (mục 9–15) dành cho team Tech. Phần này làm rõ PRD và đặc tả architecture, data flow, mô hình Genealogy, backlog, launch gate và phân công trách nhiệm.

**Phụ lục** gồm link evidence, giả định, các chi tiết còn mở và câu hỏi gửi provider.

Các nhãn dùng trong tài liệu:

| Nhãn | Ý nghĩa |
|---|---|
| **Verified** | Đã đọc trực tiếp trong documentation, API specification, source code contract hoặc trang pricing của provider vào ngày 8/10/2026 (link tại Phụ lục A). |
| **Correspondence** | Nêu trong trao đổi với provider do Business cung cấp; chưa được kiểm chứng độc lập. |
| **Recommended** | Thiết kế hoặc mặc định do Cyclone đề xuất. Chưa được duyệt. |
| **TBD** | Giả định hoặc vấn đề còn mở. Cần quyết định hoặc xác nhận từ provider. |

Stack đã được chốt: **PillarsHub** (MLM core), **Privy** (login và wallet), **Enzyme Onyx** (hạ tầng vault), **Chatwoot** (support), **Tap Prediction game và Points** của Cyclone, cùng **Helm Web App** custom kèm backend. Tài liệu này không so sánh hay chọn lại provider. Chưa có PRD của Terrel; các requirement chưa đối chiếu được với PRD được liệt kê tại Phụ lục B.

# Phần I: Business và khách hàng {.unnumbered}

# Executive overview

**Stack đã chốt đáp ứng được Phase 0.** Mọi capability trong bản PRD draft đều có sẵn từ một provider đã chốt, hoặc chỉ cần cấu hình cộng một ít việc integration từ phía Cyclone. Không có blocker nào (có evidence) buộc phải đổi provider.

**Member làm được gì trong MVP:**

1. Tham gia Helm qua invite link, Sponsor được ghi nhận vĩnh viễn ngay từ ngày đầu.
2. Login bằng email hoặc social login và tự động có một Helm wallet. Chỉ Member mới chuyển được tiền trong wallet.
3. Wallet Funding bằng cách gửi USDC trên một network từ bất kỳ sàn hoặc wallet nào.
4. Đọc điều khoản vault, Vault Deposit vào vault đã duyệt, xem position đã xác nhận và gửi yêu cầu Redemption.
5. Chơi Tap Prediction game hiện có và tích Points (không có giá trị tiền mặt).
6. Chat với support ngay trong app; support biết Member là ai nhưng không bao giờ thấy key.

**Vì sao đây là con đường nhanh nhất mà vẫn khả thi:**

- **Cyclone chỉ build phần kết nối:** trải nghiệm Member, một backend kết nối các provider, một ledger lưu identity của Member, Referral và event, cùng các view reconciliation và admin để mọi dòng tiền đều audit được.
- **Mỗi provider làm đúng việc của mình:** Privy lo login và wallet; PillarsHub lưu Genealogy và sau này tính Commission; Onyx phát hành vault share và chạy deposit queue, redeem queue; Chatwoot xử lý hội thoại.
- **Funding trực tiếp bằng crypto** giúp đưa việc onboarding payment provider ra khỏi critical path.

**Những việc làm được ngay (không cần chờ provider hay legal):** khung Helm Web App, Privy login và tạo wallet, data model cho Member và Referral, sync với PillarsHub staging, Chatwoot widget, chain indexing, và toàn bộ luồng deposit và Redemption trên testnet Sepolia của Enzyme.

**Những điều kiện để chạy tiền thật** (không điều kiện nào chặn việc build):

1. **Vault strategy và Manager.** Onyx là hạ tầng vault, không phải strategy. Cần chỉ định người chạy strategy, báo cáo giá trị vault và trả thanh khoản cho Redemption. Verified.
2. **Ownership vault và quyền upgrade của Enzyme.** Owner và Admin của vault được protocol tin tưởng hoàn toàn, và Enzyme có thể upgrade vault contract. Cần chốt pháp nhân sở hữu, multisig và điều khoản upgrade trong licence agreement. Verified.
3. **Licence agreement (MLA) và điều khoản thương mại của Enzyme.** Dùng trên production cần có thỏa thuận thương mại. Giá public khác với báo giá. Verified.
4. **Legal review về khả năng áp dụng** đối với pháp nhân vận hành, các quốc gia launch, KYC tier và điều khoản vault. Chưa provider nào đã chốt cung cấp KYC hoặc screening dùng được cho mô hình này.
5. **Provider chấp nhận business model** bằng văn bản: Privy, Enzyme và PillarsHub.

**Timeline sớm nhất khả thi (ước tính, không phải cam kết):** một test slice end-to-end chạy được khoảng 3 tuần sau kickoff, và MVP sẵn sàng cho controlled launch trong khoảng **8–12 tuần**, với điều kiện có câu trả lời về vault, licence và legal trước khoảng tuần 6. Giả định chi tiết ở mục 6.

# Stack đã chốt: mỗi hệ thống cung cấp gì

```{.mermaid #fig-capabilities caption="Các business capability, platform cung cấp từng capability và phần Cyclone build."}
flowchart TB
  subgraph Capability của Member
    A[Tham gia qua Referral] --- B[Wallet] --- C[Wallet Funding] --- D[Vault Deposit và Redemption] --- E[Game và Points] --- F[Support]
  end
  A --> PH[PillarsHub: Genealogy]
  B --> PV[Privy: login và wallet]
  C --> CH[Blockchain: chuyển USDC]
  D --> ON[Enzyme Onyx: vault share và queue]
  E --> GM[Game và Points của Cyclone]
  F --> CW[Chatwoot: hội thoại]
  PH & PV & CH & ON & GM & CW --> HB[Helm Web App và backend, do Cyclone build]
```

| Capability | Provider | Cyclone build | Trạng thái |
|---|---|---|---|
| Tham gia và login; một Helm identity ổn định | Privy (login, identity token) | Member record, mapping Privy sang Helm | Khả thi |
| Wallet | Privy embedded wallet, do Member sở hữu; gas do Helm sponsor | Màn hình wallet; hiển thị balance | Khả thi |
| Referral và Genealogy | PillarsHub (customer kèm Sponsor, Unilevel tree, export toàn bộ tree) | Ghi nhận Referral, validate, sync, reconciliation | Khả thi khi cấu hình |
| Wallet Funding | Blockchain (chuyển USDC đến address của Member) | Hiển thị address, theo dõi confirmation, screening | Khả thi |
| Vault Deposit và Redemption | Enzyme Onyx (deposit queue có allowlist, redeem queue, share, public read API) | Màn hình điều khoản, transaction flow, theo dõi status, cập nhật allowlist | Khả thi khi cấu hình; **chưa chạy tiền thật được** cho đến khi có strategy, MLA và ownership |
| Game và Points | Tap Prediction và points service của Cyclone | Liên kết account, event đã verify, hiển thị Points | **Khả thi, chờ** documentation của game API |
| Support | Chatwoot Cloud (web widget có identity validation) | Embed widget, ký identity | Khả thi |
| Vận hành | Dashboard của provider (Onyx Admin App, PillarsHub Portal, Chatwoot) | Helm admin: exception, reconciliation, audit log | Khả thi |

# Member journey

```{.mermaid #fig-journey caption="Member journey chính. Wallet Funding và Vault Deposit là hai bước riêng; Points tách biệt với tiền."}
flowchart LR
  I[Invite link] --> S[Signup và login] --> W[Tạo wallet] --> F[Funding wallet bằng USDC] --> T[Đọc điều khoản vault] --> V[Deposit request] --> P[Position được xác nhận] --> G[Chơi và tích Points] --> R[Yêu cầu Redemption]
```

1. **Invite và signup.** Member mở invite link của Sponsor và login bằng Privy. Helm ghi nhận một Referral Request ở trạng thái pending và xác nhận khi PillarsHub chấp nhận.
2. **Wallet.** Privy tạo một embedded wallet. Chỉ Member ký được bằng wallet này; Helm và Privy không chuyển được tiền trong đó.
3. **Wallet Funding.** Helm hiển thị một network và một asset được hỗ trợ (Recommended: USDC trên Arbitrum) cùng address của Member. Funding chỉ chuyển tiền vào wallet của chính Member; đây **không** phải khoản đầu tư và không tạo quyền hưởng Commission.
4. **Vault Deposit.** Member đọc điều khoản, phí và rủi ro của vault, rồi ký hai transaction: approve để vault lấy số tiền đó, và deposit request. Request ở trạng thái pending cho đến khi vault operations xử lý ở lần valuation kế tiếp. Chỉ khi đó Member mới nắm giữ vault share.
5. **Position.** Helm hiển thị share balance đã xác nhận và giá trị theo lần valuation gần nhất của vault, kèm ngày valuation.
6. **Engagement.** Member chơi Tap Prediction và tích Points. Points không có giá trị tiền mặt và không ảnh hưởng đến Vault Position hay Commission.
7. **Redemption.** Member gửi yêu cầu Redemption. Vault operations xử lý khi có thanh khoản; Helm hiển thị từng stage. Protocol không bảo đảm thời gian xử lý, nên Helm cần công bố một target vận hành.

# Phạm vi Phase 0

| In scope | Hoãn lại, trừ khi Business yêu cầu ngay khi launch |
|---|---|
| Một network và một funding asset (Recommended: USDC trên Arbitrum One) | Mua hoặc top-up tích hợp (Paymenture hoặc tương tự) |
| Một Onyx vault đã duyệt, deposit bất đồng bộ, Redemption theo queue | Thêm chain, asset hoặc vault; deposit tức thì |
| Privy embedded wallet với gas sponsorship | Server wallet, strategy tự động, policy |
| Ghi nhận Referral và toàn bộ Genealogy trong PillarsHub | Accrual và payout Commission (quyết định D2) |
| Tap Prediction game hiện có và Points | Game mới, token, quy đổi Points thành giá trị |
| Web chat qua Chatwoot | Support qua Telegram và WhatsApp |
| Helm admin cho exception, reconciliation và audit | Làm lại dashboard của provider |
| Sanctions screening cho wallet address; điều kiện quốc gia; điều khoản Member | KYC đầy đủ, trừ khi luật sư yêu cầu (quyết định D6) |

# Tóm tắt tính khả thi

| Hạng mục | Kết luận | Evidence chính | Việc còn lại |
|---|---|---|---|
| Login và identity | **Khả thi** | Privy phát hành identity token verify được; một Privy user map với một Helm Member. Verified. | Xác nhận Privy chấp nhận business model. |
| Wallet | **Khả thi** | Embedded EVM wallet do user sở hữu; hỗ trợ Arbitrum; gas sponsorship native; key export. Verified. | Mất login method duy nhất là mất wallet; cần cho thêm login method thứ hai. |
| Genealogy | **Khả thi khi cấu hình** | Customer record nhận ID do Helm định nghĩa và Sponsor ngay khi tạo; list được toàn bộ tree theo một ngày as-of. Verified. | Xác nhận auto-placement trong tree, giới hạn depth, cách sửa Sponsor, permission của token. |
| Commission (chuẩn bị cho Phase 1) | **Khả thi** | Depth được trả thưởng thiết lập trong plan, không phải trong tree; có custom volume type; payout là một bước riêng. Verified. | Quyết định có accrue gì trong Phase 0 hay không. |
| Wallet Funding | **Khả thi** | Chuyển USDC tiêu chuẩn; Helm index chain. | Chọn network và asset. |
| Vault Deposit và Redemption | **Khả thi khi cấu hình; chưa chạy tiền thật được** | Deposit queue có allowlist; Member phải ký; admin execute sau valuation; Redemption theo queue; read-only API. Verified. | Strategy và Manager, MLA, ownership, điều khoản upgrade, quy trình vận hành. |
| Game và Points | **Khả thi, chờ evidence** | Chưa nhận được documentation nào về game. | API documentation, verify event và cơ chế chống abuse. |
| Support | **Khả thi** | Web widget với signed identity; Cloud plan từ $19 mỗi agent mỗi tháng. Verified. | Chọn plan; xác nhận việc host data tại Mỹ là chấp nhận được. |
| Compliance tooling | **Còn thiếu trong stack** | Chưa provider nào đã chốt cung cấp KYC hoặc screening dùng được cho mô hình này. | Luật sư quyết định; thêm screening service ở Helm backend nếu cần. |

# MVP delivery plan

Delivery được tổ chức sao cho engineering không bao giờ phải chờ provider hay legal. Các câu trả lời đó là điều kiện cho **tiền thật**, không phải cho việc build.

| Stage | Thời lượng (ước tính) | Kết quả | Gate sang stage tiếp theo |
|---|---|---|---|
| 0. Access và quyết định | Tuần 1 | Ghi nhận quyết định của buổi họp; có PillarsHub staging, Privy app, Chatwoot, Onyx vault trên Sepolia và documentation của game | Access được xác nhận |
| 1. Thin slice end-to-end | Tuần 1–3 | Trên testnet: invite → signup → wallet → Referral được PillarsHub chấp nhận → funding → deposit request → position đã execute → Redemption; một flow từ game đến Points | Demo được slice |
| 2. Build MVP | Tuần 3–8 | Toàn bộ UI cho Member, admin và xử lý exception, reconciliation, screening, điều khoản, support, monitoring | Đủ feature trên testnet |
| 3. Production readiness | Tuần 6–10 (chồng lấn) | Deploy và bàn giao production vault, security review cho deployment của Helm, legal sign-off, diễn tập vận hành | Pass launch gate (mục 14) |
| 4. Controlled launch | Từ khoảng tuần 8–12 | Cohort chỉ theo invite, có giới hạn exposure | Các check đã thống nhất đều pass, sau đó mở rộng |

**Giả định đằng sau các khoảng thời gian này:** team Cyclone khoảng năm engineer cộng QA và một delivery lead; có access PillarsHub, Privy và Chatwoot trong tuần 1; test vault của Enzyme sẵn sàng trong tuần 1; documentation game API có trước tuần 2; vault strategy, MLA, quyết định ownership và câu trả lời legal có trước khoảng tuần 6. PillarsHub chỉ go-live cho khách hàng từ thứ Ba đến thứ Năm, 9:00–16:00 giờ US Mountain Time, nên ngày go-live bị giới hạn theo lịch này. Verified. Không ngày nào trong bảng là cam kết.

**Chi phí vận hành tham khảo** (USD mỗi tháng trừ khi ghi khác; giá verified ngày 8/10/2026 ở những mục có ghi):

| Hạng mục | Chi phí | Trạng thái |
|---|---|---|
| Privy | Miễn phí đến 499 monthly active user; $299 đến 2,499; $499 đến 9,999. Free tier gồm $1M transaction volume mỗi tháng. | Verified; phí overage và giới hạn volume của paid tier TBD |
| Gas sponsorship | Gas của network cộng phí Privy | TBD (theo usage) |
| Enzyme Onyx | Trang public: $2,000 mỗi tháng, hoặc 20% phí vault với mức tối thiểu $6,000 mỗi năm. Correspondence: $5,000 phí deploy cộng 0.25% AUM, hoặc revenue share 20%. | Verified (public) so với Correspondence; **xác nhận lại trong MLA** |
| PillarsHub | Không công bố | TBD |
| Chatwoot Cloud | $19 hoặc $39 mỗi agent (Startups, Business); $99 cho Enterprise với audit log và SSO | Verified |
| Sanctions screening cho address | Chainalysis sanctions API miễn phí ở quy mô pilot | Verified (discovery research) |
| KYC service, nếu luật sư yêu cầu | Khoảng $0.33–$1.85 mỗi lượt check theo giá công bố | Verified (discovery research) |
| Security review cho deployment của Helm | Cần báo giá | TBD |

# Tóm tắt security và compliance

- **Custody.** Wallet của Member là self-custodial: chỉ Member ký. Cả Cyclone lẫn Privy đều không chuyển được tiền của Member. Verified (Privy). Vault thì khác: Owner và Admin của vault có thể đặt giá trị share và rút asset của vault về strategy wallet, và Enzyme có thể upgrade contract. Ai giữ các role này, với cơ chế kiểm soát nào, là câu hỏi custody chính cho Business và luật sư.
- **Quyền vào vault kiểm soát được on-chain.** Onyx chỉ cho các wallet address nằm trong allowlist deposit. Helm chỉ thêm address của Member sau khi các eligibility check pass. Verified.
- **Không provider nào trong stack cung cấp KYC hoặc sanctions screening dùng được cho mô hình này.** KYC của Privy chạy trên Bridge, mà điều khoản của Bridge cấm MLM. Nếu luật sư yêu cầu kiểm tra identity, sẽ thêm một screening service ở Helm backend. Việc này chỉ thêm một service, không đổi stack.
- **Tối thiểu trước khi chạy tiền thật, bất kể luật sư kết luận thế nào:** sanctions screening cho mọi wallet address của Member, nguồn funding và address nhận Redemption; điều kiện quốc gia; điều khoản Member, công bố rủi ro và phí, privacy notice; một quy trình bằng văn bản để xử lý user và transaction bị flag.
- **Points và Referral.** Points không có giá trị tiền mặt và tách biệt khỏi tiền và Commission. Mô hình Referral và mọi liên hệ giữa Points và deposit vẫn cần luật sư review; chỉ riêng tính chất non-cash không phải là căn cứ miễn trừ.
- **Audit của provider không bao gồm deployment của Helm.** Cấu hình vault, key, quy trình valuation và các integration của Helm cần security review riêng trước khi đưa tiền vào.

# Các quyết định cần chốt tại buổi họp

| # | Quyết định | Recommended | Vì sao quan trọng |
|---|---|---|---|
| D1 | Network và funding asset | Arbitrum One, USDC native; test trên Ethereum Sepolia | Chốt phạm vi việc cho wallet, vault và indexing |
| D2 | Commission trong Phase 0 | Ghi nhận Genealogy và vault event, nhưng không accrue hay payout Commission | Tránh nghĩa vụ chi trả ngầm định; Phase 1 có thể backfill từ dữ liệu của Helm |
| D3 | Vault strategy, Manager và ownership | Business chỉ định Manager; Owner của vault là multisig do Business kiểm soát | Là gate cho tiền thật |
| D4 | Service level cho Redemption | Công bố một target vận hành (ví dụ trong vòng 5 ngày làm việc, tùy thanh khoản) | Member thấy các stage, không phải một cam kết |
| D5 | Top-up tích hợp khi launch | Không; funding trực tiếp bằng crypto | Bỏ một provider ra khỏi critical path |
| D6 | Kiểm tra identity | Luật sư quyết định tier; build sẵn các gate ngay bây giờ; screening address từ ngày đầu | Tránh làm lại nếu bắt buộc KYC |
| D7 | Quy tắc Points | Không có giá trị tiền mặt, không chuyển nhượng được, không trao theo số tiền deposit | Giữ Points tách biệt khỏi hoạt động đầu tư |
| D8 | Member không có Sponsor hợp lệ | Gắn vào root account của công ty, flag để review | Giữ Genealogy đầy đủ |
