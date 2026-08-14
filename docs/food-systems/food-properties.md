# Thuộc tính thực phẩm

Thuộc tính thực phẩm là những đặc tính được lưu trực tiếp trên vật phẩm và có thể ảnh hưởng đến cách món ăn hoạt động trong trò chơi. Khi người chơi ăn món ăn đó, Heirloom sẽ kiểm tra từng thuộc tính đã được lưu và áp dụng hiệu ứng tương ứng.

## Thuộc tính được thêm từ đâu

Thuộc tính có thể được thêm vào thông qua một hành động trong công thức, thường là `ADD_METADATA` với khóa `food_property`, hoặc được kế thừa từ nguyên liệu. Khi một công thức hoàn thành, Heirloom sẽ giữ lại các thuộc tính vốn đã có trên vật phẩm đầu ra, sau đó lấy thêm tất cả thuộc tính của những nguyên liệu được sử dụng. Toàn bộ thông tin này sẽ được lưu vào vật phẩm thành phẩm và hiển thị trong phần mô tả.

Nhờ vậy, thuộc tính thực phẩm có thể tiếp tục được truyền từ nguyên liệu này sang nguyên liệu khác qua nhiều công thức khác nhau.

## Ví dụ: Bánh kếp siêu cấp

1. Dùng `CHORUS_FRUIT` để làm mứt trong Nồi đun. Công thức làm mứt sẽ thêm thuộc tính `CHORUS`.
2. Dùng `GOLDEN_APPLE` để làm một hũ mứt khác. Công thức làm mứt sẽ thêm thuộc tính `GOLDEN`.
3. Dùng những loại mứt này làm lớp phủ cho bánh kếp trong Chảo chiên. Bánh kếp sẽ kế thừa tất cả thuộc tính đã được lưu trong phần mứt.
4. Khi ăn bánh kếp, Heirloom sẽ áp dụng toàn bộ thuộc tính thực phẩm đã được lưu trên bánh, sau đó áp dụng các hiệu ứng được thiết lập trong tệp JSON và cuối cùng là hiệu ứng của món ăn yêu thích nếu bánh kếp là món ăn yêu thích của người chơi.

Trong dữ liệu có sẵn, phần mật ong dùng cho bánh kếp sẽ lưu tên loại mật ong, chất lượng và cách trả lại chai. Tuy nhiên, mật ong sẽ không tự thêm `SWEET` vào bánh kếp, trừ khi công thức hoặc vật phẩm tùy chỉnh lưu rõ `SWEET` dưới dạng thuộc tính thực phẩm. Quản trị viên có thể thêm hiệu ứng này thông qua các hành động trong công thức.

## Hiệu ứng của từng thuộc tính

| Thuộc tính | Hiệu ứng khi ăn |
| --- | --- |
| `GLOWING` | Nhận hiệu ứng Phát sáng I trong 30 giây, kèm âm thanh và thông báo giống hiệu ứng từ đèn hiệu |
| `GOLDEN` | Nhận hiệu ứng Hồi phục II trong 5 giây và Hấp thụ I trong 2 phút |
| `CHORUS` | Tìm cách dịch chuyển người chơi đến một vị trí ngẫu nhiên an toàn, tương tự hiệu ứng của Quả Chorus |
| `SWEET` | Nhận hiệu ứng Tốc độ I và Haste I trong 10 giây |
| `SPICY` | Nhận hiệu ứng Kháng lửa I trong 20 giây và thêm 1 giây hiệu ứng lửa giả |
| `COLD` | Nhận hiệu ứng Chậm I trong 5 giây và Kháng II trong 10 giây |
| `ENERGIZING` | Nhận hiệu ứng Tốc độ II, Haste II và Nhảy cao I trong 30 giây |
| `NOURISHING` | Nhận hiệu ứng Bão hòa III trong 5 giây |
| `HEALING` | Hồi ngay 2 đơn vị máu bằng hiệu ứng Hồi máu tức thời II |
| `AFFINITY` | Nếu món ăn được người chơi khác chế biến, nhận hiệu ứng Hồi phục I trong 10 giây. Nếu đó cũng là món ăn yêu thích của người ăn, nhận Hồi phục II |
| `SOBERING` | Nếu hệ thống ủ rượu được tải và tính năng say đang được bật, mức độ say sẽ được giảm theo giá trị đã cấu hình, mặc định là 15 |

## Người chơi sẽ thấy gì

Trong trình duyệt công thức, người chơi có thể xem trước các thuộc tính thực phẩm mà món ăn sẽ nhận được dựa trên những nguyên liệu đã chọn. Món ăn sau khi chế tạo cũng sẽ giữ lại các thuộc tính này và hiển thị chúng trong phần mô tả.

Nếu món ăn được đặt xuống dưới dạng thức ăn phục vụ, các thuộc tính cũng sẽ được lưu trên khối đó. Vì vậy, khi người chơi lấy thức ăn từ đó và ăn, các hiệu ứng tương ứng vẫn được áp dụng như bình thường.

## Hướng dẫn dành cho quản trị viên

Quản trị viên có thể sử dụng thuộc tính thực phẩm để tạo ra các chuỗi hiệu ứng theo từng bước. Ví dụ, si-rô cây phong có thể được thiết lập để nhận `SWEET`. Khi dùng si-rô này cùng với mứt có thuộc tính `GOLDEN` để làm bánh kếp, bánh kếp sẽ kế thừa cả thuộc tính từ mứt lẫn thuộc tính từ si-rô.

```json
{
  "type": "ADD_METADATA",
  "key": "food_property",
  "value": "SWEET"
}
````

Không nên mặc định rằng các hiệu ứng đã được cân bằng sẵn sẽ luôn phù hợp với cách máy chủ vận hành. Nếu một món ăn cần có khả năng hồi máu, giảm say, dịch chuyển, tăng cường sức mạnh hoặc được tính là món ăn yêu thích, hãy cấu hình rõ các hiệu ứng đó trong dữ liệu của công thức hoặc nguyên liệu.
