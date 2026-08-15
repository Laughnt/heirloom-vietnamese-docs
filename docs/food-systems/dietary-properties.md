# Thuộc tính dinh dưỡng

Các nhãn dinh dưỡng hoạt động theo kiểu “chỉ cần có một nguyên liệu không phù hợp là món ăn sẽ không còn đạt thuộc tính đó”. Nếu tất cả nguyên liệu đều phù hợp, món ăn sẽ được xem là đáp ứng thuộc tính.

| Thuộc tính    | Tên hiển thị      | Ý nghĩa                                                       | Bao gồm      |
| ------------- | ----------------- | ------------------------------------------------------------- | ------------ |
| `VEGAN`       | Thuần chay        | Không sử dụng bất kỳ nguyên liệu nào có nguồn gốc từ động vật | `VEGETARIAN` |
| `VEGETARIAN`  | Ăn chay           | Không sử dụng thịt hoặc cá                                    |              |
| `GLUTEN_FREE` | Không chứa gluten | Không chứa gluten                                             |              |

## Cách Heirloom kiểm tra

Khi quản trị viên xem trước hoặc chế tạo một công thức, Heirloom sẽ kiểm tra toàn bộ nguyên liệu được sử dụng. Với các nguyên liệu có sẵn trong Minecraft, Heirloom sẽ đối chiếu chúng với cấu hình thuộc tính dinh dưỡng. Với các nguyên liệu tùy chỉnh, Heirloom có thể lưu lại thông tin dinh dưỡng ngay từ khi chúng được tạo ra. Nhờ vậy, các công thức sử dụng những nguyên liệu này về sau vẫn có thể biết được đặc tính dinh dưỡng của chúng mà không cần kiểm tra lại các nguyên liệu ban đầu.

## Ví dụ về việc kế thừa thông tin

Ví dụ, quản trị viên tạo một loại sốt tùy chỉnh từ sữa. Sau đó, loại sốt này được dùng để làm bánh mì kẹp. Mặc dù công thức bánh mì kẹp chỉ nhìn thấy nguyên liệu `SAUCE`, Heirloom vẫn biết rằng `SAUCE` được làm từ sữa. Vì vậy, bánh mì kẹp sẽ không được đánh dấu là thuần chay. Thông tin dinh dưỡng đã lưu sẽ đi theo nguyên liệu và được sử dụng cho các công thức tiếp theo.

## Ví dụ: Thêm khái niệm dinh dưỡng "Halal" hoặc "Kosher"
<!-- Note: I’m not fully familiar with the concepts of Kosher and Halal in this context, so I’m not certain how to translate this section accurately. Could you please briefly clarify what these terms mean here and how they are intended to be used in the system? -->

Quản trị viên có thể tự thêm các quy tắc dinh dưỡng riêng cho máy chủ, giống như cách tệp mặc định đã thiết lập `VEGAN`, `VEGETARIAN` và `GLUTEN_FREE`. Mỗi thuộc tính sẽ xác định những nguyên liệu nào được phép sử dụng. Danh sách `violators` sẽ xác định những nguyên liệu nào khiến món ăn không còn đáp ứng thuộc tính đó. Ví dụ, quy tắc Halal đơn giản có thể không cho phép thịt heo và các món tùy chỉnh làm từ thịt heo:

```json
"HALAL": {
  "display_name": "Halal",
  "description": "Không chứa các nguyên liệu không Halal do máy chủ quy định",
  "violators": {
    "items": [
      "PORKCHOP",
      "COOKED_PORKCHOP"
    ],
    "custom_items": [
      "BACON",
      "CHRISTMAS_HAM"
    ]
  }
}
```

Quy tắc "Kosher" cũng có thể được thiết lập theo cách tương tự:

```json
"KOSHER": {
  "display_name": "Kosher",
  "description": "Không chứa các nguyên liệu không Kosher do máy chủ quy định",
  "violators": {
    "items": [
      "PORKCHOP",
      "COOKED_PORKCHOP"
    ],
    "custom_items": [
      "BACON",
      "CHRISTMAS_HAM"
    ]
  }
}
```

Sau khi thêm các quy tắc này vào `dietary_properties`, hãy tải lại cấu hình máy chủ và thử một vài công thức để kiểm tra. Ví dụ, nếu thịt xông khói được làm từ thịt heo, thì thịt xông khói đó sẽ không được xem là phù hợp với Halal hoặc Kosher. Nếu thịt xông khói tiếp tục được dùng để làm món trứng với thịt xông khói, bánh mì kẹp thịt hoặc các món ăn tùy chỉnh khác, món ăn được tạo ra cũng sẽ không được xem là phù hợp với Halal hoặc Kosher. Điều này là do nguyên liệu tùy chỉnh vẫn ghi nhớ thông tin về những nguyên liệu đã được dùng để tạo ra nó.

!!! note
Heirloom chỉ thực hiện đúng những quy tắc mà quản trị viên đã thiết lập. Heirloom không tự quyết định món ăn nào được xem là hợp lệ theo quy định tôn giáo ngoài đời thực. Nếu máy chủ không cho phép đồ ăn dạng rượu, động vật có vú, món ăn kết hợp thịt với sữa hoặc một số loại đồ uống từ tiện ích bổ sung, hãy thêm ID của các vật phẩm đó vào danh sách `violators` tương ứng. Sau đó, nhớ kiểm tra các chuỗi công thức mà người chơi có thể sử dụng để bảo đảm kết quả đúng với quy định của máy chủ.

## Thứ tự thuộc tính

`hierarchy_rules` giúp Heirloom tự động ẩn những nhãn không cần thiết khi món ăn đã có một nhãn phù hợp hơn. Ví dụ, món ăn `VEGAN` cũng đồng thời đáp ứng điều kiện của `VEGETARIAN`, nên Heirloom chỉ cần hiển thị nhãn “Thuần chay” thay vì hiển thị cả “Thuần chay” và “Ăn chay”.

## Dòng "Có chứa"

Khối `contains_settings` dùng để thiết lập dòng “Có chứa:” trong phần mô tả của vật phẩm. Nên sử dụng mục này để hiển thị những thông tin người chơi cần biết, chẳng hạn như chất gây dị ứng, quy định riêng của máy chủ hoặc các hạn chế trong hệ thống nhập vai. Không nên chỉ sử dụng mục này để trang trí hoặc quảng bá món ăn.
