# Tài liệu Heirloom

Tài liệu dành cho người dùng và quản trị viên công khai của plugin Heirloom Minecraft và addon Heirloom Distillery.

## Xem trước cục bộ

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Mở `http://127.0.0.1:8000/`.

## Tái tạo tham chiếu nguồn

Trình tạo wiki sẽ đọc các tệp JSON của Core và Cafe được đóng gói sẵn cùng với mọi gói nội dung đã phát hành trong thư mục `../foodplugin/packs/*/content/`. Trình tạo sẽ xây dựng lại toàn bộ tài liệu tham chiếu vật phẩm, trang công thức, trang gói nội dung, điều hướng và bảng kê biểu tượng cùng lúc.

```bash
.venv/bin/python tools/generate_reference_pages.py --use-visual-pack-icons
.venv/bin/python tools/check_content_pack_generation.py
.venv/bin/python tools/check_icon_modes.py
.venv/bin/python tools/check_recipe_slot_badges.py
.venv/bin/mkdocs build --strict
```

Mỗi gói nội dung phải sử dụng siêu dữ liệu `pack` khớp trong JSON vật phẩm và JSON công thức. Siêu dữ liệu không khớp sẽ ngừng quá trình tạo thay vì xuất bản dữ liệu gói hỗn hợp.

## Xuất bản

Quy trình GitHub Actions được tích hợp sẵn sẽ xây dựng trang MkDocs và xuất bản lên GitHub Pages từ nhánh `gh-pages`.

Sau khi quy trình workflow chạy thành công lần đầu, hãy bật Pages trong cài đặt kho lưu trữ:

- Nguồn: Deploy from branch
- Nhánh: `gh-pages`
- Thư mục: `/`

Sau đó sử dụng URL đã xuất bản trong danh sách plugin công khai và bất kỳ liên kết hướng dẫn nào trong trò chơi:

```yml
guide-url: "https://kernel-person.github.io/heirloom-docs/"
```