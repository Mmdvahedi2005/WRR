# تمرین ۵ — همگام‌سازی WRR: DispatchGuard (Semaphore / Monitor / هر دو)

**زمان‌بندی déterministik WRR با Semaphore، Monitor و گاردهایادتر — 브اب trهッチو**

- **دوره:** سیستم‌عامل
- **تمرین:** ۵ — همگام‌سازی WRR
- **شاخه:** Exercise-5-WRR
- **منبع:** exercise5_wrr.py (حفاظت‌شده از شاخه main PR #1)
- **حالت‌ها:** semaphore, monitor, both
- **نتیجه:** makespan=12؛ تکمیل P1=۸, P2=۱۰, P3=۱۲؛ یکسان در همه حالت‌ها
- **تست‌ها:** ۹ تست واحد — همه پاس

---

## فهرست مطالب

1. معرفی
2. شکل‌ها
3. نتیجه‌گیری

---

## 1. معرفی

 WRR با سه حالت همگام‌سازی: semaphore، monitor و her دو. نتایج یکسان در همه حالت‌ها.

## 2. شکل‌ها

![شکل 1: FIGURE: Architectura DispatchGuard](docs/figures/dispatch_guard_architecture.svg)

*شکل 1 — FIGURE: Architectura DispatchGuard*

![شکل 2: FIGURE: جریان transync سه حالت](docs/figures/sync_variant_handover.svg)

*شکل 2 — FIGURE: جریان transync سه حالت*

![شکل 3: FIGURE: Gantt یکسان در سه حالت](docs/figures/wrr_gantt_equivalence.png)

*شکل 3 — FIGURE: Gantt یکسان در سه حالت*

![شکل 4: FIGURE: 브اب trهッチو برابر بودن متریک‌ها](docs/figures/sync_equivalence_chart.png)

*شکل 4 — FIGURE: 브اب trهッチو برابر بودن متریک‌ها*

**جدول 1 — جدول — برابری در سه حالت**

| حالت | makespan | P1 wait | P2 wait | P3 wait |
| --- | --- | --- | --- | --- |
| semaphore | ۱۲ | ۳ | ۶ | ۹ |
| monitor | ۱۲ | ۳ | ۶ | ۹ |
| both | ۱۲ | ۳ | ۶ | ۹ |

## 3. نتیجه‌گیری

سه حالت semaphore، monitor و both نتایج یکسان می‌دهند.
