# HoYoLAB-AutoLogin

HoYoLABに自動チェックインするスクリプト。結果をDiscordに送信します(任意)。
> 利用規約を確認し自己責任で使用してください。

---

## 設定手順

### 1. リポジトリをForkする

1. ページ右上の **「Fork」** ボタンをクリック
2. **「Create fork」** をクリック
3. 自分のアカウントにForkされます

> Fork後、リポジトリを必ず **Private** にしてください  
> Settings → Danger Zone → Change visibility → Make private  

### 2. Cookieを取得

1. [HoYoLab](https://www.hoyolab.com/) にログイン
2. キーボードの **F12** キーを押す
3. **「Application」** タブ → **「Cookies」→「https://www.hoyolab.com」**
4. 以下の2つをメモする

   | Name | Value |
   |------|-------------------|
   | `ltuid_v2` | Value の数字列 |
   | `ltoken_v2` | Value の文字列 |



### 3. CookieをGithubに設定

1. Forkしたリポジトリの **「Settings」** タブ
2. **「Secrets and variables」→「Actions」**
3. **「New repository secret」** で、

   | Name | Secret |
   |------|-------------------|
   | `LTUID` | `ltuid_v2` の数字列 |
   | `LTOKEN` | `ltoken_v2` の文字列 |



### 4. Discordに結果を送信 (任意)

#### Webhookを作成

1. 通知を送信したいチャンネルの **チャンネル設定** を開く
2. **「連携サービス」→「ウェブフック」→「新しいウェブフック」**
3. 名前を設定して **「ウェブフックURLをコピー」**

#### Githubに登録

ステップ3と同じ方法で登録：

| Name | Secret |
|------|--------|
| `DISCORD_WEBHOOK_URL` | コピーしたWebhook URL |



### 5. 動作確認

1. **「Actions」** タブ → **「HoYoLAB 自動チェックイン」**
2. **「Run workflow」→「Run workflow」** をクリック
3. Discordに通知が送信されたら成功



## **Q. Actionsタブに何も表示されない**  
A. 初回Forkの場合、ActionsタブでWorkflowの有効化を求められることがあります。**「I understand my workflows, go ahead and enable them」** をクリックしてください。
