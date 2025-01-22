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
     ```bash
     docker compose up 
     ```
   - バックグラウンドで実行したい場合
     ```bash
     docker compose up -d
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
