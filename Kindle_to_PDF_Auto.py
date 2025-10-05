import os
import time
import pyautogui

# ==============================================================================
# --- ユーザーが編集する項目 ---
# ==============================================================================
# 1. 撮影したい総ページ数をここに設定
total_pages = 459

# 2. スクリーンショットを撮る領域
#    (左上のX, 左上のY, 幅, 高さ)
screenshot_region = (6, 59, 1920, 1080)

# 3. ページをめくるためにクリックする場所の座標
next_page_click_coords = (1890, 5559)

# 4. 各操作の間の待機時間（秒）
wait_time = 0.5

# 5. 保存するフォルダ名とPDFファイル名
folder_name = "Kindle_Screenshots"
output_pdf_name = "Kindle_Book.pdf"

# ==============================================================================
# --- これより下は編集不要です ---
# ==============================================================================

# --- ステップ1：スクリーンショットの撮影 ---
print("--- ステップ1: スクリーンショットの撮影を開始します ---")

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
save_folder = os.path.join(desktop_path, folder_name)
os.makedirs(save_folder, exist_ok=True)

print(f"画像はデスクトップの「{folder_name}」フォルダに保存されます。")
print("5秒後に自動化を開始します。Kindleのウィンドウをクリックして準備してください。")
time.sleep(5)

for i in range(total_pages):
    page_num = i + 1
    print(f"撮影中... {page_num} / {total_pages} ページ目")

    file_name = f"page_{str(page_num).zfill(3)}.png"
    save_path = os.path.join(save_folder, file_name)

    try:
        # 315ページ目のスクリーンショット前に特別処理
        if page_num == 316:
            print("315ページ目: x967 y120 を2回クリックします...")
            pyautogui.click(967, 120)
            time.sleep(1)
            pyautogui.click(967, 120)
            time.sleep(1)

        screenshot = pyautogui.screenshot(region=screenshot_region)
        screenshot.save(save_path)
        pyautogui.press('right')
        time.sleep(wait_time)
    except Exception as e:
        print(f"\nエラーが発生しました (ページ: {page_num})")
        print(f"エラー内容: {e}")
        print("処理を停止します。")
        exit()

print("全ての撮影が完了しました！")
print("\n✨✨ スクリーンショット撮影が完了しました！ ✨✨")
print("PDFを作成する場合は、create_pdf.py を実行してください。")