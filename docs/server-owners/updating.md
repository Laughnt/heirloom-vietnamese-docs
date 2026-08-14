# Ghi chú cập nhật và chuyển đổi

## Ghi chú phiên bản 2.5

- Thông báo khởi động máy chủ đã được chuẩn hóa và hiển thị gọn gàng hơn.
- Có thể tìm kiếm công thức bằng lệnh `/hl search`.
- Nexo và ItemsAdder hiện sử dụng chung `visual_id`, cho phép xác định hình ảnh mà không phụ thuộc vào plugin cung cấp gói đồ hoạ.
- Các món ăn đã chế biến sẽ không còn tự động nhận hiệu ứng Hồi phục hoặc Độ bão hòa cộng thêm ngẫu nhiên.
- Bổ sung sẵn nội dung cho cây Hành tây và nhóm cây Allium.
- Khôi phục các định nghĩa cây nho của Distillery.

## Ghi chú phiên bản 2.0

- Hệ thống bảo vệ khu vực đã được viết lại, sử dụng WorldGuard và các sự kiện Bukkit tiêu chuẩn.
- Bổ sung trường `consume_return` dùng chung.
- Bổ sung hook hỗ trợ cơ chế tự động trồng lại và tích hợp EcoEnchants.
- Bổ sung gói hạt giống và cơ chế khám phá thế giới.
- Mở rộng các hệ thống Thành tựu, Thông thạo món ăn và Món ăn yêu thích được tích hợp sẵn.

## Danh sách kiểm tra khi cập nhật

1. Sao lưu `plugins/Heirloom/`.
2. Tắt máy chủ.
3. Thay thế các file `.jar`.
4. Khởi động máy chủ và kiểm tra các cảnh báo xuất hiện khi khởi động.
5. Chạy `/hl debug test`.
6. Kiểm tra lại cân bằng các món ăn tùy chỉnh nếu trước đây bạn từng phải tự xử lý các hiệu ứng ẩn.
