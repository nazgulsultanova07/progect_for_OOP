import pandas as pd
import matplotlib.pyplot as plt
import os

# Настройка стиля графиков
plt.style.use('ggplot')
# Чтобы русские буквы отображались на графиках
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

# Создаем папку для картинок, если ее нет
os.makedirs('plots', exist_ok=True)

print("--- АНАЛИЗ ДАННЫХ ДЛЯ ПРОЕКТА ---\n")

# ==========================================
# 1. Анализ палитр (q1)
# ==========================================
q1 = pd.read_csv('raw/q1_palettes.csv')
fail_pct = (q1['wcag_level'] == 'fail').mean() * 100
aa_pct = (q1['wcag_level'] == 'AA').mean() * 100
aaa_pct = (q1['wcag_level'] == 'AAA').mean() * 100

print(f"1. ДОСТУПНОСТЬ ПАЛИТР: {fail_pct:.1f}% палитр не проходят стандарт WCAG (уровень fail).")

# График 1: Круговая диаграмма уровней WCAG
levels = q1['wcag_level'].value_counts()
plt.figure(figsize=(8, 5))
plt.pie(levels, labels=levels.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
plt.title('Распределение палитр по уровням доступности WCAG')
plt.savefig('plots/1_wcag_levels.png')
plt.close()

# ==========================================
# 2. Анализ опроса (q2)
# ==========================================
q2 = pd.read_csv('raw/q2_designers_survey.csv')
avg_time = q2['minutes_per_palette'].mean()
issue_pct = q2['faced_accessibility_issue'].mean() * 100
time_by_role = q2.groupby('role')['minutes_per_palette'].mean()

print(f"2. ОПРОС: В среднем на подбор палитры тратят {avg_time:.1f} мин. {issue_pct:.1f}% сталкивались с проблемой доступности.")

# График 2: Среднее время по ролям (Bar chart)
plt.figure(figsize=(8, 5))
time_by_role.plot(kind='bar', color='#4c72b0')
plt.title('Среднее время подбора палитры по ролям (мин)')
plt.ylabel('Минуты')
plt.xticks(rotation=0)
plt.savefig('plots/2_time_by_role.png')
plt.close()

# ==========================================
# 3. Анализ цветов на сайтах (q3)
# ==========================================
q3 = pd.read_csv('raw/q3_site_colors.csv')
fail_by_ind = q3.groupby('industry')['passes_aa'].apply(lambda x: (1 - x.mean()) * 100)

print(f"3. САЙТЫ: Больше всего недоступных цветов в индустрии: {fail_by_ind.idxmax()} ({fail_by_ind.max():.1f}% цветов).")

# График 3: Доля недоступных цветов по индустриям
plt.figure(figsize=(8, 5))
fail_by_ind.sort_values().plot(kind='barh', color='#c44e52')
plt.title('Доля цветов, не проходящих WCAG AA, по индустриям (%)')
plt.xlabel('Процент недоступных цветов')
plt.savefig('plots/3_fail_by_industry.png')
plt.close()

# ==========================================
# 4. Анализ трендов (q4)
# ==========================================
q4 = pd.read_csv('raw/q4_trends.csv')
q4['date'] = pd.to_datetime(q4['date'])
trend_growth = q4.pivot(index='date', columns='query', values='interest')

print(f"4. ТРЕНДЫ: Интерес к 'wcag' вырос с {trend_growth['wcag'].iloc[0]} до {trend_growth['wcag'].iloc[-1]} баллов.")

# График 4: Динамика интереса (Line chart)
plt.figure(figsize=(10, 5))
plt.plot(trend_growth.index, trend_growth['wcag'], label='WCAG (Доступность)', linewidth=2)
plt.plot(trend_growth.index, trend_growth['palette generator'], label='Генераторы палитр', linewidth=2, linestyle='--')
plt.title('Динамика поисковых запросов (2021-2024)')
plt.ylabel('Популярность (0-100)')
plt.legend()
plt.tight_layout()
plt.savefig('plots/4_trends.png')
plt.close()

print("\nГотово! Графики сохранены в папку 'plots/'.")