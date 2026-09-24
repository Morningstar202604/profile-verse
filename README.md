# Profile Verse · 主页宇宙

把你的 GitHub 主页的每一个部位，都换成一张更好看的卡。
一个仓库逛完全部组件，零服务器、零成本、每日自动刷新，视觉统一（深蓝 + 金 + 星空）。

差异化设计语言：**星空背景 + 金色点缀 + 每一张卡都有一个"一眼特征"**——数字骑星轨、连续天数是星轨环中央的亮星、文字在星空里自己打字、贡献是立体的金色柱子。不做撞脸的统计条，也不做满大街的贪吃蛇。

> ✅ **已经在用**：[Morningstar202604 主页](https://github.com/Morningstar202604/Morningstar202604) 的 typing / stats / streak / 3D 贡献 / tech-stack / badges / impact 七个部位，已全部换成 Profile Verse 卡片，由主页自己的 workflow 每日刷新。

## 组件展示厅 · 8 卡 × 双主题

每张卡都有 **`dark`（深蓝星空）与 `light`（米白纸面）** 两个主题，浅色主页也能用。
展示厅里每张卡先给深色版，再给浅色版，用法都写在卡下面。

### 1 · impact-card — 开源影响力卡

你的已合并 PR 到底有多值钱？把 PR 和仓库 star 绑定，分档金色徽章（S≥50k★ 到 D<100★），一眼看出贡献进了多牛的仓库。主页的"含金量"担当。

![Impact dark](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/impact-card/preview/impact-card.svg)

![Impact light](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/impact-card/preview/impact-card-light.svg)

```yaml
- uses: Morningstar202604/profile-verse/components/impact-card@v1
  with:
    users: your-github-username          # 支持多账号聚合：a,b
    output: impact-card.svg
    theme: dark                          # 或 light
```

### 2 · stats-card — 统计卡

关注 / 公开仓库 / 已合并 PR 三个数字，骑着金色星轨。大数字 + 少文字，拒绝密密麻麻的统计条。

![Stats dark](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/stats-card/preview/stats-card.svg)

![Stats light](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/stats-card/preview/stats-card-light.svg)

```yaml
- uses: Morningstar202604/profile-verse/components/stats-card@v1
  with:
    user: your-github-username
    output: stats-card.svg
```

### 3 · streak-card — 连续贡献卡

当前连续天数 = 星轨环中央的亮星，环外 12 颗星点，下方两枚星章（最长连续 / 全年贡献）。数据来自真实贡献日历，今天还没贡献会从昨天起算，不虚报。

![Streak dark](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/streak-card/preview/streak-card.svg)

![Streak light](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/streak-card/preview/streak-card-light.svg)

```yaml
- uses: Morningstar202604/profile-verse/components/streak-card@v1
  with:
    user: your-github-username
    output: streak-card.svg
```

### 4 · typing-card — 星空打字机

一句话在星空里自己打出来，金色闪烁光标。纯 SVG + SMIL，不需要任何外部服务。

![Typing dark](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/typing-card/preview/typing-card.svg)

![Typing light](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/typing-card/preview/typing-card-light.svg)

```yaml
- uses: Morningstar202604/profile-verse/components/typing-card@v1
  with:
    phrases: "第一句话;第二句话;Third phrase"   # 最多 3 条
    output: typing-card.svg
```

### 5 · contrib-grid-card — 3D 贡献柱

第三方 3D 贡献图的国产替代：等距投影的立体金色柱子（顶面亮 / 右面中 / 左面暗三面着色），五档金色分级，53 周全年日历。这就是主页上"一眼差异"的那张卡。

![Contrib dark](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/contrib-grid-card/preview/contrib-grid-card.svg)

![Contrib light](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/contrib-grid-card/preview/contrib-grid-card-light.svg)

```yaml
- uses: Morningstar202604/profile-verse/components/contrib-grid-card@v1
  with:
    user: your-github-username
    output: contrib-grid-card.svg
```

### 6 · tech-stack-card — 技术栈星座

主语言是中央亮星，其余语言沿椭圆环绕、虚线连成星座。数据来自你的真实仓库主语言统计。

![Tech dark](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/tech-stack-card/preview/tech-stack-card.svg)

![Tech light](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/tech-stack-card/preview/tech-stack-card-light.svg)

```yaml
- uses: Morningstar202604/profile-verse/components/tech-stack-card@v1
  with:
    user: your-github-username
    output: tech-stack-card.svg
```

### 7 · banner-card — 星空全景头图

发光名字 + 渐变字 + 流星轨迹，纯视觉，不需要 API。主页最上面那一横条。

![Banner dark](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/banner-card/preview/banner-card.svg)

![Banner light](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/banner-card/preview/banner-card-light.svg)

```yaml
- uses: Morningstar202604/profile-verse/components/banner-card@v1
  with:
    name: your-name
    output: banner-card.svg
```

### 8 · badge-card — 金色奖章

一排金色奖章徽章（渐变金边 + 星形图标），替代 shields 平铺条。默认自动取真实数据，也可以完全自定义。

![Badge dark](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/badge-card/preview/badge-card.svg)

![Badge light](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/badge-card/preview/badge-card-light.svg)

```yaml
- uses: Morningstar202604/profile-verse/components/badge-card@v1
  with:
    user: your-github-username
    output: badge-card.svg
    # badges: "PRs=12;Stars=256.9k;Repos=19"   # 可选：完全自定义
```

## 为什么用 Profile Verse

- **零服务器、零成本**：GitHub Actions 定时生成 SVG，任何人一行 `<img>` 或 `uses:` 即可引用，不花钱、不绑卡
- **差异化**：统一的星空设计语言 + 每张卡一个"一眼特征"，和千篇一律的统计卡/贪吃蛇拉开距离
- **真实数据**：所有数字来自 GitHub API / 贡献日历，卡片标注数据来源与更新时间，不做假数据
- **一个入口逛全部**：所有组件收在一个仓库，视觉统一（`core/` 设计系统一处维护）
- **先合后拆**：组件独立爆红时，用 `git subtree split` 一键拆成独立仓库

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
