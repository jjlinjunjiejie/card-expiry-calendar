# 银行卡到期提醒日历

这是一个可由 Apple 日历订阅的 iCalendar 日历。每张卡在到期月份前两个月的 3 日创建全天提醒：

- 日历标题：仅卡名
- 备注：卡名和到期时间
- 提醒时间：到期月份前两个月的 3 日
- 自动归档：有效期结束满一个月后，从订阅日历移除，但在下方清单中保留并添加删除线

## 订阅

打开 [GitHub Pages 订阅页面](https://jjlinjunjiejie.github.io/card-expiry-calendar/)，然后点击“订阅到 Apple 日历”。也可以在 Apple 日历中选择“文件 → 新建日历订阅”，粘贴页面显示的 HTTPS 订阅地址。

## 银行卡状态

<!-- CARD_STATUS_START -->
_自动状态日期：2026-09-25_

<table>
  <thead>
    <tr><th>类别</th><th>银行卡</th><th>到期时间</th><th>状态</th></tr>
  </thead>
  <tbody>
    <tr><td rowspan="12">信用卡</td><td>MUFG 信用卡</td><td>2027 年 12 月</td><td>有效</td></tr>
    <tr><td>乐天信用卡</td><td>2028 年 9 月</td><td>有效</td></tr>
    <tr><td>建行全球付信用卡</td><td>2029 年 2 月</td><td>有效</td></tr>
    <tr><td>JCB信用卡</td><td>2029 年 5 月</td><td>有效</td></tr>
    <tr><td>建行哔哩哔哩信用卡</td><td>2030 年 1 月</td><td>有效</td></tr>
    <tr><td>建行 Muse 信用卡</td><td>2030 年 7 月</td><td>有效</td></tr>
    <tr><td>ViewCard</td><td>2030 年 10 月</td><td>有效</td></tr>
    <tr><td>中国银行招财猫 信用卡</td><td>2030 年 12 月</td><td>有效</td></tr>
    <tr><td>HSBC Visa Signature 信用卡</td><td>2031 年 9 月</td><td>有效</td></tr>
    <tr><td>中银香港万事达卡</td><td>2032 年 10 月</td><td>有效</td></tr>
    <tr><td>HSBC Pulse信用卡</td><td>2033 年 7 月</td><td>有效</td></tr>
    <tr><td>HSBC 万事达卡</td><td>2035 年 7 月</td><td>有效</td></tr>
    <tr><td rowspan="4">提款卡</td><td>Schwab 提款卡</td><td>2027 年 2 月</td><td>有效</td></tr>
    <tr><td>Wise提款卡</td><td>2028 年 11 月</td><td>有效</td></tr>
    <tr><td>中银香港 提款卡</td><td>2032 年 7 月</td><td>有效</td></tr>
    <tr><td>HSBC 卓越提款卡</td><td>2035 年 9 月</td><td>有效</td></tr>
    <tr><td rowspan="7">储蓄卡</td><td>上海银行储蓄卡</td><td>2029 年 7 月</td><td>有效</td></tr>
    <tr><td>广发银行储蓄卡</td><td>2031 年 11 月</td><td>有效</td></tr>
    <tr><td>光大银行储蓄卡</td><td>2031 年 12 月</td><td>有效</td></tr>
    <tr><td>兴业银行储蓄卡</td><td>2032 年 3 月</td><td>有效</td></tr>
    <tr><td>中信银行储蓄卡</td><td>2034 年 1 月</td><td>有效</td></tr>
    <tr><td>招商银行储蓄卡</td><td>2034 年 3 月</td><td>有效</td></tr>
    <tr><td>建设银行储蓄卡</td><td>2035 年 1 月</td><td>有效</td></tr>
  </tbody>
</table>
<!-- CARD_STATUS_END -->

## 更新

编辑 `cards.json` 后运行：

```bash
python3 generate_calendar.py
```

修改卡片的 `year` 和 `month` 后提交即可。年份统一使用四位数，生成器会始终按 `YYYY 年 M 月` 输出。GitHub Actions 会重新生成日历与本页状态；已订阅设备会自动获取更新。

系统每月 1 日自动检查。银行卡在到期月份结束后继续保留一个完整月，从再下一个月的 1 日起归档。例如有效期为 2027 年 2 月，会在 2027 年 4 月 1 日从订阅日历移除并在上方显示删除线。
