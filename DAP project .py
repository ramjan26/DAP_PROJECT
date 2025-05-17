import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv('C:/Users/Acer/OneDrive/Desktop/Week 1/world-happiness-report 1.csv')

# Create a composite SPI score
spi_components = ['Social support', 'Healthy life expectancy', 
                 'Freedom to make life choices', 'Generosity',
                 'Perceptions of corruption', 'Dystopia + residual']
df['SPI Score'] = df[spi_components].mean(axis=1)

# 1. Correlation Matrix
plt.figure(figsize=(10, 8))
correlation_matrix = df[spi_components + ['Ladder score']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of SPI Components with Happiness Score')
plt.show()

# 2. Bubble Charts

# Bubble Chart 1: Happiness vs Social Support
fig1 = px.scatter(
    df,
    x="Social support",
    y="Ladder score",
    size="Logged GDP per capita",
    color="Regional indicator",
    hover_name="Country name",
    title="Happiness vs. Social Support (Bubble Size = GDP per capita)",
    labels={"Social support": "Social Support (0-1)", "Ladder score": "Happiness Score"},
    size_max=30
)
fig1.show()

# Bubble Chart 2: Freedom vs Corruption
fig2 = px.scatter(
    df,
    x="Freedom to make life choices",
    y="Perceptions of corruption",
    size="Ladder score",
    color="Regional indicator",
    hover_name="Country name",
    title="Freedom vs. Corruption (Bubble Size = Happiness Score)",
    labels={
        "Freedom to make life choices": "Freedom (0-1)",
        "Perceptions of corruption": "Corruption Perception (0-1)",
    }
)
fig2.show()

# Bubble Chart 3: GDP vs Happiness with Life Expectancy
fig3 = px.scatter(
    df,
    x="Logged GDP per capita",
    y="Ladder score",
    size="Healthy life expectancy",
    color="Regional indicator",
    hover_name="Country name",
    title="Happiness vs GDP with Life Expectancy Bubble Size",
    labels={
        "Logged GDP per capita": "Logged GDP per capita",
        "Ladder score": "Happiness Score",
        "Healthy life expectancy": "Life Expectancy"
    },
    size_max=60
)
fig3.show()

# ======================
# 3. Global Maps
# ======================

# Map 1: Healthy Life Expectancy
map1 = px.choropleth(
    df,
    locations="Country name",
    locationmode="country names",
    color="Healthy life expectancy",
    hover_name="Country name",
    color_continuous_scale="Viridis",
    title="Global Healthy Life Expectancy (Years)"
)
map1.show()

# Map 2: Social Support
map2 = px.choropleth(
    df,
    locations="Country name",
    locationmode="country names",
    color="Social support",
    hover_name="Country name",
    color_continuous_scale="Plasma",
    title="Global Social Support Index"
)
map2.show()

# Map 3: Composite SPI Score
map3 = px.choropleth(
    df,
    locations="Country name",
    locationmode="country names",
    color="SPI Score",
    hover_name="Country name",
    color_continuous_scale="Plasma",
    title="Composite Social Progress Index (SPI) Score"
)
map3.show()

# 4. Radar Chart (Top 5 Countries)
top_countries = df.nlargest(5, 'Ladder score')

radar_fig = go.Figure()
for i, row in top_countries.iterrows():
    radar_fig.add_trace(go.Scatterpolar(
        r=[
            row['Social support'], 
            row['Healthy life expectancy'],
            row['Freedom to make life choices'], 
            row['Generosity'],
            row['Perceptions of corruption'],
            row['Social support']
        ],
        theta=[
            'Social support', 'Healthy life expectancy',
            'Freedom to make', 'Generosity',
            'Perceptions of corruption', 'Social support'
        ],
        fill='toself',
        name=row['Country name']
    ))

radar_fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=True,
    title='SPI Components Comparison for Top 5 Happiest Countries'
)
radar_fig.show()

# 5. Regional Analysis
regional_means = df.groupby('Regional indicator')[spi_components].mean().reset_index()
melted_regional = pd.melt(
    regional_means, 
    id_vars=['Regional indicator'], 
    value_vars=spi_components,
    var_name='SPI Component', 
    value_name='Average Score'
)

plt.figure(figsize=(12, 8))
sns.barplot(
    data=melted_regional, 
    x='Average Score', 
    y='Regional indicator', 
    hue='SPI Component'
)
plt.title('Average SPI Component Scores by Region')
plt.xlabel('Average Score')
plt.ylabel('Region')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
