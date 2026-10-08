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
- **Màn hình MLM được tái sử dụng, không build lại.** Duyệt Genealogy, chỉnh Sponsor và placement, cấu hình plan, review bonus, đóng period và release bonus đều làm trong PillarsHub Portal. Builder có các phần thiết yếu ngay trong Helm, cùng một link "Open full back office" mở vào back office của PillarsHub qua single sign-on. Verified (SSO). Helm chỉ build những gì PillarsHub chưa có.
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
| Team view và Builder back office | Back office của PillarsHub (tree, report, chi tiết bonus) qua SSO | Phần thiết yếu trong Helm (referral link, số lượng team, tóm tắt earning, payout) và bước chuyển sang qua SSO | Khả thi |
| Quản trị MLM | PillarsHub Portal (Genealogy, placement, plan, bonus, đóng period, release) | Deep link theo Member ID; phát hiện thay đổi và reconciliation | Khả thi |
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
| Referral link, số lượng team, tóm tắt earning và payout trong Helm; back office đầy đủ trong PillarsHub qua SSO | Bản Helm tự build của các màn hình PillarsHub; team analytics chuyên sâu, công cụ liên hệ cho leader, CRM |
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
| 1 | Access, environment, Privy login và wallet, member và referral model, PillarsHub staging sync, Onyx Sepolia deposit | Quyết định D1–D13; vault strategy và Manager; MLA; alpha records; soạn cơ sở tính Commission; engage counsel |
| 2 | Thin slice trên testnet; alpha import dry run; event pipeline; payout endpoint và Safe proposal trên testnet | Member và Builder terms; danh sách quốc gia; ký MLA |
| 3 | Phần thiết yếu cho Builder và PillarsHub SSO, admin approval, screening, support context; release candidate cho preregistration | Câu trả lời của counsel; deploy vault production; duyệt cơ sở tính Commission |
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
| D13 | MLM admin và Builder back office | Dùng PillarsHub Portal và back office (SSO) thay vì build trong Helm; Helm chỉ hiển thị phần thiết yếu | Tiết kiệm nhiều tuần làm UI; cần xác nhận cơ chế approval của PillarsHub Portal và cách xử lý SSO token |

# Phần II: Triển khai kỹ thuật {.unnumbered}

# Traceability với requirement của Terrel

Tài liệu *HELM Community Technology Requirements v0.2* của Terrel (ngày 6/10/2026) định nghĩa "Must" là bắt buộc **trước khi capability tương ứng được bật**, và nêu rõ capability bị hoãn thì giữ ở trạng thái tắt. Nhờ vậy Phase 0 có thể bật đầy đủ một nhóm nhỏ capability, thay vì bật một phần cho tất cả. Bảng dưới đây map từng nhóm requirement vào Phase 0 Pilot.

| Nhóm | Requirement ID | Cách xử lý trong Phase 0 Pilot | Vị trí trong tài liệu |
|---|---|---|---|
| Identity và member record | ID-01 đến ID-04 | **Trong scope.** Person ID ổn định; status Customer và Builder; các trạng thái prospect, preregistered, verified và enrolled; eligibility theo quốc gia và version của agreement | FR-1, FR-15; mục 13 |
| Quản trị phía công ty | ADM-01 đến ADM-03 | **Trong scope.** Tách riêng các role view, configure, correct, approve và release; maker-checker cho Sponsor correction, hold và payout release; môi trường test | FR-13, FR-19; mục 11.3 |
| Lifecycle action | ADM-04 | Merge và recovery nằm trong scope dưới dạng quy trình admin; suspension, termination và re-entry **bị tắt** cho đến khi được bật | Mục 13.2 |
| Sponsor và Genealogy | GEN-01 đến GEN-03 | **Trong scope.** Referrer, sponsor (enroller) và placement được ghi riêng kèm effective date; check loop và trùng lặp; **alpha import có reconciliation** | FR-3, FR-4, FR-20; mục 13 |
| Placement window | GEN-04 đến GEN-06 | **Bị tắt** cho đến khi placement policy được duyệt (quyết định D10); data model đã lưu sẵn Referral gốc và lịch sử | Mục 13.2 |
| Compensation | COMP-01 đến COMP-04 | **Trong scope, chỉ plan đơn giản.** Một eligible event đã được duyệt, Unilevel ba tầng có version, event replay-safe, các trạng thái calculated, pending, held, payable và paid, reconciliation tới batch | FR-17, FR-18; mục 12, 13.4 |
| Qualification và rank | QUAL-01 đến QUAL-03 | **Bị tắt.** Plan đơn giản không có rank; QUAL-03 chỉ áp dụng khi có cam kết về tiến độ rank | Bảng scope |
| Earnings audit | AUD-01 đến AUD-03 | **Trong scope.** Giải thích từng khoản earning từ source event đến payout; giữ lại các correction; statement theo period tách hiệu quả vault khỏi earning từ Referral | FR-18, FR-19 |
| Rewards | REW-01 đến REW-03 | Chỉ Points; không redemption, promotional credit hay quy đổi ra tiền mặt | FR-11; quyết định D7 |
| Builder back office | BO-01, BO-02, BO-04 | **Trong scope.** Phần thiết yếu trong Helm (referral link, số lượng team, tóm tắt earning, payout, dispute request); statement chi tiết và tree nằm trong back office của PillarsHub qua SSO; mobile web và ngôn ngữ của release (hành vi trên mobile của back office PillarsHub: TBD) | FR-16, FR-19 |
| Team visibility | TEAM-01, TEAM-02 | **Trong scope, mức tối thiểu.** Direct team và số lượng; không truy cập được nhánh khác hay balance, trade, support case của bất kỳ ai | FR-16 |
| Team tool | TEAM-03 đến TEAM-05 | Chỉ có bước welcome cơ bản (TEAM-05 Pilot); search, contact và automation được hoãn | Bảng scope |
| Campaign | CAMP-01 | **Trong scope.** Attribution qua Referral link, thứ tự ưu tiên và Referral không hợp lệ; CAMP-02 đến CAMP-04 bị tắt | FR-3 |
| Business intelligence | BI-01, BI-02 | **Trong scope.** Định nghĩa riêng cho customer, Builder, deposit, Commission, liability và payout; reconciliation với nguồn | FR-14 |
| Payout | PAY-01 đến PAY-04 | **Trong scope.** Payout instruction từ các khoản payable đã duyệt; giới hạn địa chỉ đích; theo dõi trạng thái; reconciliation; payee status | FR-18; mục 12, 15 |
| API và event | API-01 đến API-03 | **Trong scope.** Sandbox, event ID ổn định, replay và backfill, polling ở những chỗ webhook không an toàn; **quyền export ghi trong hợp đồng** | Mục 11, 12; launch gate |
| Support | SUP-01 đến SUP-07 | **Trong scope (Pilot).** Context view cho agent, case link tới person ID và event ID, giới hạn quyền agent, FAQ và runbook, metric | FR-12 |
| Compliance record | REC-01, REC-02 | **Trong scope.** Agreement, consent và disclosure có version; giới hạn theo quốc gia và sản phẩm kèm version của rule | FR-15; mục 15.3 |
| Vận hành | OPS-01 đến OPS-04 | **Trong scope.** Load envelope, recovery target, incident response, gate theo từng capability | Mục 15 |
| Triển khai | IMP-01 đến IMP-04 | **Trong scope.** Kế hoạch có owner, diễn tập migration, release acceptance, bàn giao | Mục 14, 15 |

**Những điểm tài liệu này khác với bản draft của Terrel:**

- **Trạng thái provider.** Bản draft của Terrel liệt kê Pillars và Infinite MLM Software là ứng viên, chưa chọn bên nào. Business sau đó đã xác nhận PillarsHub. Tài liệu này coi PillarsHub là đã được xác nhận và đề xuất chạy các proof scenario của Terrel như bước **validation** cấu hình (quyết định D12), không phải một vòng lựa chọn mới.
- **Proof scenario cho Pilot.** T01 (alpha migration), T02 (case thông thường và case biên của plan), T03 (event trùng và replay), T05 (reversal trước và sau payout), T06 (payout timeout và retry), T07 (giới hạn quyền truy cập của leader) và T11 (Customer, Builder và dual role) là gate cho Pilot. T04, T09, T12 và T13 là gate cho các capability liên quan khi chúng được bật. T10 và T14 là gate cho việc bàn giao production.
- **Vẫn còn thiếu trong danh sách "Waiting for" của Terrel:** compensation specification kèm ví dụ cụ thể, record enrollment và Genealogy của alpha, và release scope một trang (đối tượng, quốc gia, ngôn ngữ, hoạt động).

# PRD high-level đã chỉnh sửa

## Mục tiêu

1. Onboard Member, gồm cả alpha community, với một identity ổn định duy nhất và một wallet self-custodial dùng được ngay.
2. Cho phép Member nạp crypto vào wallet và tham gia vault đã được duyệt, kèm một luồng Redemption dùng được trong thực tế.
3. Ghi nhận Genealogy đầy đủ, với referrer, sponsor và placement được lưu riêng, ngay từ lượt signup đầu tiên.
4. Chi trả Commission ba tầng đơn giản trên một eligible event đã được duyệt, theo các batch USDC do Finance duyệt.
5. Tái sử dụng game Tap Prediction và Points hiện có để tăng engagement.

## Personas

- **Member (Customer):** tham gia qua Referral, nạp tiền vào wallet, deposit, chơi game, redeem, liên hệ support.
- **Builder:** Member được enroll để giới thiệu người khác; thấy Referral link, direct team và trạng thái Commission; nhận payout. Không phải Member nào cũng là Builder (ID-01).
- **Operations administrator:** review exception về Referral, import và Wallet Funding, quản lý allowlist của vault, theo dõi queue và reconciliation, xử lý escalation.
- **Finance approver:** review và duyệt payout batch và hold; ký transaction của treasury.
- **Vault operator** (do Business chỉ định): cập nhật valuation của vault, execute deposit queue và redeem queue, quản lý thanh khoản. Dùng Onyx Admin App.
- **Support agent:** trả lời Member trên Chatwoot với context read-only; không được chuyển tiền, đổi Sponsor, release payout hay cộng Points.
- **Business reviewer:** xem báo cáo funnel, mức tham gia, Referral, Commission và engagement.

## Functional requirements và acceptance criteria

| ID | Requirement | Acceptance criteria |
|---|---|---|
| FR-1 | Xác thực bằng Privy và resolve về một Helm member duy nhất | Login lại bằng bất kỳ phương thức đã link nào đều resolve về cùng một Helm member ID; backend verify mọi Privy token; trường hợp trùng người được đưa vào admin queue (ID-02) |
| FR-2 | Tạo một embedded EVM wallet cho mỗi Member | Wallet có sẵn sau lần login đầu tiên; địa chỉ được đọc từ Privy ở server-side; Member ký được một transaction thử; app giải thích cơ chế recovery và export |
| FR-3 | Ghi nhận Referral Request khi signup | Invite link được lưu trước khi login và gắn với Member mới; áp dụng thứ tự ưu tiên và window của attribution (CAMP-01); self-referral bị từ chối; Sponsor thiếu hoặc không hợp lệ xử lý theo rule D8 |
| FR-4 | Accept Sponsor Edge trong PillarsHub | Customer được tạo với ID do Helm định nghĩa, ngày signup và enroller; node được read-back với upline đúng như kỳ vọng; edge chỉ được đánh dấu accepted sau khi read-back; retry không bao giờ tạo bản trùng; referrer gốc được giữ trong Helm (GEN-01) |
| FR-5 | Hiển thị network và asset được hỗ trợ để nạp tiền | Chỉ cung cấp một network và một asset; có cảnh báo sai network; Wallet Funding đi qua các trạng thái submitted → confirmed (N block) → credited; transfer lỗi hoặc không được hỗ trợ chuyển sang exception |
| FR-6 | Screening địa chỉ | Wallet của Member khi tạo, mỗi funding source và mỗi địa chỉ đích của Redemption đều được screening; nếu có hit thì việc đưa vào allowlist của vault, payout hoặc action tương ứng bị chặn và một case được mở |
| FR-7 | Gate quyền truy cập vault | Member phải chấp nhận vault terms hiện hành (có version) và qua eligibility check; chỉ khi đó wallet mới được thêm vào allowlist của Onyx |
| FR-8 | Vault Deposit | Member ký approval đúng số tiền và deposit request; Helm theo dõi approval → request → pending → executed hoặc cancelled; position chỉ được tính sau khi execute |
| FR-9 | Hiển thị position | Số share và giá trị theo lần valuation gần nhất của vault, kèm timestamp của valuation; khớp với state on-chain |
| FR-10 | Redemption | Member ký redemption request; Helm hiển thị pending, awaiting liquidity, executed, cancelled; asset về wallet của Member; position, business event và mọi điều chỉnh Commission (nếu có) đi theo rule đã duyệt |
| FR-11 | Game và Points | Game account được link; event đã verify chỉ cộng Points một lần; rule và daily limit được hiển thị; Points tách biệt với tiền (REW-01) |
| FR-12 | Support | Identity trong chat đã được verify; context view của agent hiển thị identity, status Customer hoặc Builder, community status, trạng thái earning và payout, lịch sử case (SUP-01); case link tới person ID và event ID (SUP-04); action của agent bị giới hạn (SUP-05); FAQ và runbook có version (SUP-06); logout sẽ reset chat |
| FR-13 | Admin và reconciliation | Tách riêng các role view, configure, correct, approve và release (ADM-01); reconciliation hằng ngày cho Genealogy, Wallet Funding, Vault Position, Commission, payout và Points; sai lệch xuất hiện trong exception queue kèm audit trail |
| FR-14 | Reporting | Định nghĩa riêng cho customer, Builder, deposit, Commission, liability và payout, có hiển thị cutoff và độ mới của dữ liệu, không đếm trùng (BI-01, BI-02) |
| FR-15 | Status Customer và Builder, preregistration | Các trạng thái prospect, preregistered, verified và enrolled được theo dõi riêng; Builder enrollment là bước tường minh và có version; người ở trạng thái preregistered không được nhận earning (ID-04); capability bị giới hạn sẽ bị chặn theo quốc gia và version của agreement (ID-03, REC-02) |
| FR-16 | Team view | Builder thấy Referral link và số lượng direct team kèm độ mới của dữ liệu trong Helm, và mở back office của PillarsHub qua SSO để xem tree và report; cả hai view đều không để lộ nhánh khác hay balance, position, trade hoặc support case của bất kỳ ai (TEAM-01, TEAM-02, BO-01; cần xác nhận visibility setting của PillarsHub) |
| FR-17 | Post eligible event để tính Commission | Chỉ eligible event type đã được duyệt mới được post, sau khi confirmed on-chain, kèm external ID ổn định; replay chỉ tạo một obligation; reversal tạo một adjustment truy vết được (COMP-01, COMP-02) |
| FR-18 | Payout đơn giản | Bonus đã release được gửi về dưới dạng batch của PillarsHub tới merchant endpoint của Helm; Finance duyệt; Helm chỉ propose treasury transaction tới chính Helm wallet của Builder; mỗi payment được báo lại là Success, Failure hoặc Pending kèm transaction reference; một lần timeout và retry chỉ tạo ra một payment hoặc một exception tường minh (PAY-01 đến PAY-03, T06) |
| FR-19 | Earnings statement và dispute | Builder thấy tóm tắt earning và payout trong Helm, còn statement bonus chi tiết nằm trong back office của PillarsHub; các trạng thái hiển thị gồm calculated, pending, held, payable và paid kèm lý do (COMP-03); statement theo period tách hiệu quả vault khỏi earning từ Referral (AUD-03); dispute request mang theo earning ID (BO-02) |
| FR-20 | Import alpha community | Alpha member được import theo thứ tự Sponsor trước, giữ ngày gốc và provenance "import"; số lượng và edge khớp khi reconcile; exception được giải quyết hoặc được duyệt; rollback đã được diễn tập (GEN-03, IMP-02, T01) |

## Operational requirements

- Mọi integration write đều idempotent từ phía Helm, có retry với backoff và được reconciliation hằng ngày (API-02).
- Không private key, seed phrase hay credential đặc quyền nào của provider được lọt vào browser, log hoặc payload gửi cho support (SUP-03).
- Môi trường test và production tách riêng cho mọi provider, với credential riêng (ADM-03).
- Monitoring và alert cho: valuation của vault quá cũ, deposit hoặc redemption request pending quá target, reconciliation bị lệch, sync lỗi, screening có hit, payout batch không được confirmed trong khoảng thời gian đã thống nhất.
- Thống nhất load envelope (số người, độ sâu tree, số event mỗi giờ) và recovery target trước khi test production (OPS-01, OPS-03).

## Success metrics (target TBD)

Thời gian đến live deposit đầu tiên được duyệt và đến payout đầu tiên; tỷ lệ hoàn tất signup; conversion từ signup sang funded và từ funded sang deposited; độ đầy đủ của referral attribution (target 100% signup được accept); reconciliation của alpha import (target không có chênh lệch nào không giải thích được); độ chính xác của payout batch; số reconciliation exception mỗi tuần; mức tham gia game; first-response time và resolution time của support.

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
    ADM[Admin console và approval]
    PAYX[Payout executor: merchant endpoint]
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
  PH -->|payout batch| PAYX
  PAYX -->|propose transfer| SAFE[(Treasury Safe multisig)]
  SAFE -->|USDC tới Builder wallet| CHAIN
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
| Admin console và approval | Chỉ dữ liệu do Helm sở hữu: exception, screening case, trạng thái allowlist, import exception, thực thi payout và hold, có maker-checker; deep link sang PillarsHub Portal cho Genealogy, plan, bonus và release | PillarsHub Portal lo phần quản trị MLM; Helm lo identity, wallet và dòng tiền |
| PillarsHub Portal và back office (tái sử dụng) | Duyệt Genealogy, chỉnh Sponsor và placement, plan, bonus, đóng period, release, report MLM; Builder back office qua SSO | Không tự build: tái sử dụng để tiết kiệm thời gian build |
| Payout executor | Nhận payout batch của PillarsHub tại một custom merchant endpoint; validate callback token; check payee và hold; propose USDC transfer tới treasury multisig; báo Success, Failure hoặc Pending cho từng payment | PillarsHub tính toán và release nhưng không chuyển crypto; không có payment provider nào trong scope |
| Alpha import tool | Load alpha member theo thứ tự Sponsor trước, reconcile số lượng và edge, báo cáo exception, hỗ trợ rollback | PillarsHub không có bulk import API. Verified |

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
| Commission obligation (calculated, released) | Bonus và batch của **PillarsHub** | Bản copy statement kèm source event ID |
| Thực thi payout | Blockchain (treasury transfer) | Payout record kèm batch ID, payment ID và transaction ID; status được báo lại cho PillarsHub |
| Status Customer và Builder, preregistration | Helm DB | Master; mirror sang customer type và status trong PillarsHub |
| Points balance | Cyclone points service | Bản copy để hiển thị |
| Conversation | Chatwoot | Link tới member ID |
| Terms acceptance, kết quả screening, eligibility | Helm DB | Master |

## Ranh giới về credential, signing và custody

| Actor | Được ký hoặc thực hiện | Không được | Ghi chú |
|---|---|---|---|
| Member | Transfer từ wallet, approval cho vault, deposit request và redemption request, cancel | Admin action | Privy embedded wallet; Onyx yêu cầu chính địa chỉ của Member ký request. Verified |
| Helm backend | Write vào PillarsHub (customer, node, source) bằng token giới hạn quyền; game API; screening API; cập nhật allowlist của vault qua list-owner key; **propose** treasury payout transaction | Chuyển tiền của Member; vault admin action; thực thi payout khi chưa có chữ ký của Finance | List-owner key nằm trong key management service; chỉ sở hữu allowlist contract (cần xác nhận với Enzyme) |
| Vault Owner (Business) | Thêm và gỡ Admin; mọi admin action | — | Recommended: Safe multisig với signer thuộc Business |
| Vault Admin / operator (Business) | Cập nhật valuation; execute queue; chuyển asset sang strategy wallet; set fee | — | Được protocol tin cậy hoàn toàn. Verified |
| Treasury signer (Finance) | Duyệt và ký payout transaction từ treasury multisig | Đổi địa chỉ đích của payout | Payout chỉ đi tới Helm wallet của Builder; cần đủ threshold chữ ký của các Finance signer |
| Strategy Manager (do Business chỉ định) | Chạy strategy bên ngoài Onyx; trả lại thanh khoản | — | Custody của strategy wallet nằm ngoài Onyx. Verified |
| Enzyme | Deploy; upgrade contract (global owner) | — | Upgrade governance phải được quy định trong MLA. Verified |
| Privy | Vận hành signing enclave | Ký thay Member | Privy "is never an authorized signer". Verified |
| Support agent | Trả lời trên Chatwoot; xem member status ở chế độ read-only | Tiền, Sponsor, Points | Được enforce trong Helm admin |

Token PillarsHub gắn với từng môi trường và không hết hạn; có thể cấu hình read-only. Recommended: một token read-only cho reconciliation và một write token riêng, chặn các khu vực destructive nếu PillarsHub hỗ trợ (TBD). Bonus release và tạo batch là action của Finance trên PillarsHub Portal, không phải call từ backend của Helm; Helm chỉ nhận batch kết quả và báo lại payment status.

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

```{.mermaid #fig-flow-payout caption="Từ eligible event đến Commission và payout đơn giản."}
sequenceDiagram
  participant H as Helm backend
  participant X as PillarsHub
  participant F as Finance approver
  participant T as Treasury Safe
  participant B as Builder wallet
  H->>X: post eligible event (externalId = chain:tx:log)
  X->>X: tính Commission 3 tầng (pending)
  F->>X: đóng period, qua hold, release bonus
  X->>H: payout batch (callback token)
  H->>H: validate token, payee status, hold
  H->>T: propose USDC transfer
  F->>T: duyệt và ký (threshold)
  T->>B: USDC transfer
  H->>X: báo Success / Failure / Pending cho từng payment
  H->>H: cập nhật statement, reconcile
```

## Flow matrix

| Flow | Nguồn → đích | Dữ liệu tối thiểu | Source of truth | Deduplication key | Lỗi và retry | User thấy |
|---|---|---|---|---|---|---|
| Signup và Referral | App → Helm → PillarsHub | Privy DID, wallet address, invite code, member ID của Sponsor | Tree của PillarsHub (edge đã accept) | Helm member ID (customer ID trong PillarsHub) | Lookup trước khi create; backoff; dead letter chuyển cho ops; tree reconciliation hằng đêm | "Referral pending" rồi "confirmed" |
| Wallet Funding | Sàn → chain → Helm indexer | Chain, tx hash, log index, amount, from, to | Chain | (chain, tx hash, log index) | Re-index từ safe block gần nhất; xử lý reorg dựa trên confirmation depth | Balance pending → confirmed |
| Vault Deposit | App → Onyx contract; indexer → Helm | Request ID, amount, wallet, version của terms | Chain (queue và share) | (chain, queue address, request ID) | Transaction bị revert hiển thị kèm lý do; alert khi pending quá lâu; cross-check với Onyx API | Approval → requested → processing → position |
| Eligible event (chỉ basis đã duyệt) | Helm → source của PillarsHub | Node của Member, amount, business time, receipt time, settlement state, rule version | Business event của Helm; source trong PillarsHub | Source externalId = chain:tx:log | Lookup theo externalId khi conflict hoặc timeout; reversal post một adjustment có liên kết | Builder thấy Commission ở trạng thái pending |
| Commission payout | PillarsHub → merchant endpoint của Helm → treasury → chain | Batch ID, payment ID, node, bonus, amount, currency, period | PillarsHub (obligation); chain (payment) | Batch ID cộng payment ID; transaction hash | Batch ID giữ nguyên khi retry; Helm không bao giờ trả một payment ID hai lần; transfer chưa confirmed giữ ở Pending; lỗi được báo theo từng payment | Pending → held → payable → paid, kèm link transaction |
| Game sang Points | Game service → Helm | Event ID, member ID, Points, rule ID | Points service | Event ID | Signed event; replay protection; daily limit | Points balance và lịch sử |
| Redemption | App → Onyx; indexer → Helm | Request ID, share, địa chỉ đích | Chain | (chain, queue address, request ID) | Alert awaiting liquidity; cho cancel sau thời gian tối thiểu | Requested → awaiting liquidity → paid |
| Support | App → Chatwoot; agent → Helm admin | Member ID, identity hash, status không nhạy cảm | Chatwoot (conversation); Helm (action) | Conversation ID | Reset widget khi logout; log các Chatwoot webhook có chữ ký | Chat thread |

**Khi provider không khả dụng:** nếu PillarsHub down, signup vẫn chạy với Referral ở trạng thái pending và sync sau. Nếu indexer bị chậm, balance hiển thị "đang cập nhật". Nếu Onyx API không khả dụng, Helm đọc trực tiếp từ chain. Nếu game service down, tính năng chơi bị tắt và không mất Points.

# Genealogy, Commission và mức sẵn sàng cho Phase 1

## Data model tối thiểu

| Table | Field chính | Mục đích |
|---|---|---|
| member | helm_member_id, handle (tùy chọn, do Terrel đề xuất), lifecycle_state (prospect, preregistered, verified, enrolled), is_builder, builder_enrolled_at, country, created_at | Identity ổn định; phân biệt Customer và Builder (ID-01, ID-04) |
| provider_identity | helm_member_id, provider (privy, pillarshub, chatwoot, game), external_id, linked_at | Mapping tường minh |
| wallet | helm_member_id, chain_id, address, source (embedded), first_seen_at, screening_status, allowlist_status | Một wallet cho vault và payout cho mỗi Member |
| agreement_acceptance | helm_member_id, agreement (member terms, Builder terms, vault terms, privacy), version, accepted_at | Consent có version (REC-01) |
| referral_request | id, helm_member_id, referrer_member_id, invite_code, channel, captured_at, status, rejection_reason | Referral đang pending và bị từ chối; referrer gốc (GEN-04) |
| sponsor_edge | id, member_id, sponsor_member_id (enroller), placement_upline_id, effective_at, accepted_at, provenance (signup, import, correction), policy_version, pillarshub_sync_status, superseded_by | Toàn bộ graph ở mọi độ sâu; sponsor và placement được lưu riêng (GEN-01) |
| edge_correction | id, edge_id, old values, new values, reason, requested_by, approved_by, approved_at, consent_ref | Thay đổi có audit (ADM-02) |
| business_event | id, type, member_id, amount, currency, business_time, receipt_time, settlement_state, product, country, attribution, reverses_event_id, rule_version, source_ref, idempotency_key | Event contract tối thiểu theo Terrel |
| commission_statement | helm_member_id, period, bonus lines with PillarsHub IDs, state (calculated, pending, held, payable, paid), payout_ref | Statement của Builder (COMP-03, AUD-03) |
| payout | batch_id, payment_id, helm_member_id, amount, currency, status (received, approved, proposed, signed, confirmed, failed), safe_tx_hash, chain_tx_hash, reported_at | Theo dõi payout (PAY-02) |
| import_run | run_id, source, counts, exceptions, approved_by, rolled_back | Bằng chứng cho alpha import (IMP-02) |
| integration_outbox | id, target, payload hash, attempts, status, last_error | Sync tin cậy |

Chỉ thu thập dữ liệu có mục đích rõ ràng. Không ghi dữ liệu Sponsor hay Member lên chain.

## Rules

- **Customer và Builder:** mọi Member bắt đầu là Customer; Builder enrollment là một bước tường minh, có version, kèm Builder terms. Người ở trạng thái preregistered vẫn giữ attribution nhưng không được nhận earning (ID-04).
- **Self-referral:** bị từ chối ngay lúc capture (cùng member, cùng wallet, cùng email hoặc số điện thoại đã verify).
- **Sponsor không hợp lệ hoặc bị thiếu:** gắn vào root account của công ty với provenance "no sponsor" và flag để review (quyết định D8).
- **Cycle và trùng lặp:** không thể xảy ra với Member mới; được check ở mỗi lần correction và import (GEN-02).
- **Đổi Sponsor và placement:** không bao giờ cho self-service trong Pilot. Admin được ủy quyền thực hiện trong PillarsHub Portal, với lý do và consent reference được ghi vào một case trong Helm. Helm phát hiện mọi thay đổi qua webhook `Node/Updated` và reconciliation hằng đêm, và mở case cho bất kỳ thay đổi nào không có request đã duyệt. Chưa verify được bản thân Portal có bắt buộc người duyệt thứ hai và lưu audit log hay không; nếu không, approval được ghi trong Helm trước khi sửa trên Portal (ADM-02). Placement window có quản lý (preview, consent, deadline, notification; GEN-04 đến GEN-06) chỉ được bật sau khi policy được duyệt (quyết định D10). Customer movement giữ ở trạng thái tắt trong tree của PillarsHub để hai hệ thống không bị lệch nhau.
- **Merge account:** là quy trình admin; giữ edge được accept sớm nhất; trỏ lại các child edge kèm audit entry; retire identity bị trùng (ADM-04).
- **Import alpha community:** import Sponsor trước rồi mới đến cấp dưới, giữ ngày signup gốc và provenance "import"; không có bulk API nên phải import từng record. Verified. Reconcile số lượng và edge, giải quyết hoặc duyệt mọi exception, và diễn tập rollback trước khi cutover (GEN-03, IMP-02).

## Chứng minh tính đúng đắn

- **Full export:** phân trang qua mọi node của tree với một as-of date, không dùng endpoint downline vì endpoint này bị giới hạn ở 10 tầng. Verified.
- **Nightly reconciliation:** so sánh các edge đã accept của Helm với node trong PillarsHub (số lượng, khớp upline theo từng edge, checksum). Mọi sai lệch đều là exception.
- **Test trên staging trước khi launch:** một tree synthetic sâu ít nhất 15 tầng; dry run alpha import (T01); các scenario T02, T03, T05, T06, T07 và T11 của Terrel với kết quả kỳ vọng do Finance chuẩn bị.
- **Lịch sử:** PillarsHub nhận as-of date và lưu placement theo ngày, còn Helm lưu effective timestamp, nên vẫn hiển thị được tree tại ngày phát sinh earning gốc sau một lần correction về sau (bằng chứng cho GEN-01).

## Commission và payout đơn giản

- **Plan.** Dùng Unilevel plan ba tầng đã kết nối sẵn trên staging của PillarsHub (Correspondence). PillarsHub cấu hình các rate đã duyệt; plan ở chế độ read-only qua API, nên Helm không thể thay đổi phần kinh tế. Verified.
- **Eligible event.** Helm chỉ post event type đã được duyệt (quyết định D2) vào một source group riêng, sau khi confirmed on-chain, với external ID `chain:tx:log`. PillarsHub tính toán real-time, nên không post gì cho đến khi basis được duyệt. Verified.
- **Reversal.** Nếu rule đã duyệt có điều chỉnh Commission khi Redemption hoặc khi event lỗi, Helm xóa source hoặc post một adjustment có liên kết trước khi release; sau payout thì áp dụng recovery rule đã thống nhất (T05).
- **Hold và release.** Builder chưa có payee status bắt buộc hoặc có screening hit sẽ bị hold. Finance đóng period, review và release bonus trên PillarsHub.
- **Thực thi.** PillarsHub gửi batch tới merchant endpoint của Helm kèm callback token, và Helm validate token này với PillarsHub. Helm propose USDC transfer tới Helm wallet của từng Builder trong treasury Safe; các Finance signer duyệt; Helm báo lại status của từng payment. Verified (batch interface).
- **Reconciliation.** Hằng ngày: eligible event → source trong PillarsHub → bonus đã release → payment trong batch → transfer on-chain → statement (COMP-04).

# Backlog, phụ thuộc và lịch trình

## Backlog theo thứ tự ưu tiên

| Mức ưu tiên | Work item | Phụ thuộc vào |
|---|---|---|
| **Bắt đầu ngay** | App shell; Privy login và embedded wallet; member DB với các trạng thái Customer và Builder; capture và validate Referral; sync PillarsHub trên staging có read-back; alpha import tool trên dữ liệu mẫu; event pipeline và source posting (chỉ trên staging); payout merchant endpoint và Safe proposal trên testnet; chain indexer; deposit và redemption qua Onyx trên Sepolia; Chatwoot widget; admin skeleton có role; screening hook; CI, các môi trường, secret | Quyền truy cập test của provider; dữ liệu mẫu của alpha |
| **Thin slice (tuần 1–3)** | Demo end-to-end trên test network: signup → Referral → deposit → Commission thử → payout batch thử → Redemption; một flow game sang Points | Tài liệu game API |
| **Trước khi nhận tiền thật và chi trả payout** | Vault terms và disclosure; tự động hóa allowlist; phần thiết yếu cho Builder và bước chuyển sang PillarsHub qua SSO; Builder enrollment và terms; approval, hold và reporting cho payout; diễn tập và reconciliation cho alpha import; support agent view, FAQ và runbook; reconciliation job và alert; eligibility theo quốc gia; môi trường production; load test và recovery test; fix các finding từ security review; diễn tập vận hành | Strategy, MLA, ownership, Commission basis, câu trả lời từ legal |
| **Có thể hoãn (bị tắt)** | Placement window có quản lý; rank và qualification; campaign; top-up tích hợp; thêm chain và asset; Telegram và WhatsApp; transaction monitoring thương mại; native mobile | Nhu cầu của Business và rule đã được duyệt |

## Critical path

1. Các quyết định D1–D13 trong buổi họp.
2. **Vault sẵn sàng:** strategy và Manager → cấu hình vault (asset, async queue, external allowlist, share không chuyển nhượng được, fee) → ký MLA → deploy production → bàn giao ownership cho multisig của Business.
3. **Commission basis và proof cho plan:** eligible event, rate, period và hold được duyệt → cấu hình PillarsHub → khớp với kết quả kỳ vọng của Finance (T02).
4. **Dữ liệu alpha:** nhận record → dry run → reconciliation → exception được duyệt → diễn tập cutover (T01).
5. **Câu trả lời từ legal:** pháp nhân, các quốc gia launch, KYC tier, vault terms, mô hình chi trả Referral.
6. **Security review** phần integration của Helm, payout executor và cấu hình vault.
7. **Diễn tập vận hành:** valuation, execute queue, thanh khoản cho Redemption và một payout batch nhỏ.
8. Launch slot production của PillarsHub (thứ Ba đến thứ Năm).

Phần engineering chạy song song với mục 2–5; ngày launch phụ thuộc vào hạng mục nào xong sau cùng.

# Sẵn sàng launch và vận hành

## Gate để nhận tiền thật và chi trả Commission

Tất cả điều kiện phải đạt; không bỏ qua điều kiện nào chỉ để kịp deadline.

1. Vault strategy, Manager, fee và Member terms được Business và luật sư duyệt.
2. MLA đã ký; Enzyme xác nhận version đã deploy và audit coverage; upgrade governance có văn bản.
3. Multisig của Vault Owner đã sẵn sàng; Admin key và list-owner key nằm trong managed custody; backend của Helm không giữ Owner key hay Admin key nào.
4. Deposit và Redemption đã được chứng minh trên production với một khoản tiền nhỏ do operator cấp.
5. Reconciliation hằng ngày pass; monitoring và alert đã chạy; có đầu mối incident ở từng provider.
6. Screening và eligibility đã chạy cho tier được luật sư duyệt.
7. Security review hoàn tất và các finding mức high đã được fix.
8. Các provider (Privy, Enzyme, PillarsHub) chấp nhận mô hình kinh doanh bằng văn bản.
9. Có support agent view, FAQ, runbook và quy trình escalation, gồm cả cách xử lý user bị flag và dispute về earning (SUP-01 đến SUP-06).
10. Alpha import đã reconcile, exception đã được giải quyết hoặc duyệt, rollback đã được diễn tập (GEN-03, IMP-02).
11. **Trước payout đầu tiên:** Commission basis, rate, period và hold được Owen, Finance và luật sư duyệt; ví dụ về plan do Finance chuẩn bị khớp với kết quả của PillarsHub (T02); các scenario trùng lặp, replay và reversal đều pass (T03, T05); một batch thử có timeout cưỡng bức chỉ tạo ra một payment (T06); treasury Safe với các Finance signer đã sẵn sàng; payee status đã được thu thập (PAY-04).
12. Load envelope và recovery target đã được thống nhất và test (OPS-01 đến OPS-03); quyền export toàn bộ dữ liệu được ghi trong hợp đồng với PillarsHub và Enzyme (API-03).

## Security boundary

- **Audit coverage.** ChainSecurity đã audit Onyx core (tháng 12/2025), cross-chain wallet (tháng 5/2026) và Chainlink compliance integration (tháng 7/2026). Một deployment helper thêm vào sau lần audit cuối không nằm trong audit scope nào tìm được. Verified. Enzyme phải xác nhận vault của Helm dùng những component nào và chúng đã được audit.
- **Rủi ro upgrade.** Global owner của Enzyme có thể upgrade toàn bộ vault contract; báo cáo audit mô tả role này có thể "fully drain the system", và không thấy timelock nào. Verified. MLA phải quy định về thông báo trước và governance.
- **Gas sponsorship.** Gas sponsorship native của Privy upgrade wallet của Member bằng EIP-7702; delegation contract thuộc phạm vi security review. Verified.
- **Webhook PillarsHub không có chữ ký.** Chỉ coi là tín hiệu và fetch lại qua API. Verified.
- **PillarsHub SSO.** Backend của Helm mint một PillarsHub user token và mở back office với token nằm trong URL query string. Verified. Token trong URL có thể bị lộ qua browser history và log; cần xác nhận với PillarsHub về thời hạn token và việc chỉ dùng một lần, và mở back office trong tab mới, không gửi referrer header.
- **Payout callback.** PillarsHub xác thực payout batch bằng một callback token, và Helm validate token này với token endpoint của PillarsHub trước khi xử lý. Verified. Payout executor không giữ signing key nào; nó chỉ propose Safe transaction.
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
| Basis chi trả Referral | Việc chi trả Commission trên eligible event đã chọn có hợp pháp tại các quốc gia launch không? | Owen + Finance + luật sư | Event pipe cấu hình được; không post gì cho đến khi được duyệt | Plan của PillarsHub (verified) | **Blocker cho payout** |
| Payee status và báo cáo thuế | Cần thông tin payee nào trước khi payout? | Finance + luật sư | Gate theo payee status; quy trình hold (PAY-04) | Không có sẵn | Trước khi payout |
| Earnings disclosure | Cần những disclosure nào về earning và thu nhập? | Business + luật sư | Statement và màn hình disclosure (AUD-03) | — | Trước khi payout |
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
| Commission đơn giản | Unilevel ba tầng trên một eligible event đã được duyệt; các batch USDC do Finance duyệt, chi từ treasury Safe | Plan, source và custom merchant batch của PillarsHub (verified) | Basis, rate, period và hold được duyệt; luật sư | Owen + Finance + luật sư | **Blocker cho payout** |
| Alpha import | Import trước khi launch, giữ lịch sử; reconcile và diễn tập | Tạo customer với ID, ngày và enroller; không có bulk API (verified) | Record của alpha | Business + Tech | Cao |
| Placement window | Tắt trong Pilot; bật sau khi policy được duyệt | GEN-04 đến GEN-06 | Placement policy | Terrel + Tim | Trung bình |
| Customer và Builder | Trạng thái riêng; Builder enrollment tường minh | ID-01, ID-04 | Builder terms | Terrel + Owen | Trung bình |
| Funding path | Crypto trực tiếp; không dùng top-up provider | Paymenture không công bố asset, quốc gia hay fee và cấm "pyramid schemes" (verified) | Yêu cầu của Business | Business | Thấp |
| Points | Không có giá trị tiền mặt; không gắn với số tiền deposit | Chưa nhận được tài liệu game | Tài liệu game API; luật sư review | Business + Cyclone | Trung bình |
| Identity check | Build gate ngay từ bây giờ; tier do luật sư quyết định; screening địa chỉ từ ngày đầu | Stack hiện không có KYC (verified) | Quyết định của luật sư | Business + luật sư | Cao |

**Điều gì sẽ thay đổi các phương án mặc định này:** nếu cần top-up tích hợp ngay khi launch thì phải thêm một payment provider vào critical path; nếu cần rank, matching bonus hoặc placement window ngay khi launch thì phải thêm cấu hình plan, proof scenario và năng lực vận hành; nếu luật sư yêu cầu KYC đầy đủ thì cần thêm một identity vendor và một gate trước khi truy cập vault và payout.

# Phụ lục A: Bằng chứng {.unnumbered}

Tất cả link được đọc vào ngày 8/10/2026.

**PillarsHub:** [API authentication](https://pillars-hub.readme.io/reference/authenticating) · [Access token](https://pillars-hub.readme.io/reference/access-control-tokens) · [Swagger UI](https://api.pillarshub.com/swagger/index.html) · [Customer API spec](https://api.pillarshub.com/swagger/CustomerV1/swagger.json) · [Commission API spec](https://api.pillarshub.com/swagger/CommissionV1/swagger.json) · [Webhook](https://pillars-hub.readme.io/reference/getting-started-webhooks) · [Webhook topic](https://pillars-hub.readme.io/reference/topics) · [Invoice date và real-time commission](https://pillars-hub.readme.io/docs/invoice-dates-are-used-to-calculate-commissions) · [Launch timing protocol](https://pillars-hub.readme.io/docs/pillars-launch-timing-protocol) · [Money-out integration](https://pillars-hub.readme.io/docs/money-out-merchant-integration-guide) · [Terms](https://www.pillarshub.com/terms)

**Privy:** [Bảng giá](https://www.privy.io/pricing) · [Security FAQ](https://docs.privy.io/security/security-faqs) · [Hỗ trợ user](https://docs.privy.io/user-management/users/managing-users/supporting-your-users) · [Webhook](https://docs.privy.io/api-reference/webhooks/overview) · [React quickstart](https://docs.privy.io/basics/react/quickstart) · [Acceptable use policy](https://www.privy.io/acceptable-use-policy)

**Enzyme Onyx:** [Sản phẩm và bảng giá](https://enzyme.finance/products/onyx) · [Kiến trúc](https://docs.enzyme.finance/onyx-user-documentation/getting-started/quickstart/architecture) · [Deposit control và allowlist](https://docs.enzyme.finance/onyx-user-documentation/enzyme-vault/subscription/control) · [Redemption](https://docs.enzyme.finance/onyx-user-documentation/enzyme-vault/subscription/redemptions) · [User role](https://docs.enzyme.finance/onyx-protocol/user-roles) · [Deploy và upgrade](https://docs.enzyme.finance/onyx-protocol/architecture/deployments-and-upgrades) · [Rủi ro và hạn chế](https://docs.enzyme.finance/onyx-protocol/security/risks-and-limitations) · [SDK](https://docs.enzyme.finance/onyx-sdk) · [Public API](https://api.onyx.enzyme.finance/reference) · [Contract](https://github.com/enzymefinance/protocol-onyx) · [Báo cáo audit](https://github.com/enzymefinance/protocol-onyx/tree/main/audits)

**Chatwoot:** [Tài liệu developer](https://developers.chatwoot.com/introduction) · [Bảng giá](https://www.chatwoot.com/pricing)

**Funding và compliance:** [Paymenture](https://paymenture.com/) · [Bridge developer agreement](https://www.bridge.xyz/legal/developer-agreement) · [Chainalysis sanctions oracle](https://go.chainalysis.com/chainalysis-oracle-docs.html) · [Hướng dẫn năm 2021 của FATF](https://www.fatf-gafi.org/en/publications/Fatfrecommendations/Guidance-rba-virtual-assets-2021.html)

Ghi chú chi tiết kèm mọi nguồn và trích dẫn nằm trong `work/notes/01-pillarshub.md`, `02-enzyme-onyx.md`, `03-privy.md` và `04-chatwoot-funding-compliance.md`.

# Phụ lục B: Giả định và gap {.unnumbered}

- **Requirement v0.2 của Terrel đã được truy vết ở mục 9.** Vẫn còn thiếu trong danh sách "Waiting for" của tài liệu này: compensation specification kèm ví dụ cụ thể, record enrollment và Genealogy của alpha, và release scope một trang (đối tượng, quốc gia, ngôn ngữ, hoạt động). Các owner trong bản draft của Terrel (Tim, Darren, JT, Finance, compliance) chỉ là đề xuất và không được nhắc lại ở đây như cam kết.
- **Commission basis:** chưa được duyệt. Thiết kế hỗ trợ bất kỳ eligible event type đơn lẻ nào; không post gì cho đến khi Owen, Finance và luật sư duyệt.
- **Game và Points:** chưa nhận được tài liệu API. Cần có: cách link account, event schema và cách ký, chống trùng lặp và replay, abuse control, Points rules engine, Points có được quy đổi ra thứ gì hay không.
- **Chưa verify với provider:** auto-placement, giới hạn độ sâu, cách correction Sponsor, mức chi tiết của token permission, rate limit, ý nghĩa của mã 409, bảng giá và chứng nhận bảo mật của PillarsHub; volume limit ở gói trả phí và việc chấp nhận mô hình kinh doanh của Privy; lead time, version đã deploy, ownership của external allowlist và điều khoản thương mại của Enzyme; cơ chế retry webhook của Chatwoot.
- **Bảng giá:** giá công khai của Enzyme khác với giá trong correspondence; bảng giá của PillarsHub không công khai.
- **Năng lực team, ngân sách và launch cohort** chưa được cung cấp; các khoảng thời gian trong lịch trình giả định khoảng năm đến sáu engineer.
- **Kỳ vọng về placement window** từ cuộc gọi field của Nic chưa phải là policy đã công bố; window giữ ở trạng thái tắt cho đến khi có policy.

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
10. Custom money-out merchant: batch có mang được custom currency code như USDC không; cơ chế retry khi Helm báo Pending; Failure được re-release thế nào; giới hạn cho mỗi payment?
11. Unilevel plan ba tầng trên staging của Helm có cấu hình được với rate, period, hold và mức tối thiểu của Finance không, và ai là người thay đổi (plan ở chế độ read-only qua API)?
12. Customer type hoặc status để phân biệt Customer với Builder, và cho người ở trạng thái preregistered không được nhận earning.
13. Portal có hỗ trợ approval theo role (người duyệt thứ hai) và audit log cho việc đổi Sponsor và placement, sửa bonus và release không?
14. SSO user token: thời hạn, chỉ dùng một lần, và có cách exchange qua POST hoặc token ngắn hạn thay vì đặt token trong URL không? Có giới hạn được visibility của back office để Builder không bao giờ thấy nhánh khác hay balance không, và back office hoạt động thế nào trên mobile?

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
