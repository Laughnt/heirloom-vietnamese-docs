# Món ăn yêu thích

Tính năng món ăn yêu thích là một tính năng RPG cá nhân. Người chơi liên tục chọn ăn một món ăn tùy chỉnh, và nhận thêm hiệu ứng mỗi khi ăn món đó.

## Lệnh

```text
/hl favourite
```

Lệnh viết tắt:

```text
/hl favorite
/hl fav
```

## Hiệu ứng nhận được

Khi ăn món ăn yêu thích, người chơi sẽ nhận được các hiệu ứng sau:

| Hiệu ứng | Thời gian | Cường độ |
| --- | --- | --- |
| Hồi phục | 30 giây | I |
| Bão hòa | 15 giây | II |
| May mắn | 60 giây | I |

Những hiệu ứng này được cộng thêm sau khi các hiệu ứng từ thuộc tính thực phẩm thông thường đã được áp dụng. Nếu món yêu thích của bạn cũng là món có nhiều thuộc tính chồng chất, cả hai hệ thống sẽ cùng hoạt động.

## Tại sao điều này quan trọng

Một món yêu thích đơn thuần đã hữu ích. Nhưng một món yêu thích có thừa hưởng nhiều thuộc tính sẽ mạnh hơn rất nhiều. Ví dụ: bánh kếp làm từ mứt `GOLDEN` và `CHORUS` có thể kích hoạt hiệu ứng từ các thuộc tính đó, rồi sau đó cộng thêm gói hiệu ứng dành cho món yêu thích nếu bánh kếp được chọn là món yêu thích của bạn.

## Nấu ăn xã hội

Heirloom lưu dữ liệu "được nấu bởi" trên món ăn thành phẩm. Nếu một người chơi khác nấu món yêu thích của bạn, hệ thống sẽ thưởng cho người nấu một hiệu ứng hồi phục ngắn. Thuộc tính `AFFINITY` cũng sẽ đọc dữ liệu "được nấu bởi" và trở nên mạnh hơn nếu món ăn đó cũng là món yêu thích của bạn (x2 niềm vui).

## Lưu ý dành cho người chơi

Nếu lệnh `/hl favourite` không khả dụng, hãy hỏi quản trị viên xem quyền `heirloom.favourite` đã được cấp chưa. Tính năng này yêu cầu quyền, vì vậy quản trị viên có thể quyết định xem nó có nằm trong quyền hạn mặc định cho người chơi hay không.