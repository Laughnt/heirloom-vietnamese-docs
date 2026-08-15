## Tích hợp ItemsAdder

ItemsAdder là một phần phụ thuộc tùy chọn. Heirloom sử dụng cùng đường dẫn logic `visual_id` cho ItemsAdder như với Nexo.

## Ánh xạ được khuyến nghị

Tạo các vật phẩm tùy chỉnh trong ItemsAdder tương ứng với những `visual_id` mà máy chủ của bạn muốn thay thế. Nên giữ nguyên các ID để những hành động công thức như `SET_VISUAL_ITEM` không cần phải thay đổi.
Tạo các custom stack trong ItemsAdder tương ứng với những `visual_id` mà máy chủ của bạn muốn thay thế. Nên giữ ID ổn định để các recipe action như `SET_VISUAL_ITEM` không cần phải thay đổi.

## Quy tắc dự phòng

Nếu ItemsAdder chưa được cài đặt hoặc một vật phẩm chưa được ánh xạ, Heirloom vẫn sẽ tạo vật phẩm mặc định. Hãy kiểm tra cơ chế dự phòng này trước khi triển khai lên máy chủ chính để tránh người chơi bị chặn do cấu hình gói hiển thị không chính xác.
