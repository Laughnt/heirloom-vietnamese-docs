# Tổng quan về tích hợp hiển thị

Heirloom có thể hoạt động mà không cần gói tài nguyên bằng cách sử dụng vật liệu có sẵn trong Minecraft và kết cấu đầu người chơi. Quản trị viên cũng có thể sử dụng các hệ thống hỗ trợ tùy chọn để thay đổi cách hiển thị này.

## Quy trình không phụ thuộc hệ thống nào

1. Khai báo `visual_id` trong thông tin vật phẩm.
2. Công thức có thể sử dụng `SET_VISUAL_ITEM`.
3. `VisualItemResolver` sẽ tìm `visual_id` tương ứng từ các hệ thống đã được đăng ký.
4. Nếu không tìm thấy, Heirloom sẽ sử dụng vật phẩm thông thường làm phương án dự phòng.

Cách này giúp dữ liệu công thức không phụ thuộc vào Nexo hay ItemsAdder.

## Quy tắc sử dụng

Nên sử dụng ID vật phẩm và `visual_id` của Heirloom làm tên cố định để sử dụng chung. Sau đó, để Nexo hoặc ItemsAdder liên kết các tên này với model tương ứng. Không nên đưa tên riêng của Nexo hoặc ItemsAdder trực tiếp vào công thức, trừ khi Quản trị viên muốn công thức đó chỉ hoạt động với hệ thống tương ứng và không thể chuyển sang hệ thống khác.
