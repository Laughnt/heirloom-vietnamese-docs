# Hành động và Quy tắc Công thức
<!-- Note: I will keep many technical terms in their original form in this section to preserve their meaning and avoid confusing translations. -->

Các hành động công thức thay đổi đầu ra sau khi một công thức khớp.

| Hành động | Mục đích |
| --- | --- |
| `SET_PROPERTY` | Đặt metadata như tên hiển thị hoặc `food_property` |
| `ADD_QUALITY` | Thêm chất lượng vào đầu ra |
| `SET_QUALITY` | Đặt chất lượng đầu ra |
| `SET_TEXTURE` | Thay đổi texture đầu người chơi; các bảng công thức wiki dựa trên mã nguồn hiển thị các biến thể đầu ra riêng biệt khi quy tắc đặt texture khác nhau |
| `SET_VISUAL_ITEM` | Đổi đầu ra sang vật phẩm hiển thị trung lập với nhà cung cấp |
| `SET_RETURN_ITEM` | Trả lại vật chứa như `BUCKET` |
| `SET_CONSUME_RETURN` | Lưu trữ metadata trả lại để tiêu thụ/sử dụng sau |

Các `trigger` - điều kiện phổ biến bao gồm `HAS_INPUT`, `HAS_ANY_INGREDIENT`, `HAS_ALL_INGREDIENTS`, `HAS_INGREDIENT_PROPERTY`, `HAS_ALL_INGREDIENT_PROPERTIES`, và `INPUT_COUNT_GTE`.
