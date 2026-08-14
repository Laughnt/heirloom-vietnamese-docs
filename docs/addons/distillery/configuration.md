# Cấu hình hệ thống Ủ rượu

Các tệp quan trọng cần biết:

- `plugins/HeirloomDistillery/config.yml`
- `plugins/HeirloomDistillery/ingredients.yml`
- `plugins/HeirloomDistillery/words.yml`
- `plugins/HeirloomDistillery/lang/en.yml`

Lệnh `/hld reload` sẽ tải lại các thiết lập được hỗ trợ. Cần khởi động lại máy chủ khi quản trị viên thay đổi thay đổi các dữ liệu lớn.

Chế độ phát triển (devmode) có thể rút ngắn thời gian xử lý từng công đoạn:

```text
/hld devmode status
/hld devmode on
/hld devmode off
```

## Kiểm tra sau khi thay đổi

Sau khi chỉnh sửa cấu hình, hãy chạy thử quá trình làm trái cây và quy trình ngũ cốc để kiểm tra hai nhánh quan trọng nhất: lên men trực tiếp và quy trình thông qua Nồi đun rồi mới lên men.
