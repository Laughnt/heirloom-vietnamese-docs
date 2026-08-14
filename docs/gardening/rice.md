# Lúa

<figure class="hl-figure">
  <img src="../../images/gardening/rice.webp" alt="Cây lúa được trồng dưới nước, trên lớp đất bên dưới.">
  <figcaption>Cây lúa được trồng dưới nước, trên lớp đất bên dưới.</figcaption>
</figure>

| Trường dữ liệu | Giá trị |
| --- | --- |
| Vật phẩm | [`RICE`](../reference/items.md#item-rice) |
| Loại cây trồng | `AQUATIC` |
| Thời gian sinh trưởng cơ bản | 360 giây |
| Số giai đoạn sinh trưởng | 4 |
| Quyền cần có | `heirloom.crop.rice` |
| Trồng lại được | `Có` |

## Cách trồng

Lúa có thể được trồng trên các khối nền sau: `DIRT`, `CLAY`, `MUD`, `GRAVEL`, `SAND`.

Cách trồng: cầm vật phẩm cây giống và nhấp chuột phải vào một khối đất phù hợp. Nếu cây trồng yêu cầu một quyền cụ thể, người chơi phải có quyền đó trước khi có thể gieo trồng.

## Thu hoạch

Khi thu hoạch lúa, bạn sẽ nhận được từ 2 đến 4 hạt lúa (`RICE`).

Nếu bật `replant_after_harvest`, chỉ cần nhấp chuột phải vào cây đã trưởng thành là cây sẽ tự động quay về giai đoạn đầu, sẵn sàng cho vụ tiếp theo. Lưu ý rằng đập bỏ cây sẽ được coi là phá hủy hoàn toàn, không phải là thu hoạch hợp lệ.

## Lưu ý cho quản trị viên

Quản trị viên có thể chỉnh sửa cây trồng này trong `crops.json` hoặc tệp cấu hình của tiện ích liên quan. Mọi thông số như tốc độ tăng trưởng, số giai đoạn, khối đất hợp lệ, âm thanh, tỷ lệ rơi, tỷ lệ ra chất lượng và quyền cần thiết đều hoàn toàn có thể cấu hình được qua dữ liệu.