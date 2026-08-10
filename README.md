# 🎮 原神 HoYoLab 毎日チェックイン 自動化

毎日自動でHoYoLabのチェックインボーナスを受け取るツールです。  
GitHubのサーバーが代わりに毎朝チェックインし、結果をDiscordに通知します（通知は任意）。

> ⚠️ **注意**: このツールはHoYoLab APIを利用しています。利用規約に反する可能性があるため、自己責任でご使用ください。

---

## 📋 セットアップ手順（約15分）

### ステップ1：このリポジトリをForkする

1. このページ右上の **「Fork」** ボタンをクリック
2. **「Create fork」** をクリック
3. 自分のアカウントにコピーされます

> ⚠️ Fork後、必ずリポジトリを **Private（非公開）** にしてください  
> Settings → 一番下「Danger Zone」→「Change visibility」→「Make private」

---

### ステップ2：HoYoLabの認証情報を取得する

**PCのChromeブラウザ**で操作してください。

1. [HoYoLab](https://www.hoyolab.com/) にログイン
2. キーボードの **F12** キーを押す
3. 上タブ **「Application」** → 左メニュー **「Cookies」→「https://www.hoyolab.com」**
4. 以下の2つの値をメモする：

   | 探す名前 | メモする列 |
   |---------|----------|
   | `ltuid_v2`（または `ltuid`） | Value 列の**数字** |
   | `ltoken_v2`（または `ltoken`） | Value 列の**長い文字列** |

---

### ステップ3：認証情報をGitHubに登録する

1. Forkしたリポジトリの **「Settings」** タブ
2. 左メニュー **「Secrets and variables」→「Actions」**
3. **「New repository secret」** で以下の2つを登録：

   | Name | Secret（Value欄の値）|
   |------|-------------------|
   | `LTUID` | `ltuid_v2` の数字 |
   | `LTOKEN` | `ltoken_v2` の長い文字列 |

> 💡 `ltuid_v2` が見つからない場合は `ltuid` の値を使ってください（`ltoken` も同様）

---

### ステップ4（任意）：Discordに結果を通知する

チェックインの結果をDiscordのチャンネルに通知できます。不要な場合はスキップしてください。

#### Webhook URLの取得方法

1. 通知を送りたいDiscordサーバーの **チャンネル設定** を開く（歯車アイコン）
2. **「連携サービス」→「ウェブフック」→「新しいウェブフック」**
3. 名前を設定して **「ウェブフックURLをコピー」**

#### GitHubへの登録

ステップ3と同じ手順で、以下のSecretを追加登録：

| Name | Secret |
|------|--------|
| `DISCORD_WEBHOOK_URL` | コピーしたWebhook URL |

---

### ステップ5：動作確認をする

1. **「Actions」** タブ → **「HoYoLab 原神 毎日チェックイン」**
2. **「Run workflow」→「Run workflow」** をクリック
3. ✅ 緑のチェックが出れば成功！Discordにも通知が届きます

---

## ⏰ 自動実行のタイミング

毎日 **日本時間 午前9時** に自動実行されます。

---

## ❓ よくある質問

**Q. ❌ が出てチェックインに失敗した**  
A. Cookieの期限切れが原因の場合がほとんどです。ステップ2〜3をやり直してください。Cookieは数ヶ月〜1年程度で期限切れになります。

**Q. `ltuid_v2` が見つからない**  
A. `ltuid`（`_v2` なし）を探してください。どちらでも動作します。

**Q. Actionsタブに何も表示されない**  
A. 初回Forkの場合、ActionsタブでWorkflowの有効化を求められることがあります。**「I understand my workflows, go ahead and enable them」** をクリックしてください。
