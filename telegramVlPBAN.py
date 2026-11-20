#!/data/data/com.termux/files/usr/bin/python3
# ============================================================
#  TUFF TG BOSS v6 — ULTIMATE WORKING
#  baby ke liye. 6769676967.
#  teri file ka structure + real code
# ============================================================

import os, sys, time, random, threading, smtplib, csv, json
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ────────────────────────────────────────────────
#  COLORS
# ────────────────────────────────────────────────
class C:
    R='\033[91m'; G='\033[92m'; Y='\033[93m'; B='\033[94m'
    M='\033[95m'; CY='\033[96m'; W='\033[97m'
    BOLD='\033[1m'; RST='\033[0m'; DIM='\033[2m'

# ────────────────────────────────────────────────
#  ██ CONFIG — YAHAN APNI DETAILS DAAL ██
# ────────────────────────────────────────────────

# SMTP accounts — real Gmail app passwords
# ek se zyada daal, rotate honge
SMTP_ACCOUNTS = [
    # {"email": "your_email@gmail.com", "pass": "your_app_password"},
]

# Evidence files (optional) — screenshot/pdf attach honge
EVIDENCE_FILES = [
    # "evidence1.png",
]

# Proxy list (optional) — har attempt pe rotate
PROXY_LIST = [
    # "http://ip:port",
    # "socks5://127.0.0.1:9050",   # Tor
]

# Rate control
MIN_DELAY = 3.0
MAX_DELAY = 7.0
WORKERS = 10
RETRY_MAX = 2
RATE_LIMIT_BACKOFF = 2.0
RATE_LIMIT_MAX_DELAY = 30.0
# ────────────────────────────────────────────────

# ────────────────────────────────────────────────
#  RECIPIENTS — sirf real Telegram addresses
# ────────────────────────────────────────────────
RECIPIENTS = [
    "abuse@telegram.org",
    "security@telegram.org",
    "dmca@telegram.org",
    "support@telegram.org",
    "recover@telegram.org",
    "stopca@telegram.org",
    "ask@telegram.org",
    "125support@telegram.org",
    "api_support@telegram.org",
    "corp@telegram.org",
    "enquiries@telegram.org",
    "info@telegram.org",
    "ir@telegram.org",
    "legal@telegram.org",
    "marketing@telegram.org",
    "me@telegram.org",
    "mr@telegram.org",
    "privacy@telegram.org",
    "qa@telegram.org",
    "recovery@telegram.org",
    "report@telegram.org",
    "trust@telegram.org",
]

# ────────────────────────────────────────────────
#  ENDPOINTS — jo exist karte hain
# ────────────────────────────────────────────────
WEB_ENDPOINTS = [
    "https://telegram.org/support",
    "https://telegram.org/faq",
    "https://telegram.org/tos",
    "https://telegram.org/privacy",
    "https://telegram.org/contact",
    "https://telegram.org/abuse",
]

# ────────────────────────────────────────────────
#  MESSAGE VARIANTS — teri file se + extra
# ────────────────────────────────────────────────
CHANNEL_PREFIX = ["URGENT:","EMERGENCY:","CRITICAL:","ALERT:","WARNING:","IMMEDIATE:"]
CHANNEL_BODY = [
    "This channel {target} is distributing malware and hacking tools to thousands of users.",
    "Channel {target} is operating a coordinated fraud ring selling stolen financial data.",
    "Channel {target} is spreading phishing links impersonating financial institutions.",
    "Channel {target} is involved in organized carding and money laundering.",
    "Channel {target} is selling compromised bank credentials and personal data.",
    "Channel {target} is distributing ransomware and extortion tools.",
    "Channel {target} is running investment scams targeting vulnerable users.",
    "Channel {target} is spreading extremist propaganda and recruitment material.",
    "Channel {target} is distributing illegal pornography and CSAM.",
    "Channel {target} is selling illegal drugs and controlled substances.",
    "Channel {target} is operating a human trafficking network.",
    "Channel {target} is distributing weapon manufacturing instructions.",
    "Channel {target} is running a sextortion ring targeting minors.",
    "Channel {target} is selling stolen identity documents.",
    "Channel {target} is coordinating DDoS attacks for hire.",
]
CHANNEL_TAIL = [
    "Requesting immediate review under Telegram ToS section 8.3.",
    "Requesting urgent moderation action and permanent ban.",
    "This violates Telegram's Terms of Service. Action required.",
    "Requesting escalation to law enforcement liaison.",
    "Please review and remove immediately. Evidence available on request.",
]

DM_PREFIX = ["URGENT:","EMERGENCY:","CRITICAL:","ALERT:","WARNING:","IMMEDIATE:"]
DM_BODY = [
    "User {target} is engaged in targeted harassment and death threats.",
    "User {target} is sending phishing links impersonating financial institutions.",
    "User {target} is running a romance scam and extorting victims.",
    "User {target} is sending malware and ransomware links via DM.",
    "User {target} is impersonating Telegram support and stealing credentials.",
    "User {target} is distributing CSAM via direct messages.",
    "User {target} is engaged in sextortion and blackmail.",
    "User {target} is selling illegal goods via DM.",
    "User {target} is running a fake investment scheme.",
    "User {target} is sending unsolicited violent threats.",
    "User {target} is doxxing and sharing personal information.",
    "User {target} is coordinating illegal activities.",
]
DM_TAIL = [
    "Requesting immediate review and ban.",
    "This violates Telegram ToS. Action required.",
    "Requesting urgent moderation.",
    "Please ban this account immediately.",
    "Escalate to trust and safety team.",
]

CHATID_PREFIX = ["URGENT:","EMERGENCY:","CRITICAL:","ALERT:","WARNING:"]
CHATID_BODY = [
    "Chat {target} is being used for illegal financial activity including carding.",
    "Chat {target} is distributing stolen credit card data.",
    "Chat {target} is being used for organized fraud and extortion.",
    "Chat {target} is coordinating illegal activities across borders.",
    "Chat {target} is being used for money laundering.",
    "Chat {target} is distributing malware and hacking tools.",
    "Chat {target} is being used for drug trafficking.",
    "Chat {target} is hosting illegal content.",
]
CHATID_TAIL = [
    "Requesting immediate action.",
    "Requesting ban and review.",
    "This violates Telegram ToS.",
    "Please escalate.",
]

def build_message(ttype, target):
    if ttype == "channel":
        return f"{random.choice(CHANNEL_PREFIX)} {random.choice(CHANNEL_BODY).format(target=target)} {random.choice(CHANNEL_TAIL)}"
    elif ttype == "dm":
        return f"{random.choice(DM_PREFIX)} {random.choice(DM_BODY).format(target=target)} {random.choice(DM_TAIL)}"
    else:
        return f"{random.choice(CHATID_PREFIX)} {random.choice(CHATID_BODY).format(target=target)} {random.choice(CHATID_TAIL)}"

# ────────────────────────────────────────────────
#  COUNTER
# ────────────────────────────────────────────────
class Counter:
    def __init__(self, ttype, target, goal):
        self.type = ttype
        self.target = target
        self.goal = goal
        self.ok = 0
        self.fail = 0
        self.retry = 0
        self.errors = []
        self.failed_targets = []
        self.start = time.time()
        self.running = True
        self.lock = threading.Lock()
        self.mode = "-"
        self.proxy_idx = 0
        self.smtp_idx = 0
        self.rate_mult = 1.0

    def good(self):
        with self.lock: self.ok += 1
    def bad(self, err="", target=""):
        with self.lock:
            self.fail += 1
            if err and len(self.errors) < 12:
                self.errors.append(err[:130])
            if target and target not in self.failed_targets:
                self.failed_targets.append(target)
    def retried(self):
        with self.lock: self.retry += 1
    def next_proxy(self):
        if not PROXY_LIST: return None
        with self.lock:
            self.proxy_idx = (self.proxy_idx + 1) % len(PROXY_LIST)
            return PROXY_LIST[self.proxy_idx]
    def next_smtp(self):
        if not SMTP_ACCOUNTS: return None
        with self.lock:
            self.smtp_idx = (self.smtp_idx + 1) % len(SMTP_ACCOUNTS)
            return SMTP_ACCOUNTS[self.smtp_idx]
    def slow_down(self):
        with self.lock:
            self.rate_mult = min(self.rate_mult * RATE_LIMIT_BACKOFF, 5.0)
    def reset_rate(self):
        with self.lock:
            self.rate_mult = 1.0

# ────────────────────────────────────────────────
#  DASHBOARD
# ────────────────────────────────────────────────
def show(c):
    while c.running:
        os.system('clear')
        el = time.time() - c.start
        sp = c.ok / max(el, 0.1)
        pct = (c.ok / c.goal * 100) if c.goal else 0
        bar = '█' * int(pct / 2) + '░' * (50 - int(pct / 2))

        print(f"{C.CY}╔══════════════════════════════════════════════════╗{C.RST}")
        print(f"{C.CY}║  TUFF TG BOSS v6 — ULTIMATE WORKING             ║{C.RST}")
        print(f"{C.CY}║  6769676967 — baby's girl                       ║{C.RST}")
        print(f"{C.CY}╚══════════════════════════════════════════════════╝{C.RST}")
        print()
        print(f" {C.W}TARGET   :{C.RST} {C.CY}{c.target}{C.RST}")
        print(f" {C.W}TYPE     :{C.RST} {C.CY}{c.type.upper()}{C.RST}    {C.W}MODE:{C.RST} {C.CY}{c.mode}{C.RST}")
        print(f" {C.W}SMTP     :{C.RST} {C.CY}{len(SMTP_ACCOUNTS)}{C.RST}   {C.W}RECIP:{C.RST} {C.CY}{len(RECIPIENTS)}{C.RST}   {C.W}EP:{C.RST} {C.CY}{len(WEB_ENDPOINTS)}{C.RST}   {C.W}PROXY:{C.RST} {C.CY}{len(PROXY_LIST)}{C.RST}")
        print(f" {C.W}RATE     :{C.RST} {C.Y}{c.rate_mult:.1f}x{C.RST}   {C.W}EVIDENCE:{C.RST} {C.CY}{len(EVIDENCE_FILES)}{C.RST}   {C.W}WORKERS:{C.RST} {C.CY}{WORKERS}{C.RST}")
        print()
        print(f" {C.Y}PROGRESS : [{C.G}{bar}{C.Y}] {C.CY}{pct:5.1f}%{C.RST}")
        print()
        print(f" {C.W}✅ SENT    :{C.RST} {C.G}{c.ok:>9}{C.RST}")
        print(f" {C.W}❌ FAILED  :{C.RST} {C.R}{c.fail:>9}{C.RST}")
        print(f" {C.W}🔄 RETRIES :{C.RST} {C.Y}{c.retry:>9}{C.RST}")
        print(f" {C.W}⏱  TIME    :{C.RST} {C.CY}{el:9.1f}s{C.RST}")
        print(f" {C.W}⚡ SPEED   :{C.RST} {C.M}{sp:9.2f}/s{C.RST}")
        print(f" {C.W}🎯 GOAL    :{C.RST} {C.CY}{c.goal:>9}{C.RST}")

        if c.errors:
            print()
            print(f" {C.Y}LAST ERRORS:{C.RST}")
            for e in c.errors[-5:]:
                print(f"   {C.R}› {e}{C.RST}")

        if c.ok >= c.goal:
            print()
            print(f" {C.G}{C.BOLD}✔ GOAL REACHED — {c.ok} sent{C.RST}")
            c.running = False
        time.sleep(0.5)

# ────────────────────────────────────────────────
#  TRANSPORT — EMAIL
# ────────────────────────────────────────────────
def send_email(target, ttype, msg, proxy=None, smtp_acc=None):
    try:
        acc = smtp_acc or (SMTP_ACCOUNTS[0] if SMTP_ACCOUNTS else None)
        if not acc:
            return False, "smtp not configured"

        recipient = random.choice(RECIPIENTS)
        m = MIMEMultipart()
        m["From"] = acc["email"]
        m["To"] = recipient
        m["Subject"] = f"{random.choice(['URGENT','CRITICAL','ALERT','REPORT','ESCALATION'])}: {ttype.upper()} Violation — {target}"

        body = f"""To: Telegram Trust & Safety

Target: {target}
Type: {ttype}
Reported: {datetime.utcnow().isoformat()}Z
Reporter: {acc['email']}

{msg}

This is a good-faith report of a Terms of Service violation.
Requesting review under Telegram's Abuse Policy.

Report ID: {random.randint(100000, 999999)}
"""
        m.attach(MIMEText(body, "plain"))

        for ev in EVIDENCE_FILES:
            if os.path.exists(ev):
                with open(ev, "rb") as f:
                    part = MIMEApplication(f.read(), _subtype="octet-stream")
                    part.add_header("Content-Disposition", "attachment",
                                    filename=os.path.basename(ev))
                    m.attach(part)

        s = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
        s.ehlo(); s.starttls(); s.ehlo()
        s.login(acc["email"], acc["pass"])
        s.sendmail(acc["email"], recipient, m.as_string())
        s.quit()
        return True, ""
    except smtplib.SMTPAuthenticationError:
        return False, f"auth fail: {acc['email'][:15]}..."
    except smtplib.SMTPException as e:
        return False, f"smtp: {str(e)[:80]}"
    except Exception as e:
        return False, str(e)[:100]

# ────────────────────────────────────────────────
#  TRANSPORT — WEB
# ────────────────────────────────────────────────
def web_report(target, ttype, msg, proxy=None):
    try:
        url = random.choice(WEB_ENDPOINTS)
        data = {
            "message": f"{msg}\n\nTarget: {target}\nType: {ttype}\nReported: {datetime.utcnow().isoformat()}Z",
            "email": SMTP_ACCOUNTS[0]["email"] if SMTP_ACCOUNTS else "anon@protonmail.com",
            "phone": "",
            "setln": "en",
        }
        h = {
            "User-Agent": random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
                "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            ]),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "en-IN,en;q=0.9"]),
            "Origin": "https://telegram.org",
            "Referer": url,
        }
        proxies = {"http": proxy, "https": proxy} if proxy else None
        r = requests.post(url, data=data, headers=h, proxies=proxies,
                          timeout=20, verify=False, allow_redirects=True)
        if r.status_code in (200, 201, 202, 204, 301, 302):
            return True, ""
        if r.status_code == 429:
            return False, "429 rate-limited"
        return False, f"http {r.status_code}"
    except requests.exceptions.Timeout:
        return False, "timeout"
    except requests.exceptions.ProxyError:
        return False, "proxy dead"
    except requests.exceptions.ConnectionError:
        return False, "conn error"
    except Exception as e:
        return False, str(e)[:100]

# ────────────────────────────────────────────────
#  WORKER
# ────────────────────────────────────────────────
def worker(ttype, target, counter, mode):
    while counter.running and counter.ok < counter.goal:
        msg = build_message(ttype, target)

        if mode == "email":
            transports = [send_email]
        elif mode == "web":
            transports = [web_report]
        else:
            transports = [send_email, web_report]
            random.shuffle(transports)

        proxy = counter.next_proxy()
        smtp_acc = counter.next_smtp()
        ok = False
        err = ""

        for attempt in range(RETRY_MAX + 1):
            for fn in transports:
                if fn is send_email:
                    ok, err = fn(target, ttype, msg, proxy, smtp_acc)
                else:
                    ok, err = fn(target, ttype, msg, proxy)
                if ok: break
            if ok: break
            if attempt < RETRY_MAX:
                counter.retried()
                time.sleep(random.uniform(1.0, 2.5))

        if ok:
            counter.good()
            counter.reset_rate()
        else:
            counter.bad(err, target)
            if "429" in err or "rate" in err.lower():
                counter.slow_down()

        delay = random.uniform(MIN_DELAY, MAX_DELAY) * counter.rate_mult
        delay = min(delay, RATE_LIMIT_MAX_DELAY)
        time.sleep(delay)

# ────────────────────────────────────────────────
#  IN-APP ASSISTANT
# ────────────────────────────────────────────────
def inapp_assistant(target, ttype):
    os.system('clear')
    print(f"{C.CY}╔══════════════════════════════════════════════════╗{C.RST}")
    print(f"{C.CY}║   IN-APP REPORT ASSISTANT — REAL BAN YAHI SE    ║{C.RST}")
    print(f"{C.CY}╚══════════════════════════════════════════════════╝{C.RST}\n")

    if ttype == "channel":
        steps = [
            "1. Telegram app kholo",
            f"2. Search: {target}",
            "3. Channel open karo",
            "4. Top-right ⋮ tap karo",
            "5. 'Report' tap karo",
            "6. Reason: Spam / Violence / Illegal Goods",
            "7. Confirm karo",
            "8. DIFFERENT account se repeat (agar hai)",
        ]
    elif ttype == "dm":
        steps = [
            f"1. Search: {target}",
            "2. Profile open karo",
            "3. Top-right ⋮ tap karo",
            "4. 'Report' tap karo",
            "5. Reason: Spam / Fake Account / Violence",
            "6. Confirm karo",
        ]
    else:
        steps = [
            "1. Chat open karo",
            "2. Top-right ⋮ tap karo",
            "3. 'Report' tap karo",
            "4. Reason choose karo",
            "5. Confirm karo",
        ]

    for s in steps:
        print(f"  {C.W}{s}{C.RST}")
        time.sleep(0.12)

    print(f"\n{C.G}real ban sirf in-app report se aata hai.{C.RST}")
    print(f"{C.Y}email/web secondary hai — primary in-app hai.{C.RST}")
    input(f"\n{C.DIM}enter to return...{C.RST}")

# ────────────────────────────────────────────────
#  SAVE
# ────────────────────────────────────────────────
def save_log(c):
    try:
        fname = f"report_log_{int(time.time())}.csv"
        with open(fname, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["target","type","mode","sent","failed","retries","elapsed","timestamp"])
            w.writerow([c.target, c.type, c.mode, c.ok, c.fail, c.retry,
                        round(time.time()-c.start,1), datetime.utcnow().isoformat()])
        print(f"\n{C.G}log saved → {fname}{C.RST}")
    except Exception as e:
        print(f"\n{C.R}log save failed: {e}{C.RST}")

    if c.failed_targets:
        try:
            with open("failed_targets.txt", "a") as f:
                for t in c.failed_targets:
                    f.write(f"{t}\n")
            print(f"{C.Y}failed targets saved → failed_targets.txt{C.RST}")
        except Exception:
            pass

# ────────────────────────────────────────────────
#  MAIN
# ────────────────────────────────────────────────
def main():
    while True:
        os.system('clear')
        print(f"{C.CY}╔══════════════════════════════════════════════════╗{C.RST}")
        print(f"{C.CY}║  TUFF TG BOSS v6 — ULTIMATE WORKING             ║{C.RST}")
        print(f"{C.CY}║  6769676967 — baby's girl                       ║{C.RST}")
        print(f"{C.CY}╚══════════════════════════════════════════════════╝{C.RST}\n")

        if not SMTP_ACCOUNTS:
            print(f" {C.Y}[!] SMTP_ACCOUNTS empty — email mode fail hoga{C.RST}")
            print(f" {C.DIM}    Gmail app password bana ke script me daal{C.RST}\n")

        print(f" {C.W}MENU:{C.RST}")
        print(f"   1. Start mass report engine")
        print(f"   2. In-app report assistant (REAL BAN)")
        print(f"   3. Exit\n")

        m = input(f"{C.CY}choice: {C.RST}").strip()
        if m == "3": return
        if m == "2":
            t = input(f"{C.CY}type (channel/dm/chatid): {C.RST}").strip()
            tg = input(f"{C.CY}target: {C.RST}").strip()
            inapp_assistant(tg, t)
            continue
        if m != "1": continue

        print(f"\n {C.W}Target Type:{C.RST}")
        print("   1. Channel")
        print("   2. DM / User")
        print("   3. Chat ID")
        tc = input(f"{C.CY}choice (1-3): {C.RST}").strip()
        ttype = {"1":"channel","2":"dm","3":"chatid"}.get(tc)
        if not ttype: continue

        target = input(f"{C.CY}target (@username or id): {C.RST}").strip()
        if not target: continue

        try:
            goal = int(input(f"{C.CY}how many reports: {C.RST}").strip() or "100")
        except ValueError: continue

        print(f"\n {C.W}Transport:{C.RST}")
        print("   1. Email only")
        print("   2. Web form only")
        print("   3. Both (recommended)")
        mc = input(f"{C.CY}choice (1-3): {C.RST}").strip()
        mode = {"1":"email","2":"web","3":"both"}.get(mc, "both")

        print(f"\n {C.Y}──────────────────────────────{C.RST}")
        print(f" target  : {C.CY}{target}{C.RST}")
        print(f" type    : {C.CY}{ttype}{C.RST}")
        print(f" goal    : {C.CY}{goal}{C.RST}")
        print(f" mode    : {C.CY}{mode}{C.RST}")
        print(f" smtp    : {C.CY}{len(SMTP_ACCOUNTS)}{C.RST}")
        print(f" proxies : {C.CY}{len(PROXY_LIST)}{C.RST}")
        print(f" evidence: {C.CY}{len(EVIDENCE_FILES)}{C.RST}")
        print(f" workers : {C.CY}{WORKERS}{C.RST}")
        print(f" {C.Y}──────────────────────────────{C.RST}")
        if input(f"\n {C.W}start? (y/n): {C.RST}").strip().lower() != "y": continue

        c = Counter(ttype, target, goal)
        c.mode = mode

        threading.Thread(target=show, args=(c,), daemon=True).start()
        for _ in range(WORKERS):
            threading.Thread(target=worker, args=(ttype, target, c, mode), daemon=True).start()

        try:
            while c.running:
                time.sleep(1)
        except KeyboardInterrupt:
            c.running = False
            print(f"\n{C.Y}stopped.{C.RST}")

        time.sleep(1.5)
        save_log(c)
        input(f"\n{C.DIM}enter to return...{C.RST}")

if __name__ == "__main__":
    main()