# 搜尋食譜系統 - 路由設計文件

本文件定義了 Flask 應用程式中所有的 URL 路由、HTTP 方法，以及對應的 Jinja2 網頁模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁與熱門食譜 | GET | `/` | `index.html` | 顯示搜尋列與最新發布的食譜 |
| 搜尋食譜 | GET | `/search` | `search_results.html` | 接收 `?q=` 參數，顯示搜尋結果清單 |
| 註冊頁面 | GET | `/register` | `register.html` | 顯示建立新帳號的表單 |
| 處理註冊 | POST | `/register` | — | 寫入資料庫，成功後重導向至登入頁 |
| 登入頁面 | GET | `/login` | `login.html` | 顯示登入表單 |
| 處理登入 | POST | `/login` | — | 驗證密碼，設定 Session，重導向至首頁 |
| 登出系統 | GET | `/logout` | — | 清除 Session 並重導向至首頁 |
| 新增食譜頁面 | GET | `/recipe/create` | `recipe_create.html` | 顯示撰寫食譜的表單 (需登入) |
| 建立食譜 | POST | `/recipe/create` | — | 接收表單存入資料庫，重導向至詳細頁 |
| 食譜詳情 | GET | `/recipe/<int:id>` | `recipe_detail.html` | 顯示特定食譜內容與歷史評論 |
| 收藏食譜 | POST | `/recipe/<int:id>/save` | — | 加入收藏清單，完成後重導向回詳情頁 |
| 取消收藏 | POST | `/recipe/<int:id>/unsave` | — | 移出收藏清單，完成後重導向回詳情頁 |
| 提交評論 | POST | `/recipe/<int:id>/review`| — | 寫入評分與評論，重導向回詳情頁 |
| 產生購物清單 | GET | `/recipe/<int:id>/shopping`| `shopping_list.html` | 單獨顯示該食譜的食材，方便列印或截圖 |
| 個人主頁 | GET | `/profile` | `profile.html` | 顯示自己的食譜與已收藏的食譜 (需登入) |

## 2. 路由詳細說明

### Auth 模組 (`app/routes/auth.py`)
- **`/register` (POST)**
  - 輸入：表單的 `username`, `email`, `password`
  - 處理邏輯：檢查 email 是否已存在，將密碼 hash 後存入 `User` Model。
  - 輸出：成功重導至 `/login`，失敗則帶著錯誤訊息重新渲染 `register.html`。
- **`/login` (POST)**
  - 輸入：表單的 `email`, `password`
  - 處理邏輯：查詢 `User`，比對 password hash，將 user_id 存入 Flask Session。
  - 輸出：成功重導至 `/`，失敗重新渲染 `login.html`。

### Recipe 模組 (`app/routes/recipe.py`)
- **`/` (GET)**
  - 處理邏輯：呼叫 `Recipe.get_all()` 撈取最新食譜。
- **`/search` (GET)**
  - 輸入：URL Query Parameter `?q=關鍵字`
  - 處理邏輯：呼叫 `Recipe.get_all(search_query)`。
- **`/recipe/<id>` (GET)**
  - 處理邏輯：呼叫 `Recipe.get_by_id()`，以及 `Review.get_by_recipe()` 獲取該食譜的所有資料與留言。若有登入，一併檢查 `SavedRecipe.is_saved()` 狀態以顯示對應按鈕。
  - 錯誤處理：找不到食譜時回傳 404 頁面。
- **`/recipe/create` (POST)**
  - 輸入：表單的 `title`, `description`, `ingredients`, `steps`, `image_url`
  - 處理邏輯：檢查 Session 是否有登入，呼叫 `Recipe.create()`。
- **`/recipe/<id>/review` (POST)**
  - 輸入：表單的 `rating` (1-5), `comment`
  - 處理邏輯：檢查登入，呼叫 `Review.create()`。
- **`/recipe/<id>/save` (POST)**
  - 處理邏輯：檢查登入，呼叫 `SavedRecipe.save()`。

## 3. Jinja2 模板清單 (位於 `app/templates/`)

所有頁面均繼承自 `base.html`，以保持 Navbar 與 Footer 的一致性。

1. **`base.html`**：全域版面配置 (Header, Footer, 引入 CSS/JS)。
2. **`index.html`**：首頁 (顯示搜尋列與精選食譜卡片)。
3. **`search_results.html`**：搜尋結果頁面。
4. **`register.html`**：註冊表單。
5. **`login.html`**：登入表單。
6. **`recipe_create.html`**：撰寫食譜表單。
7. **`recipe_detail.html`**：食譜詳細介紹 (含食材清單、步驟說明、評論區、操作按鈕)。
8. **`shopping_list.html`**：純淨版的食材清單頁面 (適合列印/採買時看)。
9. **`profile.html`**：我的收藏與我的食譜。
