"""Tab 1 — sortable/filterable data table over curated columns."""

from dash import dash_table, html

import ctransforms

PAGE_SIZE = 50

layout = html.Div(
    [
        html.P(
            "Excel-like browse of daily country observations. "
            "Use column headers to sort/filter; sidebar filters narrow the universe first.",
            className="text-muted",
        ),
        dash_table.DataTable(
            id="table-sorting-filtering",
            columns=[{"name": c, "id": c} for c in ctransforms.TABLE_COLUMNS],
            page_current=0,
            page_size=PAGE_SIZE,
            page_action="custom",
            filter_action="custom",
            filter_query="",
            sort_action="custom",
            sort_mode="multi",
            sort_by=[],
            style_table={"height": "680px", "overflowX": "auto", "overflowY": "auto"},
            style_header={"fontWeight": "600", "backgroundColor": "#f8f9fa"},
            style_cell={
                "minWidth": "110px",
                "width": "110px",
                "maxWidth": "160px",
                "textAlign": "left",
                "padding": "6px",
                "fontSize": "13px",
            },
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "#fafafa"},
            ],
        ),
    ]
)
