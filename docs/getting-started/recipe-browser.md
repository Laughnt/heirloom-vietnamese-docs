# Trình duyệt công thức

<figure class="hl-figure">
  <img src="../../images/showcase/recipe-browser.jpg" alt="Trình duyệt công thức là công cụ hướng dẫn chính trong trò chơi dành cho người chơi.">
  <figcaption>Trình duyệt công thức là công cụ hướng dẫn chính trong trò chơi dành cho người chơi.</figcaption>
</figure>

## Cách mở

```text
/hl
/hl recipes
/hl search pizza
```

`/hl` mở menu chính cho người chơi. `/hl search <từ khóa>` sẽ hiển thị kết quả đã lọc theo công thức, trạm, tiện ích, sản phẩm hoặc nguyên liệu.

## Ví dụ tìm kiếm

<div class="hl-media-grid">
  <figure class="hl-media-card"><img src="../../images/showcase/recipe-search-gui.webp" alt="Giao diện tìm kiếm công thức"><figcaption>Giao diện tìm kiếm công thức đã được lọc theo kết quả hữu ích.</figcaption></figure>
  <figure class="hl-media-card"><img src="../../images/showcase/recipe-search-chat.webp" alt="Kết quả tìm kiếm công thức trong thanh chat"><figcaption>Kết quả tìm kiếm công thức trong thanh chat giúp tra cứu công thức nhanh chóng.</figcaption></figure>
</div>

## Cách sử dụng

- Nhấp vào một công thức để xem nguyên liệu đầu vào và sản phẩm đầu ra.
- Nhấp vào nguyên liệu để truy ngược lại chuỗi công thức.
- Sử dụng trang "Cách dùng vật phẩm" để trả lời câu hỏi "Món này có thể nấu gì?"
- Các công thức từ tiện ích sẽ chỉ hiển thị khi tiện ích đó đã được cài đặt và đăng ký.

## Nếu thiếu công thức

- Đảm bảo tiện ích đã được cài đặt.
- Chạy `/hl reload` sau khi thay đổi tệp JSON.
- Kiểm tra nhật ký khởi động để xem cảnh báo xác thực công thức.
- Sử dụng `/hl debug test` để kiểm tra trạng thái đăng ký.
