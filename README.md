# Tài liệu Heirloom

Tài liệu công khai dành cho người chơi và quản trị viên của plugin Heirloom Minecraft, cùng các tiện ích mở rộng Heirloom Distillery (hệ thống ủ rượu) và Heirloom Cafe (hệ thống cà phê).

## Xem trước cục bộ tại máy nhà

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Mở `http://127.0.0.1:8000/`.

## Tái tạo tham chiếu nguồn

Trình tạo wiki sẽ đọc các tệp JSON của Core và Cafe được đóng gói sẵn, cùng với toàn bộ các gói nội dung đã phát hành trong thư mục `../foodplugin/packs/*/content/`. Toàn bộ tài liệu tham chiếu vật phẩm, trang công thức, trang gói nội dung, hệ thống điều hướng và bảng biểu tượng sẽ được xây dựng lại đồng thời trong một lần.

```bash
.venv/bin/python tools/generate_reference_pages.py --use-visual-pack-icons
.venv/bin/python tools/check_content_pack_generation.py
.venv/bin/python tools/check_icon_modes.py
.venv/bin/python tools/check_recipe_slot_badges.py
.venv/bin/mkdocs build --strict
```

Mỗi gói nội dung phải sử dụng giá trị siêu dữ liệu `pack` nhất quán trong cả JSON vật phẩm và JSON công thức. Nếu hai giá trị siêu dữ liệu không khớp, quá trình tạo sẽ dừng lại thay vì xuất ra một gói dữ liệu chứa các thành phần không đồng nhất.

## Xuất bản

Quy trình GitHub Actions được tích hợp sẵn sẽ tự động xây dựng trang MkDocs và xuất bản lên GitHub Pages từ nhánh `gh-pages`.

Sau khi quy trình workflow chạy thành công lần đầu, hãy bật Pages trong cài đặt kho lưu trữ:
- Nguồn: Deploy from branch
- Nhánh: `gh-pages`
- Thư mục: `/`

Sau đó, sử dụng URL đã được xuất bản trong danh sách plugin công khai cũng như trong mọi liên kết hướng dẫn được sử dụng trong trò chơi:

```yml
guide-url: "https://kernel-person.github.io/heirloom-docs/"
```