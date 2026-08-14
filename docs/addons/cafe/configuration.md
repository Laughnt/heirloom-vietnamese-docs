# Cấu hình hệ thống Cà phê

Hệ thống Cà phê ghi các tài nguyên có thể chỉnh sửa vào thư mục `plugins/HeirloomCafe/`:

- `custom_items-cafe.json`
- `crops-cafe.json`
- `recipes-cafe.json`
- `config.yml`
- `lang/en.yml`

Hệ thống Cà phê sẽ hủy đăng ký và đăng ký lại các vật phẩm, cây trồng và công thức thuộc sở hữu của tiện ích khi gọi lệnh tải lại, giúp trình duyệt công thức có thể làm mới.

## Kiểm tra sau khi thay đổi

Sau khi chỉnh sửa công thức, hãy chạy `/hl reload`, tìm kiếm từ khoá `cafe`, sau đó kiểm tra một chuỗi công thức cà phê và một chuỗi công thức trà, giúp kiểm tra cả khâu sơ chế tại các trạm nấu ăn cơ bản lẫn bước pha chế tại Máy pha chế.
