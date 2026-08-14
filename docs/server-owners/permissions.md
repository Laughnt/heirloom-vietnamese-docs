# Phân quyền

Trên máy chủ thực tế, nên sử dụng plugin quản lý quyền như **LuckPerms** để kiểm soát quyền truy cập của người chơi.

Xem [Tham chiếu Quyền](../reference/permissions.md) để biết đầy đủ danh sách quyền.

Các quyền cơ bản nên cấp cho nhóm người chơi mặc định:

```text
/lp group default permission set heirloom.use true
/lp group default permission set heirloom.recipes true
/lp group default permission set heirloom.cookbook true
/lp group default permission set heirloom.advancements true
/lp group default permission set heirloom.favourite true
/lp group default permission set heirloom.mastery true
```

Nếu quản trị viên vẫn bật các quyền trồng cây đi kèm Heirloom, hãy cấp thêm quyền tương ứng cho từng loại cây trồng.
