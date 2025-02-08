## Usage

### 起動方法

1. **環境変数ファイルの準備**

   - `.env` ファイルをルートディレクトリに作成し、以下の情報を記載してください
     ```.env
     MYSQL_ROOT_PASSWORD=root
     MYSQL_DATABASE=techhub_db
     MYSQL_USER=testuser
     MYSQL_PASSWORD=testuser
     TZ=Asia/Tokyo
     DEBUG=True
     ```

2. **Docker イメージのビルド**

   - 初めて実行する場合、以下のコマンドで Docker イメージをビルドします
     ```bash
     docker compose up --build
     ```

3. **コンテナの起動**

   - アプリケーションを起動するには、以下を実行してください
     **【本番環境】**
     ```bash
     docker compose up
     ```
   - バックグラウンドで実行したい場合
     ```bash
     docker compose up -d
     ```
     **【開発環境】**
     ```bash
     docker compose -f compose.dev.yaml up --build
     ```

4. **ブラウザでアクセス**
   - 以下の URL にアクセスして、アプリケーションを確認します
     - `http://localhost:8080/techhub/` (Nginx 経由)
     - Hello E-tema!と表示されます

### 停止方法

1. **コンテナの停止**
   - 起動中のコンテナを停止するには以下を実行
     ```bash
     docker compose down
     ```
     **【開発環境】**
   ```bash
   docker compose -f compose.dev.yaml down
   ```

### デバッグ方法

1. **ログの確認**

   - コンテナのログを確認するには以下を実行

     ```bash
     docker logs <container_name>
     ```

     例:

     ```bash
     docker logs django
     docker logs nginx
     docker logs mysql
     ```

   - ネットワークの状態確認

   ```
   docker network inspect dev_network
   ```

### ブランチ命名規則

1\. ローカルでブランチを作成。ブランチ名は「`自分の名前#issue番号`」　例）fuji#1
<br>
2\. コードを編集
<br>
3\. コミットする。コミットメッセージには「`#issue番号`」をつける

```
例）git commit -m ‘#1ログイン機能追加’
```

<br>
4. リモートへgit pushする
<br>
5. プルリクする。レビュワーは特に指定せず、見れる人が見てdevelopにマージする。（レビュワーが勝手に設定されて外せないことがあるようで、その場合はそのままプルリクする。レビュワーじゃない人でもマージは可能。）

## 環境構築\_開発（コンテナ起動後）

1. .env ファイルがあることを確認（.env ファイルについては当ファイルの上部を参照）
2. 以下のコマンドでコンテナ内で migrate する
   　 docker exec -it django-dev python3 manage.py migrate
   これにより MySQL コンテナ内に DB が migrations ファイルにより作成される。
3. 本当に DB できてるか確認するなら以下のコマンドで MySQL コンテナに入る
   docker exec -it mysql bash
   mysql -u testuser -p
   パスワードは.env 参照
   mysql から出る時は exit
4. Django 管理画面が使用できるように superuser 設定
   docker exec -it django-dev python3 manage.py createsuperuser
5. Feed 情報 Django 管理画面で以下を設定
   Qiita http://qiita.com/{account_name}/feed.atom
   Zenn https://zenn.dev/{account_name}/feed
6. Djnago 管理画面　：localhost:8001/admin/
   　　 techhub サイト 　：localhost:8001/techhub/ 7.　記事取得コマンドはカスタムコマンドで設定
   　　　 docker exec -it django-dev python3 manage.py fetch_articles
