# Ngô

<figure class="hl-figure">
  <img src="../../images/gardening/corn.webp" alt="Cánh đồng ngô với những cây ngô cao lớn.">
  <figcaption>Cánh đồng ngô với những cây ngô cao lớn.</figcaption>
</figure>

| Trường dữ liệu | Giá trị |
| --- | --- |
| Vật phẩm | [`CORN`](../reference/items.md#item-corn) |
| Loại cây trồng | `TALL_PLANT` |
| Thời gian sinh trưởng cơ bản | 480 giây |
| Số giai đoạn sinh trưởng | 5 |
| Quyền | `heirloom.crop.corn` |
| Có thể trồng lại | `yes` |

## Cách trồng

Có thể trồng trên các khối: `GRASS_BLOCK`, `DIRT`, `COARSE_DIRT`, `PODZOL`, `ROOTED_DIRT`. Sử dụng vật phẩm hạt giống của cây trồng lên đúng khối hoặc bề mặt để bắt đầu trồng. Nếu cây trồng yêu cầu quyền, người chơi phải có quyền tương ứng mới có thể trồng.

## Thu hoạch

Vật phẩm nhận được khi thu hoạch: `CORN` 1-2. Nếu cây trồng có thuộc tính `replant_after_harvest`, người chơi có thể nhấp chuột phải để thu hoạch và cây sẽ trở lại giai đoạn phát triển đầu tiên. Ngược lại, phá cây được xem là phá bỏ cây trồng chứ không phải thu hoạch.

## Lưu ý cho quản trị viên

Quản trị viên có thể chỉnh sửa cây trồng này trong `crops.json` hoặc tệp cấu hình cây trồng của tiện ích tương ứng. Thời gian sinh trưởng, số giai đoạn, các khối có thể trồng, âm thanh, tỷ lệ rơi vật phẩm, tỷ lệ chất lượng và quyền cần thiết đều có thể được điều chỉnh thông qua cấu hình.
