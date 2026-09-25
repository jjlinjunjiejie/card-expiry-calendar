# 银行卡到期提醒日历

这是一个可由 Apple 日历订阅的 iCalendar 日历。每张卡在到期月份前两个月的 1 日创建全天提醒：

- 日历标题：仅卡名
- 备注：卡名和到期时间
- 提醒时间：到期月份前两个月的 1 日

## 订阅

打开本项目的 GitHub Pages 页面，然后点击“订阅到 Apple 日历”。也可以在 Apple 日历中选择“文件 → 新建日历订阅”，粘贴页面显示的 HTTPS 订阅地址。

## 更新

编辑 `cards.json` 后运行：

```bash
python3 generate_calendar.py
```

提交更新后的 `cards.json` 和 `calendar.ics` 即可。已订阅设备会自动获取更新。
