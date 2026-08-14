# Thực phẩm tùy chỉnh

Thực phẩm tùy chỉnh được khai báo trong các mảng `custom_items` của tệp JSON. Phần thực phẩm tùy chỉnh xác định vật phẩm mà người chơi có thể cầm và sử dụng; còn công thức quy định cách chế biến ra vật phẩm đó.

## Cấu trúc tối thiểu của thực phẩm có thể ăn

```json
{
  "id": "GOLDEN_PANCAKE",
  "name": "Golden Pancake",
  "base_material": "PLAYER_HEAD",
  "texture": "http://textures.minecraft.net/texture/...",
  "edible": true,
  "food_value": 8,
  "saturation": 6.0,
  "consume_seconds": 1.4,
  "animation": "EAT",
  "visual_id": "GOLDEN_PANCAKE"
}
```

## Các trường nâng cao cần biết

- `consume_return`: trả lại một vật phẩm sau khi ăn.
- `placeable_servings`: cho phép đặt món ăn xuống và dùng thành nhiều phần.
- `feast`: bật cơ chế yến tiệc dùng chung.
- `effects`: áp dụng các hiệu ứng thuốc được chỉ định khi ăn.
- `visual_id`: cho phép Nexo hoặc ItemsAdder thay đổi hình ảnh hiển thị mà không cần thay đổi công thức.

## Những lỗi thường gặp

- Khai báo vật phẩm nhưng hông tạo công thức để chế biến ra vật phẩm đó.
- Đặt `name` hiển thị đẹp mắt, nhưng quên `id` viết hoa ổn định được sử dụng trong công thức.
- Mong muốn món ăn có hiệu ứng từ một thuộc tính ngẫu nhiên, nhưng lại chưa thêm thao tác công thức hoặc thuộc tính được lưu tương ứng.
- Dùng ID hình ảnh dành riêng cho Nexo hoặc ItemsAdder thay vì ID hình ảnh chung được Heirloom sử dụng.

## Cách kiểm tra

Dùng `/hl give <id>` để kiểm tra vật phẩm đã khai báo, sau đó chế biến vật phẩm bằng công thức tương ứng để kiểm tra chất lượng, thuộc tính và các vật phẩm được trả lại.
