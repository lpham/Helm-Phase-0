"""Render the solution document's diagrams to outputs/figures/*.svg.

Each figure here mirrors a ```{.mermaid #fig-...}``` block in the Markdown
source; tools/mermaid-figures.lua swaps the block for this SVG in the PDF.
Keep the two in step when editing either.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import svglib  # noqa: E402
from svglib import render, sequence  # noqa: E402
from diagrams_vi import VI  # noqa: E402

def build():
    LEGEND = [("member", "Member / business step"), ("buy", "Confirmed provider"),
              ("build", "Cyclone-built"), ("chain", "On-chain")]

    # ------------------------------------------------------------ Figure 1: capabilities
    caps = [("Join with referral", "invite, Sponsor"), ("Wallet", "log in, own keys"),
            ("Fund wallet", "USDC, one network"), ("Vault", "deposit, redeem"),
            ("Games and Points", "no cash value"), ("Support", "in-app chat")]
    provs = [("PillarsHub", "genealogy, plan", "buy"), ("Privy", "login, wallets", "buy"),
             ("Blockchain", "USDC transfer", "chain"), ("Enzyme Onyx", "shares, queues", "buy"),
             ("Cyclone game", "Points service", "build"), ("Chatwoot", "conversations", "buy")]
    boxes, arrows = [], []
    for i, ((c1, c2), (p1, p2, pk)) in enumerate(zip(caps, provs)):
        x = 20 + i * 132
        boxes.append((f"c{i}", x, 30, 120, 48, f"{c1}\n{c2}", "member"))
        boxes.append((f"p{i}", x, 120, 120, 48, f"{p1}\n{p2}", pk))
        arrows.append((f"c{i}.b", f"p{i}.t", None, "data"))
        arrows.append((f"p{i}.b", "helm.t", None, "data"))
    boxes.append(("helm", 20, 215, 780, 50,
                  "Helm Web App and backend (Cyclone)\nmember record · referral sync · chain indexer · reconciliation · admin and exceptions", "build"))
    render("fig-capabilities", 820, 320, boxes, arrows, LEGEND, lines=False)

    # ------------------------------------------------------------ Figure 2: journey
    steps = [("Invite link", "member"), ("Sign up, log in", "member"), ("Wallet created", "buy"),
             ("Fund wallet\nUSDC", "chain"), ("Read vault terms", "member"),
             ("Deposit request", "chain"), ("Position confirmed", "chain"),
             ("Play, earn Points", "build"), ("Request Redemption", "chain")]
    boxes, arrows = [], []
    for i, (label, kind) in enumerate(steps[:5]):
        boxes.append((f"s{i}", 20 + i * 160, 30, 140, 46, label, kind))
        if i:
            arrows.append((f"s{i-1}.r", f"s{i}.l", None, "data"))
    for j, (label, kind) in enumerate(steps[5:]):
        i = 5 + j
        boxes.append((f"s{i}", 660 - j * 160, 130, 140, 46, label, kind))
    arrows.append(("s4.b", "s5.t", None, "money"))
    for i in range(6, 9):
        arrows.append((f"s{i-1}.l", f"s{i}.r", None, "data"))
    render("fig-journey", 820, 230, boxes, arrows, LEGEND, lines=False)

    # ------------------------------------------------------------ Figure 3: architecture
    render("fig-architecture", 820, 450, [
        ("g_b", 10, 10, 800, 70, "Browser", "group"),
        ("app", 30, 32, 760, 38, "Helm Web App · Privy SDK (Member signs) · Chatwoot widget", "build"),
        ("g_h", 10, 100, 800, 150, "Helm backend (Cyclone)", "group"),
        ("api", 30, 125, 180, 46, "API and auth\nverifies Privy tokens", "build"),
        ("db", 225, 125, 180, 46, "Member DB and ledger\nreferrals · events · audit", "build"),
        ("int", 420, 125, 180, 46, "Integration workers\noutbox · retries", "build"),
        ("idx", 615, 125, 175, 46, "Chain indexer\nconfirmations", "build"),
        ("rec", 30, 190, 375, 46, "Reconciliation and alerts\nchain · Onyx API · PillarsHub · Points", "build"),
        ("adm", 420, 190, 370, 46, "Admin console\nexceptions · screening cases · Sponsor corrections", "build"),
        ("privy", 20, 285, 120, 50, "Privy\nlogin, wallets", "buy"),
        ("ph", 150, 285, 120, 50, "PillarsHub\ngenealogy", "buy"),
        ("game", 280, 285, 120, 50, "Game and Points\nCyclone service", "build"),
        ("scr", 410, 285, 120, 50, "Sanctions API\naddress screening", "buy"),
        ("cw", 540, 285, 120, 50, "Chatwoot Cloud\nsupport", "buy"),
        ("onyxapi", 670, 285, 130, 50, "Onyx public API\nread-only", "buy"),
        ("chain", 20, 360, 780, 40, "Arbitrum: USDC · Onyx deposit and redeem queues · shares · valuation", "chain"),
    ], [
        ("app.b", "api.t", "Privy token", "data"),
    ], LEGEND, lines=False)

    # ------------------------------------------------------------ Figures 4-9: sequences
    sequence("fig-flow-signup", [
        ("m", "Member app", "member"), ("p", "Privy", "buy"),
        ("h", "Helm backend", "build"), ("x", "PillarsHub", "buy")], [
        ("m", "m", "store invite code", "data"),
        ("m", "p", "log in", "ctrl"),
        ("p", "m", "access token, embedded wallet", "data"),
        ("m", "h", "register(token, invite code)", "data"),
        ("h", "p", "verify token, read wallet address", "data"),
        ("h", "h", "member + pending Referral Request; screen address", "ctrl"),
        ("h", "x", "find customer by Helm ID", "data"),
        ("h", "x", "create customer (id, externalIds, enrollerId)", "data"),
        ("h", "x", "read node and upline", "data"),
        ("h", "h", "Sponsor Edge accepted", "ctrl"),
        ("h", "m", "referral confirmed", "data"),
    ])

    sequence("fig-flow-funding", [
        ("e", "Exchange or wallet", "member"), ("c", "Arbitrum", "chain"),
        ("i", "Helm indexer", "build"), ("h", "Helm backend", "build"), ("m", "Member app", "member")], [
        ("e", "c", "USDC transfer to Member address", "money"),
        ("i", "c", "Transfer event seen (submitted)", "data"),
        ("i", "i", "wait N confirmations", "ctrl"),
        ("i", "h", "funding confirmed (chain, tx, log)", "data"),
        ("h", "h", "screen source address, record event", "ctrl"),
        ("h", "m", "balance updated", "data"),
    ])

    sequence("fig-flow-deposit", [
        ("m", "Member app", "member"), ("h", "Helm backend", "build"),
        ("c", "Onyx contracts", "chain"), ("o", "Vault operator", "member")], [
        ("m", "h", "accept vault terms (version)", "data"),
        ("h", "c", "add wallet to allowlist", "ctrl"),
        ("m", "c", "approve exact amount", "money"),
        ("m", "c", "requestDeposit", "money"),
        ("c", "h", "DepositRequest(requestId) via indexer", "data"),
        ("o", "c", "update valuation; execute deposit requests", "ctrl"),
        ("c", "h", "DepositRequestExecuted(requestId, shares)", "data"),
        ("h", "h", "position confirmed; business event", "ctrl"),
        ("h", "m", "position and valuation date", "data"),
    ])

    sequence("fig-flow-game", [
        ("m", "Member app", "member"), ("g", "Game and points service", "build"),
        ("h", "Helm backend", "build")], [
        ("m", "g", "play (linked Helm member)", "data"),
        ("g", "g", "validate result, apply limits", "ctrl"),
        ("g", "h", "signed event (event id, member, Points)", "data"),
        ("h", "h", "verify signature; dedupe on event id", "ctrl"),
        ("h", "m", "Points balance (from service)", "data"),
    ])

    sequence("fig-flow-redemption", [
        ("m", "Member app", "member"), ("h", "Helm backend", "build"),
        ("c", "Onyx contracts", "chain"), ("o", "Vault operator", "member")], [
        ("m", "h", "screen destination (own wallet)", "ctrl"),
        ("m", "c", "requestRedeem(shares)", "money"),
        ("c", "h", "RedeemRequest(requestId) via indexer", "data"),
        ("o", "c", "update valuation; ensure liquidity", "ctrl"),
        ("o", "c", "execute redeem requests", "ctrl"),
        ("c", "h", "RedeemRequestExecuted(requestId, assets)", "data"),
        ("h", "h", "position reduced; business event", "ctrl"),
        ("h", "m", "USDC in wallet; stages complete", "money"),
    ])

    sequence("fig-flow-support", [
        ("m", "Member app", "member"), ("h", "Helm backend", "build"),
        ("w", "Chatwoot", "buy"), ("a", "Agent", "member"), ("d", "Helm admin", "build")], [
        ("m", "h", "request chat identity", "data"),
        ("h", "m", "member ID + identity hash", "data"),
        ("m", "w", "open verified conversation", "data"),
        ("w", "a", "conversation with member ID", "data"),
        ("a", "d", "look up status (read-only)", "data"),
        ("d", "d", "ops resolves exception (approval, audit)", "ctrl"),
        ("a", "w", "reply to Member", "data"),
    ])



def main():
    base = svglib.BASE
    for lang, out in (("en", base), ("vi", base / "vi")):
        out.mkdir(parents=True, exist_ok=True)
        svglib.LANG, svglib.VI, svglib.OUT = lang, VI, out
        build()
    print("figures written (en, vi)")


if __name__ == "__main__":
    main()
