import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
print("Current directory:", os.getcwd())
print("Files in directory:", os.listdir("."))
print("Loading Delhi AQI data...")
df = pd.read_csv("city_day.csv")
# Clean & Filter for Delhi
df['Date'] = pd.to_datetime(df['Date'])
delhi = df[df['City'] == 'Delhi'].copy()
delhi = delhi[['Date', 'PM2.5', 'PM10', 'NO2', 'AQI', 'AQI_Bucket']].dropna(subset=[
                                                                            'AQI'])
delhi.set_index('Date', inplace=True)

print(f"Loaded {len(delhi)} days of Delhi AQI data.")

# Analysis
monthly_aqi = delhi['AQI'].resample('ME').mean()
yearly_aqi = delhi['AQI'].resample('YE').mean()

# Worst & Best Months
worst_month = monthly_aqi.idxmax().strftime('%B %Y')
best_month = monthly_aqi.idxmin().strftime('%B %Y')

#  Unhealthy Days
unhealthy = (delhi['AQI'] > 200).mean() * 100
very_unhealthy = (delhi['AQI'] > 300).mean() * 100

# Correlation
corr = delhi[['PM2.5', 'PM10', 'NO2', 'AQI']].corr()

# Print Insights
print("\n" + "="*50)
print("     DELHI AIR QUALITY INSIGHTS")
print("="*50)
print(f"• Total Days Analyzed: {len(delhi)}")
print(
    f"• Worst Month: {worst_month} (AQI: {monthly_aqi.max():.1f}) → Diwali + Stubble Burning")
print(f"• Best Month: {best_month} (AQI: {monthly_aqi.min():.1f}) → Monsoon")
print(f"• % Days AQI > 200 (Unhealthy): {unhealthy:.1f}%")
print(f"• % Days AQI > 300 (Hazardous): {very_unhealthy:.1f}%")
print(f"• PM2.5 → AQI Correlation: {corr.loc['PM2.5', 'AQI']:.2f}")

# Visualizations
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 12

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Delhi Air Quality Dashboard (2015–2020)',
             fontsize=18, fontweight='bold')

# Monthly AQI Trend
monthly_aqi.plot(ax=axes[0, 0], color='red', linewidth=2)
axes[0, 0].axhline(100, color='yellow', linestyle='--', label='Moderate')
axes[0, 0].axhline(200, color='orange', linestyle='--', label='Unhealthy')
axes[0, 0].axhline(300, color='red', linestyle='--', label='Hazardous')
axes[0, 0].set_title('Monthly Average AQI')
axes[0, 0].set_ylabel('AQI')
axes[0, 0].legend()
axes[0, 0].tick_params(axis='x', rotation=45)

# AQI by Year
delhi['Year'] = delhi.index.year
sns.boxplot(data=delhi, x='Year', y='AQI',
            ax=axes[0, 1], hue='Year', legend=False, palette='Reds')
axes[0, 1].set_title('AQI Distribution by Year')

# Correlation Heatmap
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=axes[1, 0])
axes[1, 0].set_title('Pollutant vs AQI Correlation')
# Unhealthy Days per Year
yearly_unhealthy = delhi.groupby('Year')['AQI'].apply(
    lambda x: (x > 200).mean() * 100)
yearly_unhealthy.plot(kind='bar', ax=axes[1, 1], color='orange')
axes[1, 1].set_title('% Days AQI > 200 (Unhealthy) by Year')
axes[1, 1].set_ylabel('% Days')
axes[1, 1].set_xlabel('Year')

plt.tight_layout()
plt.savefig('delhi_aqi_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()
