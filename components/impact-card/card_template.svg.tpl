<svg xmlns="http://www.w3.org/2000/svg" width="640" height="$HEIGHT" viewBox="0 0 640 $HEIGHT" role="img" aria-label="Open Source Impact Card — $USER">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="$BG_TOP"/>
      <stop offset="1" stop-color="$BG_BOTTOM"/>
    </linearGradient>
  </defs>
  <rect width="640" height="$HEIGHT" rx="16" fill="url(#bg)" stroke="$LINE" stroke-width="1.5"/>

  <text x="30" y="40" font-family="'Segoe UI',Helvetica,Arial,'PingFang SC','Microsoft YaHei',sans-serif" font-size="15" font-weight="700" letter-spacing="2.5" fill="$GOLD_BRIGHT">OPEN SOURCE IMPACT</text>
  <text x="610" y="40" text-anchor="end" font-family="'Segoe UI',Helvetica,Arial,'PingFang SC','Microsoft YaHei',sans-serif" font-size="11" fill="$SUB">更新于 $DATE</text>
  <text x="30" y="66" font-family="'Segoe UI',Helvetica,Arial,'PingFang SC','Microsoft YaHei',sans-serif" font-size="17" font-weight="600" fill="$TEXT">$USER</text>
  <text x="610" y="66" text-anchor="end" font-family="'Segoe UI',Helvetica,Arial,'PingFang SC','Microsoft YaHei',sans-serif" font-size="11" fill="$SUB">GitHub · 已合并 PR</text>
  <line x1="30" y1="82" x2="610" y2="82" stroke="$LINE" stroke-width="1"/>

  <rect x="30" y="96" width="180" height="78" rx="10" fill="$PANEL" stroke="$LINE"/>
  <text x="120" y="140" text-anchor="middle" font-family="'Segoe UI',Helvetica,Arial,sans-serif" font-size="26" font-weight="700" fill="$GOLD">$PR_COUNT</text>
  <text x="120" y="161" text-anchor="middle" font-family="'PingFang SC','Microsoft YaHei','Segoe UI',sans-serif" font-size="11.5" fill="$MUTED">合并 PR</text>

  <rect x="230" y="96" width="180" height="78" rx="10" fill="$PANEL" stroke="$LINE"/>
  <text x="320" y="140" text-anchor="middle" font-family="'Segoe UI',Helvetica,Arial,sans-serif" font-size="26" font-weight="700" fill="$GOLD">$REPO_COUNT</text>
  <text x="320" y="161" text-anchor="middle" font-family="'PingFang SC','Microsoft YaHei','Segoe UI',sans-serif" font-size="11.5" fill="$MUTED">贡献仓库</text>

  <rect x="430" y="96" width="180" height="78" rx="10" fill="$PANEL" stroke="$LINE"/>
  <text x="520" y="140" text-anchor="middle" font-family="'Segoe UI',Helvetica,Arial,sans-serif" font-size="23" font-weight="700" fill="$GOLD">$IMPACT</text>
  <text x="520" y="161" text-anchor="middle" font-family="'PingFang SC','Microsoft YaHei','Segoe UI',sans-serif" font-size="11.5" fill="$MUTED">影响力分 · Σ 仓库 star</text>

  <text x="30" y="210" font-family="'PingFang SC','Microsoft YaHei','Segoe UI',sans-serif" font-size="12.5" font-weight="600" letter-spacing="1" fill="$GOLD">贡献分档 · 按仓库 star</text>
  $TIER_BOXES

  <text x="30" y="300" font-family="'PingFang SC','Microsoft YaHei','Segoe UI',sans-serif" font-size="12.5" font-weight="600" letter-spacing="1" fill="$GOLD">TOP 贡献仓库</text>
  $TOP_ROWS
  $RECENT_LINE

  <text x="30" y="$FOOTER_Y" font-family="'PingFang SC','Microsoft YaHei','Segoe UI',sans-serif" font-size="10.5" fill="$DIM">数据来源 GitHub API · 每日自动刷新 · 零服务器自动生成</text>
  <text x="610" y="$FOOTER_Y" text-anchor="end" font-family="'Segoe UI',Helvetica,Arial,sans-serif" font-size="10.5" fill="$DIM">impact-card</text>
</svg>
