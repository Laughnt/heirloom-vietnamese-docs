# Công thức tùy chỉnh

Công thức xác định hệ thống chế biến, thành phẩm, thời gian chế biến, nguyên liệu, thao tác và các quy tắc tùy chọn. Thành phẩm có thể được thay đổi thông qua các thao tác cơ bản, thao tác theo quy tắc, thông tin kế thừa từ nguyên liệu và cơ chế chất lượng.

## Công thức tối thiểu

```json
{
  "id": "SWEET_PANCAKES",
  "station": "FRYING_PAN",
  "output": "PANCAKES",
  "processing_time": 160,
  "ingredients": [
    { "type": "REQUIRED", "max": 1, "options": [{ "custom_item": "BAG_OF_FLOUR" }] },
    { "type": "REQUIRED", "max": 1, "options": [{ "item": "EGG" }] },
    { "type": "OPTIONAL", "max": 1, "options": [{ "item": "HONEY_BOTTLE" }] }
  ],
  "actions": [
    { "type": "SET_PROPERTY", "key": "NAME", "value": "Sweet Pancakes" },
    { "type": "ADD_METADATA", "key": "food_property", "value": "SWEET" }
  ]
}
```

## Nâng cao: Kế thừa thuộc tính qua nhiều bước

Đặt thuộc tính cho nguyên liệu trung gian nếu muốn người chơi tạo ra món ăn có nhiều thuộc tính thông qua nhiều công đoạn chế biến. Ví dụ, mứt có thể nhận thuộc tính `CHORUS` từ quả chorus. Khi dùng loại mứt này làm lớp phủ cho bánh, bánh sẽ kế thừa thuộc tính đó.

## Các thao tác theo quy tắc thường dùng

- `SET_PROPERTY` với khóa `NAME`: thay đổi tên hiển thị của vật phẩm.
- `ADD_METADATA` với khóa `food_property`: thêm thuộc tính thực phẩm để có thể được kế thừa và áp dụng khi ăn.
- `SET_RETURN_ITEM`: trả lại vật chứa sau khi chế biến xong.
- `SET_CONSUME_RETURN`: trả lại vật chứa sau khi ăn.
- `SET_VISUAL_ITEM`: chuyển sang một biến thể hình ảnh không phụ thuộc vào nền tảng cung cấp hình ảnh.
- `ADD_QUALITY` và `SET_QUALITY`: điều chỉnh chất lượng thành phẩm.

## Những lỗi thường gặp

- Dùng `SET_PROPERTY` cho `food_property`; các công thức có sẵn dùng `ADD_METADATA` để thêm thuộc tính thực phẩm có thể được kế thừa.
- Đặt vật phẩm tùy chỉnh vào `item` thay vì `custom_item`.
- Quên rằng ô nguyên liệu tùy chọn mặc định có thể nhận từ `0` đến `max`, vì vậy quy tắc cần xử lý cả trường hợp không có nguyên liệu.
- Chỉnh sửa JSON nhưng chỉ kiểm tra bằng `/hl give`; các thao tác của công thức và cơ chế kế thừa chỉ xuất hiện khi thực sự chế biến theo công thức.

## Cách kiểm tra

Chạy `/hl reload`, tìm công thức cần kiểm tra, chế biến tất cả các trường hợp đã thay đổi và kiểm tra phần mô tả vật phẩm. Khi kiểm tra cơ chế kế thừa, hãy chế biến nguyên liệu trung gian trước, sau đó dùng chính vật phẩm đó trong công thức tiếp theo.
