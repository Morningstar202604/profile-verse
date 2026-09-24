# Profile Verse · 主页宇宙

把你的 GitHub 主页的每一个部位，都换成一张更好看的卡。
一个仓库逛完全部组件，零服务器、零成本、每日自动刷新，视觉统一（深蓝 + 金 + 星空）。

差异化设计语言：**星空背景 + 金色点缀 + 每一张卡都有一个"一眼特征"**——数字骑星轨、连续天数是星轨环中央的亮星、文字在星空里自己打字。不做撞脸的统计条。

## 组件预览

![Impact Card](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/impact-card/preview/impact-card.svg)

![Stats Card](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/stats-card/preview/stats-card.svg)

![Streak Card](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/streak-card/preview/streak-card.svg)

![Typing Card](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/typing-card/preview/typing-card.svg)

![Contribution Grid Card](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/contrib-grid-card/preview/contrib-grid-card.svg)

![Tech Stack Card](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/tech-stack-card/preview/tech-stack-card.svg)

![Banner Card](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/banner-card/preview/banner-card.svg)

![Badge Card](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/badge-card/preview/badge-card.svg)

> 每张卡都有 **`dark`（深蓝星空）与 `light`（米白纸面）双主题**，加一行 `theme: light` 即可切换，浅色主页也能用。

## 为什么用 Profile Verse

- **零服务器、零成本**：GitHub Actions 定时生成 SVG，任何人一行 `<img>` 或 `uses:` 即可引用，不花钱、不绑卡
- **差异化**：统一的星空设计语言 + 每张卡一个"一眼特征"，和千篇一律的统计卡/贪吃蛇拉开距离
- **真实数据**：所有数字来自 GitHub API / 贡献日历，卡片标注数据来源与更新时间，不做假数据
- **一个入口逛全部**：所有组件收在一个仓库，视觉统一（`core/` 设计系统一处维护）
- **先合后拆**：组件独立爆红时，用 `git subtree split` 一键拆成独立仓库

## 组件

| 组件 | 说明 · 一眼特征 | 状态 | 用法 |
| --- | --- | --- | --- |
| [impact-card](components/impact-card/) | 已合并 PR × 仓库 star 影响力卡 · 分档金徽章 | 已发布 | `uses: .../components/impact-card@v1` |
| [stats-card](components/stats-card/) | 统计卡：关注/仓库/已合并 PR · 数字骑星轨 | 已发布 | `uses: .../components/stats-card@v1` |
| [streak-card](components/streak-card/) | 连续贡献卡 · 星轨环中央亮星 | 已发布 | `uses: .../components/streak-card@v1` |
| [typing-card](components/typing-card/) | 标语横幅 · 星空打字机 + 金色光标 | 已发布 | `uses: .../components/typing-card@v1` |
| [contrib-grid-card](components/contrib-grid-card/) | 3D 等距贡献柱 · 替换第三方 3D Action | 已发布 | `uses: .../components/contrib-grid-card@v1` |
| [tech-stack-card](components/tech-stack-card/) | 技术栈星座图 · 主语言是中央亮星 | 已发布 | `uses: .../components/tech-stack-card@v1` |
| [banner-card](components/banner-card/) | 星空全景头图 · 发光名字 + 流星 | 已发布 | `uses: .../components/banner-card@v1` |
| [badge-card](components/badge-card/) | 金色奖章徽章 · 替代 shields 平铺条 | 已发布 | `uses: .../components/badge-card@v1` |

> 主页替换进度：P1（外部服务）已替换——typing / streak / stats；P2（第三方 3D Action）已替换——contrib-grid-card；P3（自研资产沉淀）已完成——tech-stack / banner / badge。唯一保留的第三方项：浏览量计数（纯静态做不了实时计数）。

## 快速开始（以 impact-card 为例）

workflow 里接入（公开仓库 Actions 免费）：

```yaml
- uses: actions/checkout@v4
- name: Generate impact card
  uses: Morningstar202604/profile-verse/components/impact-card@v1
  with:
    users: your-github-username
    output: impact-card.svg
```

README 里一行引用：

```markdown
![Impact Card](https://cdn.jsdelivr.net/gh/你的用户名/你的仓库@main/impact-card.svg)
```

每个组件的完整用法见各自 README。

## 设计规范（差异化 + 不拥挤原则）

- **一眼特征**：每张卡一个独特形态（星轨 / 星环 / 打字机 / 3D 等距柱 / 星座 / 流星横幅 / 奖章），不做撞脸方案
- 单卡单主题，640 宽横版，大数字 + 少文字，留白优先
- 品牌色：深蓝 `#0B1026` + 金 `#C9A86A` + 星空点；**双主题**（`dark` / `light`）在 `core/theme.py` 一处维护
- 数据真实：统一走 `core/github.py`，全部卡每日自动刷新，卡片标注数据来源与更新时间

## 目录结构

```
profile-verse/
├── core/                     共享核心：GitHub API 层 · 贡献日历 · star 分档 · 星空主题
├── components/
│   ├── impact-card/          组件 = 生成脚本 + SVG 模板 + action.yml + README + preview
│   ├── stats-card/
│   ├── streak-card/
│   ├── typing-card/
│   ├── contrib-grid-card/
│   ├── tech-stack-card/
│   ├── banner-card/
│   └── badge-card/
├── .github/workflows/        本仓库自刷新示例
└── README.md                 组件目录页
```

## License

MIT © Morningstar202604
