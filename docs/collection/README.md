# 微信全年文章完整性规程

目标窗口为 2025-11-01 至 2026-11-01（含边界）。截图只能证明关注关系，搜索结果只能发现候选文章；二者都不能证明历史目录无遗漏。

## 何时才算完成一个账号

1. 在微信账号主页核验名称、头像/主体线索，保存非敏感的文字证据，不上传私人聊天或整屏截图。
2. 从官方历史页或发布者导出逐次枚举推送，越过 2025-11-01 后再检查一页，确认下边界；同时检查 2026-11-01 上边界。
3. 每次推送记录日期、推送标识、卡片总数及证据；主条和“余下 N 篇”全部展开，位置从 1 连续编号。
4. 每篇记录标题、日期、原文 URL、正文阅读证据、图表是否检查、检查时间。付费、删除、仅摘要或正文打不开都记作阻塞，不能算已读。
5. 目录总数只有在历史边界闭合后才可计算；否则必须为 `null`，不能把当前发现数当总数。

`scripts/audit_coverage.py` 只检查证据字段和内部一致性，不能自行证明页面或人工阅读真实发生。当前可见“与数据同行”主页及文章卡片，但桌面控制点击返回 `noWindowsAvailable`，因此仍未完成目录枚举。

## 运行

```bash
python3 scripts/audit_coverage.py \
  --accounts sources/collection-accounts.json \
  --articles sources/collection-articles.json \
  --output reports/collection-coverage.json \
  --markdown-output reports/collection-coverage.md

# CI/交付门禁：当前预期退出 1，直到 36 个账号全部闭合并读完
python3 scripts/audit_coverage.py \
  --accounts sources/collection-accounts.json \
  --articles sources/collection-articles.json \
  --require-complete
```

仓库只保存目录元数据、原创摘要、链接与必要短引文，不保存公众号全文、私人聊天、账号凭据或企业资料。
