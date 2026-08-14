# Lệnh và Quyền của hệ thống Ủ rượu

Sử dụng lệnh `/hld` để tương tác với tiện ích này.

| Lệnh | Chức năng | Quyền cần thiết |
| --- | --- | --- |
| `/hld help` | Hiển thị trợ giúp | `heirloom.distillery.use` |
| `/hld info` | Thông tin tiện ích | `heirloom.distillery.use` |
| `/hld menu` | Giao diện đồ họa của Distillery | `heirloom.distillery.use` |
| `/hld list` | Liệt kê các vật phẩm | `heirloom.distillery.use` |
| `/hld stats <vật phẩm>` | Xem thông số nguyên liệu | `heirloom.distillery.use` |
| `/hld drunk [người chơi]` | Kiểm tra mức độ say | tự dùng cho bản thân, cần cấp quyền cho người khác |
| `/hld give <vật phẩm> [số lượng]` | Cấp vật phẩm | `heirloom.distillery.admin` |
| `/hld reload` | Tải lại cấu hình | `heirloom.distillery.admin` |
| `/hld devmode [bật|tắt|trạng thái]` | Bật chế độ xử lý nhanh (dùng cho nhà phát triển) | `heirloom.distillery.admin` |
| `/hld lab` | Mở Phòng thí nghiệm Ủ | `heirloom.distillery.admin` |
