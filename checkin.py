import os
import requests

# ===== 設定 =====
ACT_ID = "e202102251931481"
SIGN_URL = "https://sg-hk4e-api.hoyolab.com/event/sol/sign"
INFO_URL  = "https://sg-hk4e-api.hoyolab.com/event/sol/info"
HOME_URL  = "https://sg-hk4e-api.hoyolab.com/event/sol/home"
LANG = "ja-jp"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Referer": "https://act.hoyolab.com/",
    "Origin":  "https://act.hoyolab.com",
    "Accept":  "application/json, text/plain, */*",
    "Accept-Language": "ja-JP,ja;q=0.9",
    "Content-Type": "application/json;charset=UTF-8",
    "x-rpc-signgame": "hk4e",
    "x-rpc-language": "ja-jp",
}

# ---------- Cookie ヘルパー ----------

def build_cookie() -> str:
    """
    環境変数から Cookie 文字列を組み立てる。
    HOYOLAB_COOKIE が直接セットされていればそれを使う。
    なければ LTUID / LTOKEN の組み合わせで構築する。
    """
    direct = os.environ.get("HOYOLAB_COOKIE", "").strip()
    if direct:
        # mi18nLang が含まれていなければ追記して言語を日本語に固定する
        if "mi18nLang" not in direct:
            direct = direct.rstrip("; ") + "; mi18nLang=ja-jp;"
        return direct

    ltuid  = os.environ.get("LTUID",  "").strip()
    ltoken = os.environ.get("LTOKEN", "").strip()
    if ltuid and ltoken:
        return f"ltuid_v2={ltuid}; ltoken_v2={ltoken}; mi18nLang=ja-jp;"

    raise ValueError(
        "エラー: 認証情報が見つかりません。"
    )

# ---------- API ----------

def get_sign_info(cookie: str) -> dict:
    resp = requests.get(
        INFO_URL,
        headers={**HEADERS, "Cookie": cookie},
        params={"act_id": ACT_ID, "lang": LANG},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()

def get_today_reward(cookie: str, day_index: int) -> dict | None:
    """今日は何がもらえるかな？"""
    try:
        resp = requests.get(
            HOME_URL,
            headers={**HEADERS, "Cookie": cookie},
            params={"act_id": ACT_ID, "lang": LANG},
            timeout=30,
        )
        resp.raise_for_status()
        awards = resp.json().get("data", {}).get("awards", [])
        if awards and day_index < len(awards):
            return awards[day_index]
    except Exception:
        pass
    return None

def sign(cookie: str) -> dict:
    resp = requests.post(
        SIGN_URL,
        headers={**HEADERS, "Cookie": cookie},
        json={"act_id": ACT_ID, "lang": LANG},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()

# ---------- Discord ----------

def send_discord(webhook_url: str, success: bool, message: str, reward: dict | None = None):
    if not webhook_url:
        return

    if success:
        color = 0x57F287  # 緑
        title = "✅ チェックインに成功したよ！"
        desc  = message
        if reward:
            desc += f"\n\n **本日の報酬**: {reward['name']} × {reward['cnt']}"
    else:
        color = 0xED4245  # 赤
        title = "❌ チェックインに失敗したよ。"
        desc  = message

    payload = {
        "embeds": [{
            "title": title,
            "description": desc,
            "color": color,
            "footer": {"text": "HoYoLAB 自動チェックイン"},
        }]
    }

    if reward and reward.get("icon"):
        payload["embeds"][0]["thumbnail"] = {"url": reward["icon"]}

    try:
        r = requests.post(webhook_url, json=payload, timeout=10)
        r.raise_for_status()
        print("[Discord] 通知送信に成功")
    except Exception as e:
        print(f"[Discord] 通知送信に失敗: {e}")

# ---------- メイン ----------

def main():
    print("=== HoYoLAB 自動チェックイン ===")

    cookie      = build_cookie()
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()

    # チェックイン済み確認
    info_res = get_sign_info(cookie)
    if info_res.get("retcode") == 0:
        info = info_res["data"]
        total_days = info.get("total_sign_day", 0)

        if info.get("is_sign"):
            msg = f"今日はすでにチェックインしたよ！（今月の累計: {total_days}日）"
            print(f"✅ {msg}")
            send_discord(webhook_url, True, msg)
            return

    # チェックイン実行
    result  = sign(cookie)
    retcode = result.get("retcode", -1)
    message = result.get("message", "不明なエラー")

    if retcode in (0, -5003):
        # 成功後にもう一回 info を取得して累計日数を表示
        info_res2  = get_sign_info(cookie)
        total_days = info_res2.get("data", {}).get("total_sign_day", total_days if 'total_days' in dir() else "?")
        reward     = get_today_reward(cookie, int(total_days) - 1) if str(total_days).isdigit() else None

        msg = f"チェックインに成功したよ！（今月の累計: {total_days}日）"
        print(f"✅ {msg}")
        send_discord(webhook_url, True, msg, reward)
    else:
        msg = f"チェックインに失敗したよ。 (コード: {retcode}): {message}\nCookieが期限切れの可能性があります。"
        print(f"❌ {msg}")
        send_discord(webhook_url, False, msg)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
