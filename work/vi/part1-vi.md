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

**Phần II** (mục 9–16) dành cho team Tech. Phần này làm rõ PRD và đặc tả architecture, data flow, mô hình Genealogy, backlog, launch gate và phân công trách nhiệm.

**Phụ lục** gồm link evidence, giả định, các chi tiết còn mở và câu hỏi gửi provider.

Các nhãn dùng trong tài liệu:

| Nhãn | Ý nghĩa |
|---|---|
| **Verified** | Đã đọc trực tiếp trong documentation, API specification, source code contract hoặc trang pricing của provider vào ngày 8/10/2026 (link tại Phụ lục A). |
| **Correspondence** | Nêu trong trao đổi với provider do Business cung cấp; chưa được kiểm chứng độc lập. |
| **Recommended** | Thiết kế hoặc mặc định do Cyclone đề xuất. Chưa được duyệt. |
| **TBD** | Giả định hoặc vấn đề còn mở. Cần quyết định hoặc xác nhận từ provider. |

Stack đã được chốt: **PillarsHub** (MLM core), **Privy** (login và wallet), **Enzyme Onyx** (hạ tầng vault), **Chatwoot** (support), **Tap Prediction game và Points** của Cyclone, cùng **Helm Web App** custom kèm backend. Tài liệu này không so sánh hay chọn lại provider. Các requirement của Terrel (HELM Community Technology Requirements v0.2, ngày 6/10/2026) được đối chiếu tại mục 9.

# Phần I: Business và khách hàng {.unnumbered}

# Executive overview

**Mục tiêu của Phase 0:** vốn đang chờ được triển khai, nên MVP được cắt gọn thành con đường nhanh nhất để Business **onboarding Member, cho Member tham gia vault (Business gọi là "staking"), ghi nhận Genealogy chính xác và chi trả một khoản Commission Referral đơn giản**. Mọi thứ khác để sau.

**Stack đã chốt đáp ứng được việc này.** Mỗi capability đều có sẵn từ một provider đã chốt, hoặc chỉ cần cấu hình cộng một lượng việc integration có giới hạn từ phía Cyclone. Không có blocker nào (có evidence) buộc phải đổi provider. Các requirement của Terrel (v0.2, ngày 6/10/2026) đã được map vào scope này tại mục 9.

**Member làm được gì khi launch:**

1. Tham gia Helm qua invite link, hoặc được import từ alpha community với lịch sử Referral được giữ nguyên.
2. Login bằng email hoặc social login và tự động có một Helm wallet. Chỉ Member mới chuyển được tiền trong wallet.
3. Wallet Funding bằng cách gửi USDC trên một network từ bất kỳ sàn hoặc wallet nào.
4. Đọc điều khoản vault, Vault Deposit vào vault đã duyệt, xem position đã xác nhận và gửi yêu cầu Redemption.
5. Xem direct team và referral link của mình, và với vai trò Builder, xem Commission ở trạng thái pending, held hoặc paid.
6. Nhận Commission payout bằng USDC trực tiếp vào Helm wallet, theo các batch do Finance duyệt.
7. Chơi Tap Prediction game hiện có và tích Points (không có giá trị tiền mặt).
8. Chat với support ngay trong app; support biết Member là ai và trạng thái của Member, nhưng không bao giờ thấy key.

**Vì sao đây là con đường nhanh nhất mà vẫn khả thi:**

- **Cyclone chỉ build phần kết nối:** trải nghiệm Member, một backend kết nối các provider, một ledger lưu identity, Referral và event, payout executor, cùng các view reconciliation và admin để mọi dòng tiền đều audit được.
- **Mỗi provider làm đúng việc của mình:** Privy lo login và wallet; PillarsHub lưu Genealogy và tính Commission bằng Unilevel plan hiện có; Onyx phát hành vault share và chạy deposit queue, redeem queue; Chatwoot xử lý hội thoại.
- **Payout tận dụng cơ chế batch của PillarsHub.** PillarsHub gửi các payout batch đã duyệt đến một merchant endpoint do Helm build; Helm trả USDC từ một multisig treasury do Business kiểm soát và báo kết quả ngược lại. Verified. Không cần payment provider.
- **Funding trực tiếp bằng crypto** giúp đưa việc onboarding payment provider ra khỏi critical path.

**Những việc làm được ngay (không cần chờ provider hay legal):** khung Helm Web App, Privy login và wallet, data model cho Member, Referral và event, sync với PillarsHub staging, tooling cho alpha import (khi có sample data), payout executor trên testnet, Chatwoot widget, chain indexing, và toàn bộ luồng deposit và Redemption trên testnet Sepolia của Enzyme.

**Những điều kiện để chạy tiền thật và payout** (không điều kiện nào chặn việc build):

1. **Vault strategy và Manager.** Onyx là hạ tầng vault, không phải strategy. Cần chỉ định người chạy strategy, báo cáo giá trị vault và trả thanh khoản cho Redemption. Verified.
2. **Ownership vault và quyền upgrade của Enzyme.** Owner và Admin của vault được protocol tin tưởng hoàn toàn, và Enzyme có thể upgrade vault contract. Cần chốt pháp nhân sở hữu, multisig và điều khoản upgrade trong licence agreement. Verified.
3. **Licence agreement (MLA) và điều khoản thương mại của Enzyme.** Dùng trên production cần có thỏa thuận thương mại. Verified.
4. **Cơ sở tính Commission cho payout đơn giản.** Event nào được trả thưởng (ví dụ một vault deposit đã xác nhận, hoặc doanh thu phí vault), tỷ lệ của ba level, kỳ tính, thời gian hold và mức tối thiểu phải được Owen, Finance và luật sư duyệt. Requirement của Terrel nêu rõ rằng "a raw deposit … must not silently replace approved eligible activity".
5. **Legal review về khả năng áp dụng** đối với pháp nhân vận hành, các quốc gia launch, KYC tier, điều khoản vault và mô hình payout Referral.
6. **Provider chấp nhận business model** bằng văn bản: Privy, Enzyme và PillarsHub.

**Timeline sớm nhất khả thi (ước tính, không phải cam kết):** một test slice end-to-end, gồm cả một test payout, chạy được khoảng 3 tuần sau kickoff; controlled launch có deposit trong khoảng **8–12 tuần**, với điều kiện có câu trả lời về vault, licence, cơ sở tính Commission và legal trước khoảng tuần 6. Live payout đầu tiên diễn ra sau khi kỳ đầu tiên được duyệt đã đóng và hết thời gian hold. Giả định chi tiết ở mục 6; mục 6.1 nêu những gì làm được trong 30 ngày.

# Stack đã chốt: mỗi hệ thống cung cấp gì

```{.mermaid #fig-capabilities caption="Các business capability, platform cung cấp từng capability và phần Cyclone build."}
flowchart TB
  subgraph Capability của Member
    A[Tham gia qua Referral] --- B[Wallet] --- C[Wallet Funding] --- D[Vault Deposit và Redemption] --- E[Commission payout] --- F[Game, Points, support]
  end
  A --> PH[PillarsHub: Genealogy]
  B --> PV[Privy: login và wallet]
  C --> CH[Blockchain: chuyển USDC]
  D --> ON[Enzyme Onyx: vault share và queue]
  E --> PC[PillarsHub tính, Helm trả từ treasury]
  F --> CW[Game của Cyclone; Chatwoot]
  PH & PV & CH & ON & PC & CW --> HB[Helm Web App và backend, do Cyclone build]
```

| Capability | Provider | Cyclone build | Trạng thái |
|---|---|---|---|
| Tham gia và login; một Helm identity ổn định | Privy (login, identity token) | Member record có trạng thái Customer và Builder, mapping Privy sang Helm | Khả thi |
| Wallet | Privy embedded wallet, do Member sở hữu; gas do Helm sponsor | Màn hình wallet; hiển thị balance | Khả thi |
| Referral, Genealogy và alpha import | PillarsHub (customer kèm enroller, Unilevel tree, export toàn bộ tree, placement có ngày) | Ghi nhận Referral và validate, sync, alpha import và reconciliation | Khả thi khi cấu hình |
| Wallet Funding | Blockchain (chuyển USDC đến address của Member) | Hiển thị address, theo dõi confirmation, screening | Khả thi |
| Vault Deposit và Redemption | Enzyme Onyx (deposit queue có allowlist, redeem queue, share, public read API) | Màn hình điều khoản, transaction flow, theo dõi status, cập nhật allowlist | Khả thi khi cấu hình; **chưa chạy tiền thật được** cho đến khi có strategy, MLA và ownership |
| Commission payout đơn giản | PillarsHub (tính real time, bonus release, payout batch đến một custom merchant) | Ghi nhận eligible event, payout executor, treasury proposal, status callback, statement | Khả thi khi cấu hình và có custom work; **bị chặn** cho đến khi cơ sở tính Commission được duyệt |
| Team view | Dữ liệu tree và bonus của PillarsHub | Direct-team view trong Helm, lọc theo permission | Khả thi |
| Game và Points | Tap Prediction và points service của Cyclone | Liên kết account, event đã verify, hiển thị Points | **Khả thi, chờ** documentation của game API |
| Support | Chatwoot Cloud (web widget có identity validation) | Widget, ký identity, agent context view trong Helm admin | Khả thi |
| Vận hành | Dashboard của provider (Onyx Admin App, PillarsHub Portal, Chatwoot) | Helm admin: exception, approval, reconciliation, audit log | Khả thi |

# Member journey

```{.mermaid #fig-journey caption="Member journey chính. Wallet Funding, Vault Deposit và Commission là các event riêng; Points tách biệt với tiền."}
flowchart LR
  I[Invite link] --> S[Signup và login] --> W[Tạo wallet] --> F[Funding wallet bằng USDC] --> T[Đọc điều khoản vault] --> V[Deposit request] --> P[Position được xác nhận] --> C[Sponsor nhận Commission] --> R[Payout vào wallet]
```

1. **Invite và signup.** Member mở invite link của Sponsor và login bằng Privy. Helm ghi nhận Referral Request và xác nhận khi PillarsHub chấp nhận. Member từ alpha community được import cùng Sponsor hiện có.
2. **Wallet.** Privy tạo một embedded wallet. Chỉ Member ký được bằng wallet này; Helm và Privy không chuyển được tiền trong đó.
3. **Wallet Funding.** Helm hiển thị một network và một asset được hỗ trợ (Recommended: USDC trên Arbitrum) cùng address của Member. Funding chỉ chuyển tiền vào wallet của chính Member; đây **không** phải khoản đầu tư và không tạo ra Commission.
4. **Vault Deposit.** Member đọc điều khoản, phí và rủi ro của vault, rồi ký hai transaction: approve để vault lấy số tiền đó, và deposit request. Request ở trạng thái pending cho đến khi vault operations xử lý ở lần valuation kế tiếp. Chỉ khi đó Member mới nắm giữ vault share.
5. **Position.** Helm hiển thị share balance đã xác nhận và giá trị theo lần valuation gần nhất của vault, kèm ngày valuation.
6. **Commission.** Nếu đáp ứng cơ sở tính đã duyệt, PillarsHub tính Commission cho Sponsor (tối đa ba level). Builder thấy Commission ở trạng thái pending, held rồi payable.
7. **Payout.** Sau khi kỳ đóng và hết thời gian hold, Finance duyệt batch. Helm trả USDC từ treasury vào Helm wallet của từng Builder; Builder thấy trạng thái paid kèm transaction reference.
8. **Redemption và engagement.** Member có thể gửi yêu cầu Redemption, được xử lý khi có thanh khoản và hiển thị từng stage, và chơi Tap Prediction để tích Points.

# Phạm vi Phase 0

| In scope (Pilot) | Hoãn lại; giữ ở trạng thái tắt cho đến khi được duyệt |
|---|---|
| Một network và một funding asset (Recommended: USDC trên Arbitrum One) | Mua hoặc top-up tích hợp (Paymenture hoặc tương tự) |
| Một Onyx vault đã duyệt, deposit bất đồng bộ, Redemption theo queue | Thêm chain, asset hoặc vault; deposit tức thì |
| Privy embedded wallet với gas sponsorship | Server wallet, strategy tự động, policy |
| Ghi nhận Referral, trạng thái Customer và Builder, toàn bộ Genealogy trong PillarsHub, alpha import | Tự chuyển placement hoặc chuyển hàng loạt; placement window có kiểm soát (GEN-04 đến GEN-06) |
| **Commission đơn giản:** Unilevel plan ba level hiện có, một eligible event đã duyệt, payout USDC theo batch do Finance duyệt | Rank, quy tắc qualification, matching bonus hoặc leadership bonus, campaign, contest |
| Direct-team view, referral link, trạng thái thu nhập và statement | Team analytics chuyên sâu, công cụ liên hệ cho leader, CRM |
| Tap Prediction game hiện có và Points (không có giá trị tiền mặt) | Quy đổi Points thành giá trị, game mới, token |
| Web chat qua Chatwoot kèm agent context; FAQ và runbook | Support qua Telegram và WhatsApp; AI agent |
| Sanctions screening cho wallet address; điều kiện quốc gia; điều khoản Member | KYC đầy đủ, trừ khi luật sư yêu cầu (quyết định D6) |

# Tóm tắt tính khả thi

| Hạng mục | Kết luận | Evidence chính | Việc còn lại |
|---|---|---|---|
| Login và identity | **Khả thi** | Privy phát hành identity token verify được; một Privy user map với một Helm Member. Verified. | Xác nhận Privy chấp nhận business model. |
| Wallet | **Khả thi** | Embedded EVM wallet do user sở hữu; hỗ trợ Arbitrum; gas sponsorship native; key export. Verified. | Mất login method duy nhất là mất wallet; cần cho thêm login method thứ hai. |
| Genealogy và alpha import | **Khả thi khi cấu hình** | Customer record nhận ID do Helm định nghĩa, ngày signup và enroller ngay khi tạo; list được toàn bộ tree theo một ngày as-of; placement có ghi ngày. Không có bulk import API. Verified. | Dữ liệu alpha; auto-placement, giới hạn depth và cách sửa trên staging. |
| Tính Commission | **Khả thi** | Depth được trả thưởng thiết lập trong plan; custom volume source mang external ID; tính toán real time. Verified. | Cơ sở tính, tỷ lệ, kỳ tính và hold được duyệt; PillarsHub cấu hình plan. |
| Commission payout | **Khả thi với custom work** | PillarsHub gửi release batch đến một custom merchant endpoint, xác thực bằng callback token; merchant báo "Success", "Failure" hoặc "Pending" cho từng payment; cho phép custom currency code. Verified. | Helm build merchant endpoint và treasury executor; approval flow cho Finance. |
| Wallet Funding | **Khả thi** | Chuyển USDC tiêu chuẩn; Helm index chain. | Chọn network và asset. |
| Vault Deposit và Redemption | **Khả thi khi cấu hình; chưa chạy tiền thật được** | Deposit queue có allowlist; Member phải ký; admin execute sau valuation; Redemption theo queue; read-only API. Verified. | Strategy và Manager, MLA, ownership, điều khoản upgrade, quy trình vận hành. |
| Game và Points | **Khả thi, chờ evidence** | Chưa nhận được documentation nào về game. | API documentation, verify event và cơ chế chống abuse. |
| Support | **Khả thi** | Web widget với signed identity; Cloud plan từ $19 mỗi agent mỗi tháng. Verified. | Agent context view; FAQ và runbook (SUP-04 đến SUP-06). |
| Compliance tooling | **Còn thiếu trong stack** | Chưa provider nào đã chốt cung cấp KYC hoặc screening dùng được cho mô hình này. | Luật sư quyết định; thêm screening service ở Helm backend nếu cần. |

# MVP delivery plan

Delivery được tổ chức sao cho engineering không bao giờ phải chờ provider hay legal. Các câu trả lời đó là điều kiện cho **tiền thật và payout**, không phải cho việc build.

| Stage | Thời lượng (ước tính) | Kết quả | Gate sang stage tiếp theo |
|---|---|---|---|
| 0 – Access và quyết định | Tuần 1 | Ghi nhận quyết định của buổi họp; có PillarsHub staging, Privy, Chatwoot, Onyx vault trên Sepolia, documentation của game và alpha sample data | Access được xác nhận |
| 1 – Thin slice end-to-end | Tuần 1–3 | Trên testnet: invite → signup → wallet → Referral được chấp nhận → funding → deposit → position đã execute → test Commission → test payout batch → Redemption | Demo được slice |
| 2 – Build MVP | Tuần 3–8 | UI cho Member có team view và statement, admin approval, diễn tập alpha import, reconciliation, screening, điều khoản, support context, monitoring | Đủ feature trên testnet |
| 3 – Production readiness | Tuần 6–10 (chồng lấn) | Deploy và bàn giao production vault; cấu hình plan và kiểm chứng bằng các ví dụ của Finance; thiết lập treasury multisig; security review; legal sign-off; diễn tập alpha import và payout | Pass launch gate (mục 15) |
| 4 – Controlled launch | Từ khoảng tuần 8–12 | Cohort chỉ theo invite, có giới hạn exposure; payout đầu tiên sau khi kỳ đầu tiên đóng và hết hold | Các check đã thống nhất đều pass, sau đó mở rộng |

## 30-day plan

Những gì thực tế có thể có sau 30 ngày kể từ kickoff, tách theo mức độ phụ thuộc vào engineering và vào các quyết định bên ngoài. Tất cả là ước tính cho team năm đến sáu engineer, có access provider ngay tuần 1.

| Mức | Live tại ngày 30 | Phụ thuộc |
|---|---|---|
| **1. Chắc chắn** (chỉ engineering) | Toàn bộ journey trên testnet: signup → wallet → referral → Wallet Funding bằng USDC → Vault Deposit → position → tính Commission → **test payout batch từ treasury Safe** → Redemption. Alpha import tool đã chạy và reconcile trên sample data. Admin role, maker-checker, reconciliation hằng ngày, Chatwoot | Access test của provider; alpha sample data |
| **2. Nhiều khả năng, nếu Business chốt trong tuần 1** | **Preregistration live với user thật, chưa nhận tiền:** signup, wallet, referral link, Genealogy trên PillarsHub production, alpha community đã import kèm Sponsor và ngày gốc, direct-team view, support. Khớp release sequence của Terrel và ID-04: người preregister giữ attribution nhưng chưa được earn | Member terms và privacy notice; danh sách quốc gia; alpha records; slot production của PillarsHub (thứ Ba đến thứ Năm) |
| **3. Có thể khoảng ngày 30–35, chỉ khi mọi việc bên ngoài đúng hạn** | **Pilot tiền thật có giới hạn:** một cohort được mời (ví dụ leader alpha), có limit mỗi Member và tổng, deposit vào vault production | Xem điều kiện bên dưới |
| **4. Không thực tế trong 30 ngày** | Payout Commission thật đầu tiên; placement window, rank và campaign; full KYC nếu counsel yêu cầu (thêm khoảng 1–2 tuần) | Payout cần cơ sở tính đã duyệt cộng một lần đóng period và hold: khoảng **ngày 45–60** nếu period theo tuần và hold ngắn |

**Điều kiện cho mức 3:**

| Điều kiện | Hạn chót |
|---|---|
| Chỉ định vault strategy và Manager; setup Owner multisig | Tuần 1 |
| Ký MLA với Enzyme; deploy và handover vault production | Ký trong tuần 1–2; deploy xong trước tuần 3 (Enzyme chưa công bố lead time) |
| Counsel xác nhận entity, quốc gia launch, KYC tier và vault terms | Tuần 3 |
| Security review tập trung vào vault configuration, key và integration | Tuần 4 |
| Diễn tập vận hành với một khoản nhỏ của nhà vận hành | Tuần 4 |

**Theo từng tuần:**

| Tuần | Engineering | Business, Finance và counsel |
|---|---|---|
| 1 | Access, environment, Privy login và wallet, member và referral model, PillarsHub staging sync, Onyx Sepolia deposit | Quyết định D1–D12; vault strategy và Manager; MLA; alpha records; soạn cơ sở tính Commission; engage counsel |
| 2 | Thin slice trên testnet; alpha import dry run; event pipeline; payout endpoint và Safe proposal trên testnet | Member và Builder terms; danh sách quốc gia; ký MLA |
| 3 | Team view, statement, admin approval, screening, support context; release candidate cho preregistration | Câu trả lời của counsel; deploy vault production; duyệt cơ sở tính Commission |
| 4 | Preregistration go-live; alpha cutover; kiểm tra load và recovery; fix theo security review; diễn tập tiền thật | Security review; diễn tập vận hành; go/no-go cho pilot có giới hạn |

**Mốc ngày 30 đề xuất chốt tại buổi họp:** *preregistration live, alpha community đã import, Genealogy đã khóa, vault và payout đã chạy đúng trên testnet.* Chạy song song các điều kiện của mức 3 để mở deposit thật ngay khi đủ điều kiện, và duyệt cơ sở tính Commission sớm để payout đầu tiên không bị trễ thêm.

## Giả định và chi phí vận hành

**Giả định đằng sau các khoảng thời gian này:** team Cyclone khoảng năm đến sáu engineer cộng QA và một delivery lead; có access provider và alpha sample data trong tuần 1; documentation game API có trước tuần 2; vault strategy, MLA, ownership, cơ sở tính Commission và câu trả lời legal có trước khoảng tuần 6. PillarsHub chỉ go-live cho khách hàng từ thứ Ba đến thứ Năm, 9:00–16:00 giờ US Mountain Time. Verified. Không ngày nào trong bảng là cam kết.

**Chi phí vận hành tham khảo** (USD mỗi tháng trừ khi ghi khác; giá verified ngày 8/10/2026 ở những mục có ghi):

| Hạng mục | Chi phí | Trạng thái |
|---|---|---|
| Privy | Miễn phí đến 499 monthly active user; $299 đến 2,499; $499 đến 9,999. Free tier gồm $1M transaction volume mỗi tháng. | Verified; phí overage và giới hạn volume của paid tier TBD |
| Gas | Transaction của Member được sponsor cộng transaction payout từ treasury | TBD (theo usage) |
| Enzyme Onyx | Trang public: $2,000 mỗi tháng, hoặc 20% phí vault với mức tối thiểu $6,000 mỗi năm. Correspondence: $5,000 phí deploy cộng 0.25% AUM, hoặc revenue share 20%. | Verified (public) so với Correspondence; **xác nhận lại trong MLA** |
| PillarsHub | Không công bố | TBD |
| Treasury multisig | Safe contract (chỉ tốn gas) | Recommended |
| Chatwoot Cloud | $19 hoặc $39 mỗi agent (Startups, Business); $99 cho Enterprise với audit log và SSO | Verified |
| Sanctions screening cho address | Chainalysis sanctions API miễn phí ở quy mô pilot | Verified (discovery research) |
| KYC service, nếu luật sư yêu cầu | Khoảng $0.33–$1.85 mỗi lượt check theo giá công bố | Verified (discovery research) |
| Security review cho deployment của Helm | Cần báo giá | TBD |

# Tóm tắt security và compliance

- **Custody.** Wallet của Member là self-custodial: chỉ Member ký. Cả Cyclone lẫn Privy đều không chuyển được tiền của Member. Verified (Privy). Vault thì khác: Owner và Admin của vault có thể đặt giá trị share và rút asset của vault về strategy wallet, và Enzyme có thể upgrade contract. Ai giữ các role này, với cơ chế kiểm soát nào, là câu hỏi custody chính cho Business và luật sư.
- **Payout treasury.** Commission được trả từ một multisig treasury do Business sở hữu. Backend của Helm chỉ có thể đề xuất payout transaction; các signer của Finance duyệt. Payout chỉ đi vào Helm wallet của chính Builder, nên không ai có thể chuyển hướng một khoản thanh toán bằng cách đổi địa chỉ nhận (PAY-01).
- **Quyền vào vault kiểm soát được on-chain.** Onyx chỉ cho các wallet address nằm trong allowlist deposit. Helm chỉ thêm address của Member sau khi các eligibility check pass. Verified.
- **Không provider nào trong stack cung cấp KYC hoặc sanctions screening dùng được cho mô hình này.** KYC của Privy chạy trên Bridge, mà điều khoản của Bridge cấm MLM. Nếu luật sư yêu cầu kiểm tra identity, sẽ thêm một screening service ở Helm backend.
- **Tối thiểu trước khi chạy tiền thật hoặc payout, bất kể luật sư kết luận thế nào:** screening cho mọi wallet của Member, nguồn funding và address nhận Redemption; điều kiện quốc gia; điều khoản Member và Builder, công bố rủi ro, phí và thu nhập, privacy notice; một quy trình bằng văn bản để xử lý user và transaction bị flag; payee status là điều kiện bắt buộc để payout (PAY-04).
- **Payout Referral dựa trên hoạt động vault là điểm legal nhạy cảm nhất.** Trả Commission theo deposit gắn phần thưởng với tiền mới đổ vào; luật sư phải duyệt cơ sở tính trước payout đầu tiên. Points không có giá trị tiền mặt và tách biệt khỏi tiền và Commission.
- **Audit của provider không bao gồm deployment của Helm.** Cấu hình vault, key, quy trình valuation, payout executor và các integration của Helm cần security review riêng trước khi đưa tiền vào.

# Các quyết định cần chốt tại buổi họp

| # | Quyết định | Recommended | Vì sao quan trọng |
|---|---|---|---|
| D1 | Network và funding asset | Arbitrum One, USDC native; test trên Ethereum Sepolia | Chốt phạm vi việc cho wallet, vault, payout và indexing |
| D2 | Cơ sở tính Commission cho payout đơn giản | Một eligible event đã duyệt (vault deposit đã xác nhận hoặc doanh thu phí vault), ba level Unilevel, kỳ tính, hold và mức tối thiểu do Owen, Finance và luật sư duyệt; engineering build event pipe ngay bây giờ | Payout không thể go-live nếu thiếu quyết định này; cơ sở tính quyết định rủi ro legal |
| D3 | Vault strategy, Manager và ownership | Business chỉ định Manager; Owner của vault là multisig do Business kiểm soát | Là gate cho tiền thật |
| D4 | Service level cho Redemption | Công bố một target vận hành (ví dụ trong vòng 5 ngày làm việc, tùy thanh khoản) | Member thấy các stage, không phải một cam kết |
| D5 | Top-up tích hợp khi launch | Không; funding trực tiếp bằng crypto | Bỏ một provider ra khỏi critical path |
| D6 | Kiểm tra identity | Luật sư quyết định tier; build sẵn các gate ngay bây giờ; screening address từ ngày đầu | Tránh làm lại nếu bắt buộc KYC |
| D7 | Quy tắc Points | Không có giá trị tiền mặt, không chuyển nhượng được, không trao theo số tiền deposit | Giữ Points tách biệt khỏi hoạt động đầu tư |
| D8 | Member không có Sponsor hợp lệ | Gắn vào root account của công ty, flag để review | Giữ Genealogy đầy đủ |
| D9 | Import alpha community | Import trước khi launch, giữ Sponsor và ngày gốc; reconcile số lượng và edge (GEN-03) | Vốn và các mối quan hệ hiện có được chuyển sang với lịch sử nguyên vẹn |
| D10 | Placement window đã hứa trong field call | Không có trong Pilot; công bố policy trước, sau đó mới bật workflow có kiểm soát (GEN-04 đến GEN-06) | Tránh build tính năng chuyển placement trước khi có quy tắc |
| D11 | Payout treasury và người duyệt | Safe multisig do Business sở hữu; Finance duyệt từng batch; payout chỉ vào Helm wallet của Builder | Kiểm soát payout (PAY-01 đến PAY-04) |
| D12 | Trạng thái của PillarsHub | Đã chốt theo Business; validate bằng các proof scenario T01–T06 của Terrel trên staging, không phải một lần chọn lại | Đối chiếu cách dùng chữ "candidate" của Terrel với stack đã chốt |
