# Tệp ngôn ngữ

Heirloom đi kèm với nhiều tệp ngôn ngữ khác nhau. Bạn có thể chọn ngôn ngữ đang sử dụng trong `config.yml`.

```yml
locale: en
```

Các lệnh hữu ích:

```text
/hl lang list
/hl lang missing <locale>
```

Khi muốn tạo bản dịch riêng, hãy sao chép `lang/en.yml`, giữ nguyên toàn bộ key và chỉ dịch phần **value**. Sau đó chạy `/hl reload` để áp dụng bản dịch mới.
