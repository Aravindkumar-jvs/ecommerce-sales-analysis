import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  E-Commerce Sales Analysis — SQL + Python")
print("=" * 60)

df = pd.read_csv("ecommerce_orders.csv")
print(f"\nDataset loaded: {len(df)} orders | {df['Customer_ID'].nunique()} customers\n")

conn = sqlite3.connect(":memory:")
df.to_sql("orders", conn, index=False, if_exists="replace")

print("=" * 60)
print("ANALYSIS 1: Revenue by Category")
print("=" * 60)
q1 = """
SELECT Category,
       COUNT(*) as Total_Orders,
       ROUND(SUM(Revenue), 2) as Total_Revenue,
       ROUND(AVG(Revenue), 2) as Avg_Order_Value,
       ROUND(AVG(Customer_Rating), 2) as Avg_Rating
FROM orders
WHERE Order_Status = 'Delivered'
GROUP BY Category
ORDER BY Total_Revenue DESC
"""
df_q1 = pd.read_sql(q1, conn)
print(df_q1.to_string(index=False))

print("\n" + "=" * 60)
print("ANALYSIS 2: Top 5 Cities by Revenue")
print("=" * 60)
q2 = """
SELECT City,
       COUNT(DISTINCT Customer_ID) as Unique_Customers,
       COUNT(*) as Total_Orders,
       ROUND(SUM(Revenue), 2) as Total_Revenue
FROM orders
GROUP BY City
ORDER BY Total_Revenue DESC
LIMIT 5
"""
df_q2 = pd.read_sql(q2, conn)
print(df_q2.to_string(index=False))

print("\n" + "=" * 60)
print("ANALYSIS 3: Monthly Revenue Trend")
print("=" * 60)
q3 = """
SELECT Year, Month, Quarter,
       COUNT(*) as Orders,
       ROUND(SUM(Revenue), 2) as Revenue
FROM orders
WHERE Order_Status = 'Delivered'
GROUP BY Year, Month
ORDER BY Year, Month
"""
df_q3 = pd.read_sql(q3, conn)
print(df_q3.to_string(index=False))

print("\n" + "=" * 60)
print("ANALYSIS 4: Payment Method Preference")
print("=" * 60)
q4 = """
SELECT Payment_Method,
       COUNT(*) as Usage_Count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders), 1) as Usage_Pct,
       ROUND(SUM(Revenue), 2) as Total_Revenue
FROM orders
GROUP BY Payment_Method
ORDER BY Usage_Count DESC
"""
df_q4 = pd.read_sql(q4, conn)
print(df_q4.to_string(index=False))

print("\n" + "=" * 60)
print("ANALYSIS 5: Customer Segmentation by Order Value")
print("=" * 60)
q5 = """
SELECT Customer_ID,
       COUNT(*) as Orders,
       ROUND(SUM(Revenue), 2) as Total_Spend,
       ROUND(AVG(Revenue), 2) as Avg_Order_Value,
       CASE
           WHEN SUM(Revenue) > 50000 THEN 'High Value'
           WHEN SUM(Revenue) > 20000 THEN 'Mid Value'
           ELSE 'Low Value'
       END as Segment
FROM orders
WHERE Order_Status = 'Delivered'
GROUP BY Customer_ID
ORDER BY Total_Spend DESC
LIMIT 10
"""
df_q5 = pd.read_sql(q5, conn)
print(df_q5.to_string(index=False))

print("\n" + "=" * 60)
print("ANALYSIS 6: Return & Cancellation Rate by Category")
print("=" * 60)
q6 = """
SELECT Category,
       COUNT(*) as Total_Orders,
       SUM(CASE WHEN Order_Status='Returned' THEN 1 ELSE 0 END) as Returns,
       SUM(CASE WHEN Order_Status='Cancelled' THEN 1 ELSE 0 END) as Cancellations,
       ROUND(SUM(CASE WHEN Order_Status='Returned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as Return_Rate_Pct
FROM orders
GROUP BY Category
ORDER BY Return_Rate_Pct DESC
"""
df_q6 = pd.read_sql(q6, conn)
print(df_q6.to_string(index=False))

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("E-Commerce Sales Dashboard", fontsize=16, fontweight='bold', y=0.98)

ax1 = axes[0, 0]
colors = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4', '#FF5722', '#795548']
bars = ax1.barh(df_q1['Category'], df_q1['Total_Revenue'], color=colors)
ax1.set_xlabel('Total Revenue (₹)', fontsize=10)
ax1.set_title('Revenue by Category', fontweight='bold')
for bar, val in zip(bars, df_q1['Total_Revenue']):
    ax1.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
             f'₹{val:,.0f}', va='center', fontsize=8)
ax1.invert_yaxis()

ax2 = axes[0, 1]
ax2.pie(df_q4['Usage_Count'], labels=df_q4['Payment_Method'],
        autopct='%1.1f%%', colors=['#FF6384','#36A2EB','#FFCE56','#4BC0C0','#9966FF','#FF9F40'],
        startangle=90)
ax2.set_title('Payment Method Distribution', fontweight='bold')

ax3 = axes[1, 0]
df_q3['Period'] = df_q3['Year'].astype(str) + '-' + df_q3['Month'].astype(str).str.zfill(2)
ax3.plot(range(len(df_q3)), df_q3['Revenue'], marker='o', color='#2196F3', linewidth=2, markersize=4)
ax3.fill_between(range(len(df_q3)), df_q3['Revenue'], alpha=0.15, color='#2196F3')
ax3.set_title('Monthly Revenue Trend', fontweight='bold')
ax3.set_xlabel('Month')
ax3.set_ylabel('Revenue (₹)')
tick_positions = list(range(0, len(df_q3), 3))
ax3.set_xticks(tick_positions)
ax3.set_xticklabels([df_q3['Period'].iloc[i] for i in tick_positions], rotation=45, fontsize=7)

ax4 = axes[1, 1]
ax4.barh(df_q2['City'], df_q2['Total_Revenue'], color='#4CAF50')
ax4.set_xlabel('Total Revenue (₹)', fontsize=10)
ax4.set_title('Top 5 Cities by Revenue', fontweight='bold')
ax4.invert_yaxis()

plt.tight_layout()
plt.savefig("sales_analysis_dashboard.png", dpi=150, bbox_inches='tight')
print("\n✅ Dashboard saved → sales_analysis_dashboard.png")

conn.close()
print("\n✅ Analysis complete!")
print("\nKey Insights:")
top_cat = df_q1.iloc[0]
print(f"  • Top category: {top_cat['Category']} with ₹{top_cat['Total_Revenue']:,.0f} revenue")
top_city = df_q2.iloc[0]
print(f"  • Top city: {top_city['City']} with ₹{top_city['Total_Revenue']:,.0f} revenue")
top_pay = df_q4.iloc[0]
print(f"  • Most used payment: {top_pay['Payment_Method']} ({top_pay['Usage_Pct']}% of orders)")
