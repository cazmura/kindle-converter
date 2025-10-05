#!/usr/bin/env python3
"""
画像からPDFを作成するスクリプト（横向き、圧縮対応）
"""

import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4

# ==============================================================================
# --- ユーザーが編集する項目 ---
# ==============================================================================
# 画像が保存されているフォルダ名
folder_name = "Kindle_Screenshots"

# 出力するPDFファイル名
output_pdf_name = "Kindle_Book.pdf"

# 画像の品質（1-100, 低いほど容量削減、85程度が推奨）
image_quality = 85

# 目標ファイルサイズ（MB）
target_size_mb = 200

# ==============================================================================
# --- PDF作成処理 ---
# ==============================================================================

print("--- PDF文書の作成を開始します ---")

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
save_folder = os.path.join(desktop_path, folder_name)

try:
    image_files = sorted([f for f in os.listdir(save_folder) if f.endswith('.png')])

    if not image_files:
        print(f"エラー: 「{folder_name}」フォルダに画像ファイルが見つかりません。")
        exit()

    print(f"{len(image_files)}個の画像ファイルをPDFに挿入します。")
    print(f"ページサイズ: A4横向き")
    print(f"画像品質: {image_quality}")
except FileNotFoundError:
    print(f"エラー: 「{folder_name}」というフォルダが見つかりません。")
    exit()

# 一時フォルダを作成（圧縮画像用）
temp_folder = os.path.join(save_folder, "temp_compressed")
os.makedirs(temp_folder, exist_ok=True)

# 画像を圧縮
print("\n画像を圧縮中...")
compressed_images = []
for i, image_file in enumerate(image_files):
    image_path = os.path.join(save_folder, image_file)
    print(f"圧縮中 ({i+1}/{len(image_files)}): {image_file}")

    img = Image.open(image_path)

    # PNGをJPEGに変換して圧縮
    if img.mode in ('RGBA', 'LA', 'P'):
        # 透過情報がある場合は白背景に変換
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # 圧縮して保存
    compressed_path = os.path.join(temp_folder, f"{os.path.splitext(image_file)[0]}.jpg")
    img.save(compressed_path, 'JPEG', quality=image_quality, optimize=True)
    compressed_images.append(compressed_path)

# PDF作成（横向き）
print("\nPDFを作成中...")
pdf_path = os.path.join(desktop_path, output_pdf_name)
page_size = landscape(A4)  # A4を横向きに
c = canvas.Canvas(pdf_path, pagesize=page_size)

for i, image_path in enumerate(compressed_images):
    print(f"PDF挿入中 ({i+1}/{len(compressed_images)}): {os.path.basename(image_path)}")

    img = Image.open(image_path)
    img_width, img_height = img.size

    # 横向きA4サイズに合わせて調整
    c.drawImage(image_path, 0, 0, width=page_size[0], height=page_size[1],
                preserveAspectRatio=True)
    c.showPage()

c.save()

# ファイルサイズを確認
pdf_size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
print(f"\nPDFを保存しました: {output_pdf_name}")
print(f"ファイルサイズ: {pdf_size_mb:.2f} MB")

# 目標サイズを超えている場合は警告
if pdf_size_mb > target_size_mb:
    print(f"\n⚠️  ファイルサイズが目標({target_size_mb}MB)を超えています。")
    print(f"image_quality の値を下げて再実行してください。")
    print(f"現在の設定: {image_quality} → 推奨: {int(image_quality * 0.8)}")
else:
    print(f"✓ ファイルサイズは目標({target_size_mb}MB)以下です。")

# 一時フォルダを削除
print("\n一時ファイルを削除中...")
for compressed_path in compressed_images:
    os.remove(compressed_path)
os.rmdir(temp_folder)

print("\n✨✨ PDF作成が完了しました！ ✨✨")
