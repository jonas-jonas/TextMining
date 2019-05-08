from bokeh.plotting import figure
from bokeh.embed import components

from services.database import DatabaseHandler
import pandas as pd
import logging

def posts_by_time():
    data = pd.read_sql("SELECT created_utc FROM post", DatabaseHandler().session.connection)

    print(data)

    result = {}

    for x in data:
        print(x)
    return result

def comments_by_time(post_id):
    query = f"""
            SELECT start_time, count(c.created_utc) AS comments
            FROM (SELECT generate_series(min(created_utc), max(created_utc), interval '60 min') FROM comment) g(start_time)
            LEFT JOIN comment c ON c.created_utc >= g.start_time
                 AND c.created_utc <  g.start_time + interval '60 min'
            WHERE c.post_id = '{post_id}'
            GROUP  BY 1
            ORDER  BY 1;"""

    data = pd.read_sql(query, DatabaseHandler().session.connection)

    p = figure(sizing_mode="scale_width", tools="", title="Comments by time", x_axis_type="datetime")

    p.vbar(source = data, x="start_time", top ="comments", width=1, line_width=10, legend="Comments")
    print(type(data['start_time'][0]))

    return components(p)


