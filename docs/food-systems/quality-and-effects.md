# Chất lượng và hiệu ứng

Chất lượng được lưu trên thực phẩm và nguyên liệu tùy chỉnh. Một số loại cây trồng có thể giữ lại và cải thiện chất lượng qua mỗi lần trồng, trong khi công thức có thể đặt giá trị chất lượng hoặc tăng thêm chất lượng. Hệ thống tinh thông nấu ăn cũng có thể giúp nâng cao chất lượng của món ăn trong những lần chế biến tiếp theo.

## Chất lượng được lấy từ đâu

- `SET_QUALITY` đặt một mức chất lượng cụ thể cho món ăn được tạo ra.
- `ADD_QUALITY` tăng thêm chất lượng hiện tại khi công thức đáp ứng điều kiện tương ứng.
- Nếu công thức không đặt chất lượng cụ thể, thực phẩm tùy chỉnh được chế tạo thủ công có thể lấy mức chất lượng cao nhất từ các nguyên liệu được sử dụng.
- Hệ thống Tinh thông nấu ăn sẽ cộng thêm một lượng chất lượng riêng cho từng công thức trong những lần chế biến tiếp theo.
- Cây trồng có thể lưu lại chất lượng và giữ nguyên chất lượng đó khi được trồng lại.

## Hiệu ứng được lấy từ đâu

Khi người chơi ăn một món ăn, các hiệu ứng của món đó có thể đến từ:

- Lượng thức ăn và độ bão hòa mà món ăn cung cấp.
- Các thuộc tính thực phẩm được lưu trong `food_property`.
- Danh sách `effects` trong tệp JSON.
- Hiệu ứng dành cho món ăn yêu thích.
- Hiệu ứng dành cho người đã chế biến món ăn khi món đó được nấu bởi người khác.
- Tính năng giảm say của hệ thống ủ rượu nếu món ăn có thuộc tính `SOBERING`.

## Kiểm tra khi cần cân bằng

Nếu một món ăn cho hiệu ứng quá yếu, trước tiên hãy kiểm tra xem công thức có thực sự thêm thuộc tính hoặc hiệu ứng cần thiết hay không. Nếu món ăn quá mạnh, hãy kiểm tra các nguyên liệu mà nó kế thừa, vì một nguyên liệu trung gian có thể đã mang theo thuộc tính hoặc hiệu ứng và khiến chúng tiếp tục được truyền sang nhiều công thức khác.

Các món ăn được chế tạo nên tuân theo đúng những giá trị đã được cấu hình. Nếu một món ăn cần có khả năng hồi máu, tăng độ bão hòa hoặc nhận thêm hiệu ứng thuốc, hãy khai báo rõ các hiệu ứng đó trong tệp JSON.
