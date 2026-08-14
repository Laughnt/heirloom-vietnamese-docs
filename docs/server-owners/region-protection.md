# Bảo vệ khu vực

Heirloom có cơ chế tương thích với các plugin bảo vệ khu vực theo hai lớp kiểm tra, giúp các thao tác trồng trọt và sử dụng trạm nấu ăn tuân theo quyền của khu vực.

## WorldGuard

- Khi người chơi sử dụng trạm nấu ăn, Heirloom kiểm tra quyền `INTERACT` của WorldGuard để xác định người chơi có được phép tương tác tại khu vực đó hay không.
- Khi người chơi trồng hoặc thu hoạch cây, Heirloom kiểm tra quyền `BUILD` của WorldGuard để đảm bảo khu vực cho phép thay đổi khối.

## Các plugin Claim khác

Khi người chơi trồng cây, Heirloom sẽ tạo một `BlockPlaceEvent` giống như một thao tác đặt khối thông thường.

Tương tự, khi thu hoạch cây, Heirloom sẽ tạo một `BlockBreakEvent` như khi người chơi phá khối.

Nhờ vậy, các plugin bảo vệ và claim (chiếm dụng khu vực) như Towny, GriefPrevention, Lands cùng các plugin tương tự vẫn có thể bắt và xử lý các sự kiện này theo cơ chế thông thường. Nếu khu vực không cho phép thao tác, plugin bảo vệ có thể hủy sự kiện thao tác để ngăn hành động người chơi vừa làm.

## Kiểm tra trước khi đưa máy chủ vào hoạt động

Trước khi mở máy chủ cho người chơi, hãy vào một khu vực đã được bảo vệ và kiểm tra đầy đủ các thao tác sau:

- Trồng cây.
- Thu hoạch cây.
- Sử dụng trạm nấu ăn.
- Phá trạm nấu ăn khi bên trong vẫn còn nguyên liệu.

Các thao tác trên nên được kiểm tra bằng cả người chơi **có quyền** và không có quyền, nhằm đảm bảo hệ thống bảo vệ khu vực đang chặn đúng những hành động cần thiết.
