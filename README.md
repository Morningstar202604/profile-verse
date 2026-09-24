# Profile Verse · 主页宇宙

把你的 GitHub 主页的每一个部位，都换成一张更好看的卡。
一个仓库逛完全部组件，零服务器、零成本、每日自动刷新，视觉统一（深蓝 + 金）。

![Impact Card](https://cdn.jsdelivr.net/gh/Morningstar202604/profile-verse@main/components/impact-card/preview/impact-card.svg)

## 为什么用 Profile Verse

- **零服务器、零成本**：GitHub Actions 定时生成 SVG，任何人一行 `<img>` 或 `uses:` 即可引用，不花钱、不绑卡
- **一个入口逛全部**：所有组件收在一个仓库，别人看一次 README 就能挑走想要的卡
- **视觉统一**：所有卡共用 `core/` 设计系统（品牌色 / 字体 / star 分档 / GitHub API 层）
- **先合后拆**：组件独立爆红时，用 `git subtree split` 一键拆成独立仓库，引用地址换仓名即可

## 组件

| 组件 | 说明 | 状态 | 用法 |
| --- | --- | --- | --- |
| [impact-card](components/impact-card/) | 已合并 PR × 仓库 star 影响力卡 | 已发布 | `uses: Morningstar202604/profile-verse/components/impact-card@v1` |
| typing-card | 打字机标语卡（SVG 内置动画） | 规划中 | — |
| streak-card | 连续贡献天数卡 | 规划中 | — |
| stats-card | 星标 / 关注 / 仓库统计卡 | 规划中 | — |
| tech-stack-card | 技术栈图卡 | 规划中 | — |
| contrib-grid-card | 贡献热力图卡（替换 3D/蛇形图） | 规划中 | — |
| banner-card | 主页头图 / 尾图 | 规划中 | — |

> 主页替换路线图与每个部位的做法见仓库讨论区 / 各组件 README。

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

完整用法见 [components/impact-card/README.md](components/impact-card/README.md)。

## 设计规范（不拥挤原则）

- 单卡单主题：一张卡只讲一件事，不做大杂烩
- 640 宽横版，信息密度低，大数字 + 少文字，留白优先
- 品牌色：深蓝 `#0B1026` + 金 `#C9A86A`，主题在 `core/theme.py` 一处维护
- 数据来源统一走 `core/github.py`，全部卡每日自动刷新

## 目录结构

```
profile-verse/
├── core/                     共享核心：GitHub API 层 · star 分档 · 主题
├── components/
│   └── impact-card/          组件 = 生成脚本 + SVG 模板 + action.yml + README
├── .github/workflows/        本仓库自刷新示例
└── README.md                 组件目录页
```

## License

MIT © Morningstar202604
