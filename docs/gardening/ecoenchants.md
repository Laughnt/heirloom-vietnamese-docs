# Tích hợp EcoEnchants

Heirloom đọc thông tin tích hợp phù phép từ `enchantment_integrations.json` và tìm đến các phù phép Bukkit đã được đăng ký bằng mã có dạng `namespace:key`.

## Các phù phép EcoEnchants được hỗ trợ sẵn

| Mục đích          | Mã                                             | Cách hoạt động                                                                         |
| ----------------- | ---------------------------------------------- | -------------------------------------------------------------------------------------- |
| Tự động trồng lại | `ecoenchants:replant`, `ecoenchants:replenish` | Cây trồng sẽ tự động mọc lại sau khi thu hoạch, kể cả khi bình thường cây sẽ bị phá bỏ |
| Tăng Fortune      | `ecoenchants:prospector`                       | Mỗi cấp phù phép sẽ cộng thêm 1 cấp Fortune khi tính số lượng vật phẩm nhận được       |

## Ảnh hưởng khi chơi

Các phù phép tự động trồng lại giúp việc trồng và thu hoạch cây thuận tiện hơn, nhưng vẫn tuân theo điều kiện của cây trồng, chẳng hạn như cây đã đủ lớn và có thể thu hoạch hay chưa. Phù phép tăng Fortune có thể làm tăng số lượng vật phẩm nhận được theo cấu hình của cây trồng. Nó không tự tạo thêm những vật phẩm mà cây trồng chưa được cấu hình để rơi ra.

## Lưu ý cho quản trị viên

Quản trị viên có thể thêm các phù phép khác bằng mã có cùng định dạng `namespace:name`. Sau khi chỉnh sửa, hãy tải lại cấu hình và thử thu hoạch một cây đã trưởng thành bằng công cụ có phù phép tương ứng để kiểm tra tích hợp hoạt động đúng.
