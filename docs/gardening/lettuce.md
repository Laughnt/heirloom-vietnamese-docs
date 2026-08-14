# Xà lách

<figure class="hl-figure">
  <img src="../../images/gardening/lettuce.webp" alt="Cây xà lách được trồng sát mặt đất.">
  <figcaption>Cây xà lách được trồng sát mặt đất.</figcaption>
</figure>

| Trường dữ liệu | Giá trị |
| --- | --- |
| Vật phẩm | [`LETTUCE`](../reference/items.md#item-lettuce) |
| Loại cây trồng | `SHORT_PLANT` |
| Thời gian sinh trưởng cơ bản | 300 giây |
| Số giai đoạn sinh trưởng | 4 |
| Quyền cần có | `heirloom.crop.lettuce` |
| Trồng lại được | `Có` |

## Cách trồng

Xà lách có thể được trồng trên các khối đất sau: `GRASS_BLOCK`, `DIRT`, `COARSE_DIRT`, `PODZOL`, `ROOTED_DIRT`.

Cách trồng rất đơn giản: chỉ cần cầm vật phẩm cây giống và nhấp chuột phải vào một khối đất phù hợp. Nếu cây trồng yêu cầu một quyền cụ thể, người chơi phải có quyền đó trước khi có thể gieo trồng.

## Thu hoạch

Khi thu hoạch xà lách, bạn sẽ nhận được từ 1 đến 3 củ xà lách (`LETTUCE`).

Nếu tính năng `replant_after_harvest` được bật, bạn chỉ cần nhấp chuột phải vào cây đã trưởng thành để thu hoạch, và cây sẽ tự động quay trở về giai đoạn phát triển ban đầu. Lưu ý rằng việc đập bỏ cây sẽ bị coi là phá hủy hoàn toàn, không phải là một vụ thu hoạch hợp lệ.

## Lưu ý cho quản trị viên

Để điều chỉnh các thông số cho cây xà lách, quản trị viên có thể sửa trực tiếp trong tệp `crops.json` hoặc tệp cấu hình của tiện ích liên quan. Mọi thông số như tốc độ tăng trưởng, số giai đoạn, khối đất hợp lệ, âm thanh, tỷ lệ rơi vật phẩm, tỷ lệ ra chất lượng và quyền cần thiết đều hoàn toàn có thể cấu hình được qua dữ liệu.