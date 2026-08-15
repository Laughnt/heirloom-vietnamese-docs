# Cây trồng tùy chỉnh

Tệp JSON của cây trồng quy định loại cây, cách cây phát triển, điều kiện gieo trồng, hình ảnh hiển thị và vật phẩm nhận được khi thu hoạch.

## Cấu trúc tối thiểu

Một cây trồng bình thường cần có ID vật phẩm, loại cây, thiết lập sinh trưởng, quy tắc gieo trồng, hình ảnh sẽ hiển thị và quy tắc thu hoạch loại cây trồng đó. Khi quản trị viên chuẩn bị tạo cây trồng mới, nên lấy một cây có cơ chế gần với mong muốn làm mẫu: xà lách cho cây trồng trên mặt đất, cà chua cho cây dây leo, lúa cho cây trồng dưới nước và ngô cho cây thân cao.

## Các phần quan trọng

- `growth`: thời gian sinh trưởng, khả năng xuất hiện biến thể, các giai đoạn phát triển và kích thước sẽ hiển thị.
- `planting`: các khối có thể gieo trồng, vật phẩm trồng cây tiêu hao và quyền cần thiết cho việc trồng.
- `textures`: hình ảnh hiển thị trong quá trình sinh trưởng và khi cây đã trưởng thành.
- `harvest`: vật phẩm rơi ra, vật phẩm thưởng thêm, khả năng trồng lại, âm thanh phát ra và tỉ lệ nhận được nông sản chất lượng cao.

## Lựa chọn cách thiết kế

Hãy chọn loại cây dựa trên cách cây hoạt động và phát triển trong thế giới. Cây giống cà chua nên được thiết lập là dây leo vì cần có tường để phát triển. Cây giống lúa nên được thiết lập là cây trồng dưới nước vì yêu cầu về nước là một phần của cơ chế trồng trọt. Không nên dùng độ lệch hiển thị để “giả” một loại cây khác khi điều kiện đặt cây của nó không giống nhau.

## Những lỗi thường gặp

- Bật sinh cây tự nhiên cho cây dây leo, nhưng không có vị trí tường phù hợp để sinh trưởng.
- Cho người chơi cây trồng dưới nước, trong khi phải trên nước mới sống.
- Thêm vật phẩm thưởng với số lượng chịu ảnh hưởng bởi phù phép May mắn, nhưng sử dụng công cụ không có phù phép để kiểm tra nên chưa thể xác định chính xác số lượng vật phẩm được nhận.
- Quên cấp quyền trồng cây, khiến quản trị viên trồng được nhưng người chơi lại không thể.

## Cách kiểm tra

Gieo cây, chờ cây lớn hoặc tăng tốc quá trình sinh trưởng, rồi thu hoạch để kiểm tra vật phẩm nhận được. Sau đó, hãy thử trồng lại cây và kiểm tra trong khu vực được bảo vệ bằng một người chơi bình thường để chắc chắn mọi thứ đều hoạt động đúng.
