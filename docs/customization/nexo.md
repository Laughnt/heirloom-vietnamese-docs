# Tích hợp Nexo

Heirloom vẫn có thể khởi động bình thường nếu không cài Nexo.

## Mapping được khuyến nghị

Tạo các item Nexo có `visual ID` tương ứng với Heirloom. Quy ước đặt tên phổ biến thường là:

```text
heirloom_<visual_id_viết_thường>
```

Ví dụ:

```text
heirloom_tomato
heirloom_ice_cream_chorus
heirloom_espresso
```

## Kiểm tra

Khởi động máy chủ với Nexo đã được cài đặt, chạy `/hl reload`, sau đó tạo vật phẩm thông qua Heirloom thay vì tạo trực tiếp bằng Nexo.

Cách này giúp xác nhận Heirloom đang sử dụng Nexo để tạo vật phẩm, đồng thời các công thức và lệnh của Heirloom cũng đang sử dụng Nexo đúng cách.
