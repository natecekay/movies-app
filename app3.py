#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc, html, Input, Output
import pandas as pd
import gdown
import pandas as pd


# In[ ]:


# Original Google Drive sharing URL
url = "https://drive.google.com/file/d/1hPEoAtDZx0zE6sERnWPejOqy_S2dQGpA/view?usp=sharing"


# In[ ]:


# Transform to direct download link
file_id = url.split('/d/')[1].split('/view')[0]
direct_url = f"https://drive.google.com/uc?id={file_id}"


# In[ ]:


# Output file
output = "movie_ratings.csv"


# In[ ]:


# Download the file
gdown.download(direct_url, output, quiet=False)


# In[ ]:


# Load the CSV file into a pandas DataFrame
data_dir = pd.read_csv(output)
movie_data = data_dir


# In[ ]:


# Clean the data
movie_data = movie_data.drop(columns=['Unnamed: 0'])  # Drop unnecessary index column
movie_data = movie_data.dropna(subset=['imdb'])  # Remove rows with missing IMDb ratings


# In[ ]:


# Initialize the Dash app
app = dash.Dash(__name__)


# In[ ]:


# App layout
app.layout = html.Div([
    html.H1("Movie Recommendation App", style={'text-align': 'center'}),
    html.Label("Select Minimum IMDb Rating:"),
    dcc.Slider(
        id='imdb-slider',
        min=0,
        max=10,
        step=0.1,
        value=8,
        marks={i: str(i) for i in range(11)}
    ),
    html.Br(),
    html.Label("Filter by Release Year:"),
    dcc.RangeSlider(
        id='year-slider',
        min=movie_data['year'].min(),
        max=movie_data['year'].max(),
        step=1,
        value=[2000, 2020],
        marks={i: str(i) for i in range(movie_data['year'].min(), movie_data['year'].max() + 1, 10)}
    ),
    html.Br(),
    html.Div(id='movie-output'),
])


# In[ ]:


# Callback for updating movie recommendations
@app.callback(
    Output('movie-output', 'children'),
    [Input('imdb-slider', 'value'),
     Input('year-slider', 'value')]
)
def update_recommendations(imdb_min, year_range):
    filtered_movies = movie_data[
        (movie_data['imdb'] >= imdb_min) &
        (movie_data['year'] >= year_range[0]) &
        (movie_data['year'] <= year_range[1])
    ]
    filtered_movies = filtered_movies.sort_values(by='imdb', ascending=False)
    if filtered_movies.empty:
        return html.Div("No movies match the selected criteria.")
    return html.Ul([
        html.Li(f"{row['movie']} (Year: {row['year']}, IMDb: {row['imdb']})")
        for _, row in filtered_movies.iterrows()
    ])


# In[ ]:


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)

