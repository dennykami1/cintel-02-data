from shiny import App, Inputs, Outputs, Session, ui, render
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd  # Import pandas here
from shinywidgets import output_widget, render_widget
import shinyswatch
import palmerpenguins  # This Package Provides the Palmer Penguin Dataset

# Load the Palmer Penguins dataset
penguins = palmerpenguins.load_penguins()  # Correctly load the dataset

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style(""" 
            .title-box {
                background-color: #457b9d; /* Title box color */
                border: 1px solid #ccc;
                padding: 10px;
                text-align: center;
                font-family: 'Arial', sans-serif;
                font-size: 15px;
                color: #111111;
                margin-bottom: 5px;
                border-radius: 12px;
            }
            .sidebar-custom {
                background-color: #8ecae6; /* Sidebar background color */
                padding: 35px;
                border-radius: 12px;
                border: 1px solid #edf6f9;
            }
            .custom-border-card {
                border: 12px solid #8ecae6; /* Border color for outer cards */
                border-radius: 12px;
                padding: 0; /* No padding in the card to avoid gap */
                margin-bottom: 10px;
            }
            .card-header {
                margin: -3px 0 0 0;
                padding: 10px; /* Maintain your padding */
                background-color: #8ecae6; /* Header background color */
                color: #14213d; /* Header text color */
                border-top: 3px solid #8ecae6; /* Header top border color */
                border-bottom: 3px solid #8ecae6; /* Header bottom border color */
            }
        """)
    ),
    ui.card(
        ui.layout_sidebar(
            ui.sidebar(
                ui.div(
                    ui.h2("Side Bar"),
                    ui.tags.hr(),
                    ui.input_slider("selected_number_of_bins", "Seaborn Bin Count", 1, 50, 25),
                    ui.tags.hr(),
                    ui.input_numeric("numeric", "Numeric Input for Plotly Histogram Bins", 1, min=1, max=10),
                    ui.output_text_verbatim("value"),
                    ui.tags.hr(),
                    ui.input_selectize(
                        "selectize",
                        "Select an option below:",
                        {"bill_length_mm": "bill_length", "flipper_length_mm": "flipper_length", "body_mass_g": "body_mass"},
                    ),
                    ui.input_checkbox_group(
                        "multi_choice_input",
                        "Select One or More Penguin Species to Display:",
                        choices=["Adelie", "Chinstrap", "Gentoo"],
                        selected=["Adelie", "Chinstrap", "Gentoo"],
                        inline=False
                    ),
                    class_="sidebar-custom"  # Apply custom sidebar class
                ),
            ),
            ui.div(
                ui.h2("Kami's take on the PyShiny App with Palmer Penguins Histograms"),
                class_="title-box"
            ),
            ui.page_fillable(
                ui.card(
                    ui.card_header("Histogram of Flipper Length from Palmer Penguins Dataset", style="background-color: #8ecae6; color: #14213d;"),
                    ui.layout_columns(
                        ui.card(
                            ui.h2("Histogram"),
                            ui.output_plot("penguin_flipper_histogram")
                        ),
                        ui.card(
                            ui.h2("Scatter Plot"),
                            ui.output_plot("penguin_histogram"),
                            full_screen=True  # Make inner card full-screen width
                        )
                    ),
                    class_="custom-border-card"  # Apply custom border class to this card only
                ),
                full_screen=True  # Make inner card full-screen width
            ),
            ui.card(
                ui.card_header("Palmer Penguins Data Frame & Data Grid", style="background-color: #8ecae6; color: #14213d;"),
                ui.layout_columns(
                    ui.card(
                        ui.column(
                            11,
                            ui.h2("Data Frame"),
                            ui.output_data_frame("penguins_df")
                        )
                    ),
                    ui.card(
                        ui.column(
                            11,
                            ui.h2("Data Table"),
                            ui.output_data_frame("penguins_dt")
                        )
                    )
                ),
                class_="custom-border-card",  # Apply custom border class to this card only
                full_screen=True  # Outer card full-screen width
            )
        ),
        full_screen=True,  # Outer card full-screen width
        style="padding: 20px;"
    ),
    theme=shinyswatch.theme.lumen
)

def server(input, output, session):

    @output
    @render.plot(alt="A histogram of flipper length from Palmer Penguins dataset")
    def penguin_flipper_histogram():
        plt.clf()
        selected_species = input.multi_choice_input()
        filtered_data = penguins[penguins['species'].isin(selected_species)] if selected_species else penguins

        colors = {"Adelie": "#0f4c5c", "Chinstrap": "#fb8b24", "Gentoo": "#5f0f40"}
        for species in selected_species:
            species_data = filtered_data[filtered_data['species'] == species]['flipper_length_mm'].dropna()
            plt.hist(species_data, bins=input.selected_number_of_bins(), 
                     density=True, alpha=0.5, color=colors[species], 
                     label=species)
        
        plt.xlabel("Flipper Length (mm)")
        plt.ylabel("Density")
        plt.title("Histogram of Flipper Length from Palmer Penguins Dataset")
        plt.legend(title="Penguin Species")
    
    @output
    @render_widget  # Use render_widget for the Plotly histogram
    def penguin_histogram(): 
        scatterplot = px.histogram(
                data_frame=penguins,
                x="body_mass_g",
                nbins=input.n(),
            ).update_layout(
                title={"text": "Penguin Mass", "x": 0.5},
                yaxis_title="Count",
                xaxis_title="Body Mass (g)",
            )
    
        return scatterplot  
        
    @output
    @render.data_frame
    def penguins_df():
        return render.DataGrid(penguins)

    @output
    @render.data_frame  
    def penguins_dt():
        return render.DataTable(penguins) 
app = App(app_ui, server)
