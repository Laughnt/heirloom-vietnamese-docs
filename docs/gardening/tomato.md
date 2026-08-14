# Cà chua

<figure class="hl-figure">
  <img src="../../images/gardening/tomato.webp" alt="Cây cà chua phát triển theo dạng dây leo.">
  <figcaption>Cây cà chua phát triển theo dạng dây leo.</figcaption>
</figure>

| Trường dữ liệu | Giá trị |
| --- | --- |
| Vật phẩm | [`TOMATO`](../reference/items.md#item-tomato) |
| Loại cây trồng | `VINE` |
| Thời gian sinh trưởng cơ bản | 420 giây |
| Số giai đoạn sinh trưởng | 4 |
| Quyền cần có | `heirloom.crop.tomato` |
| Trồng lại được | `Có` |

## Cách trồng

Cà chua có thể được trồng trên các khối được định nghĩa trong tệp cấu hình cây trồng (xem `crops.json`).

Để trồng, cầm vật phẩm cây giống và nhấp chuột phải vào khối đất phù hợp. Nếu cây trồng yêu cầu quyền cụ thể, người chơi phải có quyền trồng loại cây đó, trước khi tiến hành gieo trồng.

## Thu hoạch

Khi thu hoạch cà chua, người chơi sẽ nhận được từ 1 đến 2 quả cà chua (`TOMATO`).

Nếu bật `replant_after_harvest`, chỉ cần nhấp chuột phải vào cây đã trưởng thành để thu hoạch, cây sẽ tự động quay về giai đoạn đầu. Lưu ý rằng hành động phá bỏ cây được xem là phá hủy hoàn toàn, không phải một vụ thu hoạch hợp lệ.

## Lưu ý cho quản trị viên

Quản trị viên có thể chỉnh sửa cây trồng này trong `crops.json` hoặc tệp cấu hình của tiện ích liên quan. Tốc độ sinh trưởng, số giai đoạn, các khối cho phép trồng, âm thanh, tỷ lệ rơi, tỷ lệ ra chất lượng và quyền yêu cầu đều được thiết lập hoàn toàn qua dữ liệu cấu hình.
