## Tích hợp ItemsAdder

ItemsAdder là **soft dependency**. Heirloom sử dụng cùng đường dẫn logic `visual_id` cho ItemsAdder giống như với Nexo.

## Ánh xạ được khuyến nghị

Tạo các custom stack trong ItemsAdder tương ứng với những `visual_id` mà máy chủ của bạn muốn thay thế. Nên giữ ID ổn định để các recipe action như `SET_VISUAL_ITEM` không cần phải thay đổi.

## Quy tắc dự phòng

Nếu ItemsAdder không được cài đặt hoặc một item chưa được ánh xạ, item Heirloom thông thường vẫn được tạo. Hãy kiểm tra cơ chế dự phòng này trước khi đưa lên máy chủ chính để tránh việc người chơi bị chặn do lỗi cấu hình visual pack.
