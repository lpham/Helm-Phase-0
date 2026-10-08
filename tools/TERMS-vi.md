# Quy tắc cho bản tiếng Việt (Helm Phase 0)

Đối tượng đọc: team Business và Tech của một công ty IT. Viết như một tài liệu nội bộ chuyên nghiệp: văn xuôi tiếng Việt tự nhiên, **giữ nguyên thuật ngữ tiếng Anh** mà dân IT/crypto dùng hằng ngày. Không dịch 1:1, không cố Việt hóa thuật ngữ.

## Giữ nguyên tiếng Anh (không dịch, không kèm chú thích)

- Thuật ngữ domain theo `GLOSSARY.md`: Member, Sponsor, Sponsor Edge, Genealogy, Referral, Referral Request, Wallet Funding, Vault Deposit, Redemption, Vault Position, Commission, Points, Yield Product.
- Sản phẩm và vai trò: wallet, embedded wallet, vault, share, position, allowlist, deposit queue, redeem queue, NAV, valuation, Owner, Admin, Manager, operator, multisig, signer, key, key export, custody, self-custodial, custodial, gas sponsorship.
- Kỹ thuật: frontend, backend, API, SDK, endpoint, webhook, polling, indexer, ledger, outbox, retry, backoff, dead letter, idempotent, deduplication key, reconciliation, event, payload, token, access token, rate limit, staging, production, sandbox, testnet, mainnet, deploy, upgrade, timelock, audit, security review, monitoring, alert, runbook, incident, dashboard, admin console, data model, schema, source of truth, read-back, sync.
- Quy trình: onboarding, signup, login, MVP, thin slice, backlog, critical path, launch, launch gate, go-live, controlled launch, cohort, scope, out of scope, blocker, TBD, owner (người phụ trách), stakeholder, KYC, AML, KYT, sanctions screening, Travel Rule, compliance, legal review, MLA, SLA.
- Tên endpoint, field, event, function, mã quyết định (D1–D8), mã requirement (FR-1…), ID diagram, tên provider và sản phẩm.

## Viết bằng tiếng Việt

- Câu văn, động từ, liên từ, giải thích, tiêu đề mục (có thể lẫn thuật ngữ tiếng Anh, ví dụ "Data flow end-to-end", "Phạm vi Phase 0").
- Từ phổ thông không phải thuật ngữ: "quyết định", "rủi ro", "chi phí", "giả định", "phụ thuộc", "trách nhiệm", "ước tính", "điều kiện".

## Nhãn bằng chứng

Giữ nguyên: **Verified**, **Correspondence**, **Recommended**, **TBD**.

## Định dạng

- Ngày tháng dạng Việt ("ngày 9/10/2026" hoặc "9 tháng 10 năm 2026"); số tiền giữ định dạng gốc ("$2,000", "$1M").
- Giữ nguyên cấu trúc Markdown, bảng, link, thuộc tính `{.unnumbered}`, khối Mermaid (`{.mermaid #fig-... caption="..."}`); caption viết tiếng Việt, nhãn Mermaid theo cùng quy tắc trên.
- Tiêu đề phần: "Phần I: Business và khách hàng", "Phần II: Triển khai kỹ thuật" (template dựa vào chữ "Phần "). "Appendix" → "Phụ lục".
- Không dùng "bạn". Văn phong ngắn gọn, trực tiếp.
