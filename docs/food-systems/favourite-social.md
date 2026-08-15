# Phần thưởng cho món yêu thích và người chế biến

Thông tin về món ăn yêu thích và người chế biến được lưu riêng cho từng người chơi. Những thông tin này không ảnh hưởng đến việc Heirloom xác định công thức, nhưng có thể kết hợp với các thuộc tính của món ăn khi người chơi ăn chúng.

## Món ăn yêu thích

Người chơi có thể chọn món ăn yêu thích bằng lệnh `/hl favourite`. Khi ăn món ăn tùy chỉnh đã chọn làm món yêu thích, người chơi sẽ nhận được:

| Hiệu ứng | Thời gian | Cấp độ |
| -------- | --------- | ------ |
| Hồi phục | 30 giây   | I      |
| Bão hòa  | 15 giây   | II     |
| May mắn  | 60 giây   | I      |

Heirloom sẽ kiểm tra món ăn yêu thích sau khi áp dụng các hiệu ứng từ thuộc tính của món ăn. Vì vậy, nếu một món ăn vừa là món yêu thích vừa có các thuộc tính tạo hiệu ứng, người chơi sẽ nhận được cả hai hiệu ứng.

## Người chế biến

Khi người chơi chế tạo một món ăn có thể ăn được, Heirloom lưu lại thông tin về người đã chế biến món đó. Sau này, nếu một người chơi khác ăn món ăn yêu thích do người đó chế biến, người chế biến có thể nhận được hiệu ứng hồi phục trong thời gian ngắn.

## Mối liên kết

`AFFINITY` cũng sử dụng thông tin về người đã chế biến món ăn. Nếu món ăn được chế biến bởi người khác, người ăn sẽ nhận được hiệu ứng hồi phục. Nếu món ăn đó đồng thời là món yêu thích của người ăn, cấp độ của hiệu ứng hồi phục sẽ được tăng lên.

## Lưu dữ liệu

Dữ liệu RPG của người chơi được lưu trong `plugins/Heirloom/playerdata/`. Lựa chọn món ăn yêu thích và cấp độ thành thạo của mỗi người chơi được lưu riêng.
