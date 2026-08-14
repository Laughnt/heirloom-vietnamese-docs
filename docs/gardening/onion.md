# Hành tây

<figure class="hl-figure">
  <img src="../../images/gardening/onion.webp" alt="Cây hành tây được trồng theo kiểu Allium sát mặt đất.">
  <figcaption>Cây hành tây được trồng theo kiểu Allium sát mặt đất.</figcaption>
</figure>

| Trường dữ liệu | Giá trị |
| --- | --- |
| Vật phẩm | [`ONION`](../reference/items.md#item-onion) |
| Loại cây trồng | `ALLIUM` |
| Thời gian sinh trưởng cơ bản | 360 giây |
| Số giai đoạn sinh trưởng | 4 |
| Quyền cần có | `heirloom.crop.onion` |
| Trồng lại được | `Có` |

## Cách trồng

Hành tây có thể được trồng trên các khối đất sau: `GRASS_BLOCK`, `DIRT`, `COARSE_DIRT`, `PODZOL`, `ROOTED_DIRT`.

Để trồng, bạn chỉ cần cầm vật phẩm cây giống và nhấp chuột phải vào khối đất phù hợp. Nếu cây trồng yêu cầu một quyền cụ thể, người chơi phải có quyền đó trước khi có thể trồng.

## Thu hoạch

Khi thu hoạch hành tây, bạn sẽ nhận được từ 1 đến 3 củ hành (`ONION`).

Nếu tính năng `replant_after_harvest` được bật, chỉ cần nhấp chuột phải vào cây đã trưởng thành để thu hoạch, cây sẽ tự động quay về giai đoạn phát triển ban đầu. Lưu ý rằng việc đập bỏ cây sẽ bị coi là phá hủy hoàn toàn chứ không phải một vụ thu hoạch hợp lệ.

## Lưu ý cho quản trị viên

Quản trị viên có thể chỉnh sửa cây trồng này trong `crops.json` hoặc tệp cấu hình cây trồng của tiện ích liên quan. Các thông số như tốc độ tăng trưởng, số giai đoạn, khối đất hợp lệ, âm thanh, tỷ lệ rơi vật phẩm, tỷ lệ ra chất lượng và quyền cần thiết đều hoàn toàn có thể cấu hình được qua dữ liệu.