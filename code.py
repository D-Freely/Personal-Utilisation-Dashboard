import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# --------------------

# USER INPUT SECTION

util_report_path = '.../Util report - 042019_062020.csv'

# --------------------

pd.options.mode.chained_assignment = None
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# Create new column headers
util_column_headers = ['Date', 'Utilisation (%)', 'Target Chargeable', 'Chargeable Hours', 'BD', 'People Management', 'Training', 'Holiday & Other Leave', 'Sick', 'Other', 'Planned Hours', 'Overtime']


# Read in utilisation and time reports
df_util = pd.read_csv(util_report_path, index_col=False, skiprows=[0,1,3,4], names=util_column_headers, header=0)

# ------------------------------------------------------------------------------------------

df_util['Date'] = pd.to_datetime(df_util['Date'])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

app.layout = html.Div([

    html.Br(),

    html.H1(
        children='Personal Utilisation Dashboard',
        style = {
            'textAlign': 'center'
            }
        ),
    html.Div(children= 'Created by the FS Ops Data Analytics Community', style = {
        'textAlign': 'center',
        'color': '#000000'
        }),

    html.Br(),

    dbc.Row(dbc.Col(dcc.DatePickerRange(
        id='my-date-picker-range',
        calendar_orientation='horizontal',
        day_size=39,
        end_date_placeholder_text="Return",
        with_portal=False,
        first_day_of_week=0,
        reopen_calendar_on_clear=True,
        is_RTL=False,
        clearable=True,
        number_of_months_shown=1,
        min_date_allowed=df_util['Date'].tolist()[0],
        max_date_allowed=df_util['Date'].tolist()[-1],
        initial_visible_month=df_util['Date'].tolist()[0],
        start_date=df_util['Date'].tolist()[0].date(),
        end_date=df_util['Date'].tolist()[-1].date(),
        display_format='MMMM, YY',
        month_format='MMMM, YYYY',
        minimum_nights=2,

        persistence=True,
        persisted_props=['start_date'],
        persistence_type='session',

        updatemode='singledate'
        ),
        width={'size': 5, 'offset': 5},

                    ),
            ),

    html.Br(),

    dbc.Row(dbc.Col(dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Graph(
                        id='table',
                    )

                    ]
                ),
            ],
        color='secondary'
    ),
        width={'size':10, 'offset':1}
    )),

    html.Br(),

    dbc.Row(dbc.Col(dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Summary of Hours", className="card-title"),
                    dcc.Graph(
                        id='sum of hours',
                    )

                ]
            ),
        ],
        color='secondary'
    ),
        width={'size': 10, 'offset': 1}
    )),

    html.Br(),

    dbc.Row(dbc.Col(dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H4("Utilisation % per month", className="card-title"),
                    dcc.Graph(
                        id='util per month',
                    )

                ]
            ),
        ],
        color='secondary'
    ),
        width={'size': 10, 'offset': 1}
    )),

    html.Br()

    ])



@app.callback(
    [Output('sum of hours', 'figure'),
     Output('util per month', 'figure'),
     Output('table', 'figure')],
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_output(start_date, end_date):
    mask = (df_util['Date'] >= start_date) & (df_util['Date'] <= end_date)
    df_util2 = df_util.loc[mask]
    df_util2['Date'] = df_util2['Date'].dt.strftime('%b %Y')

    fig1 = px.bar(df_util2, x='Date', y=['Chargeable Hours', 'BD', 'Training', 'Holiday & Other Leave', 'Other'], template='seaborn')

    fig1.add_trace(go.Scatter(name='Planned Hours', x=df_util2['Date'], y=df_util['Planned Hours']))

    fig1.update_layout(barmode='stack',
                       legend_title_text='',
                       legend=dict(
                           orientation="h",
                           yanchor="bottom",
                           y=1.02,
                           xanchor="right",
                           x=1
                       ),
                       title_font_family='Calibri',
                       title_font_color='IndianRed',
                       title_font_size=20,
                       height=350,
                       plot_bgcolor='rgba(0, 0, 0, 0)',
                       paper_bgcolor='rgba(0, 0, 0, 0)'
                       )

    fig1.update_yaxes(title_text='Hours', title_font=dict(size=15, family='Courier', color='IndianRed'),
                      title_standoff=10)
    fig1.update_xaxes(title_text='', title_font=dict(size=15, family='Courier', color='IndianRed'),
                      title_standoff=10)

# ------------------------------------------------------------------------------------------

    xlabel_lst = [0, 25, 50, 75, 100]
    xlabel_lst_str = [str(x) + '%' for x in xlabel_lst]
    average_util = df_util2['Utilisation (%)'].mean()
    average_text = str('{:.0f}'.format(average_util)) + '%' + ' Average'

    fig2 = px.bar(df_util2, x='Utilisation (%)', y='Date', orientation='h', template='seaborn')

    fig2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
        title_font_family='Calibri',
        title_font_color='IndianRed',
        title_font_size=20,
        height=350,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)'
        )

    fig2.update_yaxes(title_text='Date', title_font=dict(size=15, family='Courier', color='IndianRed'),
                      title_standoff=10)
    fig2.update_xaxes(title_text='Utilisation', title_font=dict(size=15, family='Courier', color='IndianRed'),
                      title_standoff=10, tickmode='array', tickvals=xlabel_lst, ticktext=xlabel_lst_str)
    fig2.add_vline(x=average_util, line_width=2, line_dash="dash", line_color="IndianRed",
                   annotation_text=average_text, annotation_position='top', annotation_font_size=15,
                   annotation_font_color='IndianRed')

# ------------------------------------------------------------------------------------------

    fig3 = go.Figure()
    fig3.add_trace(go.Indicator(
        mode='number',
        value=df_util2['Chargeable Hours'].sum(),
        domain={'x': [0, 0.5], 'y': [0, 1]},
        title='Total Chargeable Hours',
        number={"font": {"size": 70}}
    ))
    fig3.add_trace(go.Indicator(
        mode='number',
        value=df_util2['BD'].sum(),
        domain={'x': [0.3, 0.75], 'y': [0, 1]},
        title='Total BD Hours',
        number={"font": {"size": 70}}
    ))
    fig3.add_trace(go.Indicator(
        mode='number',
        value=df_util2['Training'].sum(),
        domain={'x': [0.6, 1], 'y': [0, 1]},
        title='Total Training Hours',
        number={"font": {"size": 70}}
    ))

    fig3.update_layout(
        template='seaborn',
        height=140,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(
            t=20,
            b=10,
            l=20,
            r=20)
    )

    return fig1, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)
