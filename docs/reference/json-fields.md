# Tham chiếu các trường JSON

## Trường Vật phẩm tùy chỉnh

| Trường               | Ý nghĩa                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `id`                 | ID định danh của vật phẩm. Nên viết bằng chữ in hoa và giữ cố định để tránh làm hỏng các cấu hình đang sử dụng vật phẩm này.         |
| `name`               | Tên hiển thị của vật phẩm trong trò chơi.                                                                                            |
| `base_material`      | Loại vật phẩm Minecraft (vanilla) được dùng làm vật liệu nền cho vật phẩm tùy chỉnh.                                                   |
| `texture`            | Đường dẫn của đồ hoạ (đầu người chơi) được dùng để hiển thị vật phẩm.                                                                       |
| `edible`             | Xác định người chơi có thể ăn vật phẩm này hay không.                                                                                |
| `food_value`         | Lượng độ no mà người chơi được hồi phục khi ăn vật phẩm.                                                                         |
| `saturation`         | Lượng độ bão hòa được hồi phục khi ăn vật phẩm.                                                                                  |
| `consume_seconds`    | Số giây cần để người chơi ăn hoặc uống vật phẩm.                                                                                     |
| `animation`          | Hoạt ảnh được phát khi sử dụng vật phẩm, chẳng hạn `EAT` (ăn) hoặc `DRINK` (uống).                                                   |
| `effects`            | Danh sách các hiệu ứng thuốc được áp dụng cho người chơi khi sử dụng vật phẩm.                                                       |
| `visual_id`          | ID dùng để xác định hình ảnh hiển thị của vật phẩm. ID này không phụ thuộc vào plugin cung cấp hệ thống vật phẩm hoặc resource pack. |
| `consume_return`     | Vật phẩm được trả lại cho người chơi sau khi sử dụng vật phẩm hoặc hoàn thành công thức.                                             |
| `placeable_servings` | Số lượng phần có thể đặt xuống thế giới, chẳng hạn như các phần của một chiếc bánh.                                                  |
| `feast`              | Cho phép vật phẩm hoạt động như một món ăn chung, để nhiều người chơi có thể cùng sử dụng.                                           |

## Trường Công thức

| Trường             | Ý nghĩa                                                                                                                      |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| `id`               | ID định danh của công thức. Nên giữ cố định để các cấu hình khác có thể tham chiếu đến công thức này.                        |
| `station`          | Trạm hoặc khối được sử dụng để thực hiện công thức.                                                                          |
| `output`           | Vật phẩm chính được tạo ra sau khi công thức hoàn thành.                                                                     |
| `weighted_outputs` | Danh sách các vật phẩm có thể nhận được ngẫu nhiên. Mỗi vật phẩm có một **trọng số** riêng để quyết định khả năng xuất hiện. |
| `processing_time`  | Thời gian cần để hoàn thành công thức, tính bằng **tick** (1tick = 1/20 giây).                                                                   |
| `ingredients`      | Các nguyên liệu cần đưa vào công thức. Một số ô có thể là bắt buộc, trong khi một số ô có thể được để trống hoặc tùy chọn.   |
| `actions`          | Các thao tác luôn được thực hiện khi công thức hoàn thành, chẳng hạn như thay đổi vật phẩm đầu ra.                           |
| `rules`            | Các thay đổi chỉ được áp dụng khi một điều kiện cụ thể được đáp ứng.                                                         |

## Trường Cây trồng

| Trường       | Ý nghĩa                                                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| `id`         | ID định danh của cây trồng.                                                                                                    |
| `item_id`    | ID vật phẩm được sử dụng để trồng cây hoặc nhận được khi thu hoạch.                                                            |
| `plant_type` | Xác định cách cây trồng được đặt và hoạt động trong thế giới, chẳng hạn như cây thấp, cây cao, dây leo hoặc cây thủy sinh.     |
| `growth`     | Các thiết lập liên quan đến quá trình sinh trưởng, bao gồm thời gian phát triển, kích thước và số lượng giai đoạn sinh trưởng. |
| `planting`   | Xác định cây có thể được trồng trên loại khối nào và người chơi cần quyền gì để trồng.                                         |
| `textures`   | Các gói đồ hoạ được sử dụng để hiển thị cây ở từng giai đoạn sinh trưởng, từ lúc mới trồng cho đến khi trưởng thành.              |
| `harvest`    | Thiết lập cách thu hoạch cây, bao gồm vật phẩm nhận được, âm thanh, khả năng trồng lại và tỷ lệ chất lượng của nông sản.       |
