from shiny import App, Inputs, Outputs, Session, ui, render
import matplotlib.pyplot as plt
import numpy as np
import shinyswatch
import palmerpenguins  # This Package Provides the Palmer Penguin Dataset

# Load the Palmer Penguins dataset
penguins = palmerpenguins.load_penguins()

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.style(""" 
            .title-box {
                background-color: #A4C8E1; /* Title box color */
                border: 1px solid #ccc;
                padding: 10px;
                text-align: center;
                font-family: 'Arial', sans-serif;
                font-size: 15px;
                color: #333;
                margin-bottom: 5px;
                border-radius: 9px;
            }
            /* Custom styling for the DataFrame header */
            .dataframe-header th {
                background-color: #A4C8E1; /* Light blue for header */
                color: #333; /* Text color for header */
            }
        """)
    ),
    ui.card(  # Outer card to encapsulate everything
        ui.div(
            ui.h2("Kami's take on the PyShiny App with Palmer Penguins Histograms"),
            class_="title-box"
        ),
        ui.page_fillable(
            ui.layout_columns(
                # Card for Histogram of Flipper Length
                ui.card(
                    ui.card_header("Histogram of Flipper Length from Palmer Penguins Dataset", style="background-color: #A4C8E1; color: #333;"),
                    ui.layout_sidebar(
                        ui.sidebar(
                            ui.input_slider("selected_number_of_bins1", "Number of Bins (Flipper Length)", 1, 50, 20),
                            ui.tags.hr(),
                            ui.input_checkbox_group(
                                "multi_choice_input",
                                "Select One or More Penguin Species to Display:", 
                                choices=["Adelie", "Chinstrap", "Gentoo"],
                                selected=["Adelie", "Chinstrap", "Gentoo"],
                                inline=False,
                            ),
                            bg="#edf6f9"
                        ),
                        ui.output_plot("penguin_flipper_histogram")
                    ),
                    full_screen=True  # Make inner card full-screen width
                ),
                # Card for Histogram of Body Mass
                ui.card(
                    ui.card_header("Histogram of Body Mass from Palmer Penguins Dataset", style="background-color: #A4C8E1; color: #333;"),
                    ui.layout_sidebar(
                        ui.sidebar(
                            ui.input_slider("selected_number_of_bins2", "Number of Bins (Body Mass)", 1, 50, 20),
                            bg="#edf6f9"
                        ),
                        ui.output_plot("penguin_body_mass_histogram")
                    ),
                    full_screen=True  # Make inner card full-screen width
                ),
            ),
            # Card for Palmer Penguins Data Frame
            ui.card(
                ui.card_header("Palmer Penguins Data Frame & Data Grid", style="background-color: #A4C8E1; color: #333;"),
                ui.layout_columns(
                    # Column for Data Frame
                    ui.card(
                        ui.column(
                            11, 
                            ui.h2("Data Frame"),
                            ui.output_data_frame("penguins_df"),
                        ),
                    ),
                    # Column for Data Table
                    ui.card(
                        ui.column(
                            11,  
                            ui.h2("Data Table"),
                            ui.output_data_frame("penguins_dt"),
                        
                        ),
                    ),   
                ),
                full_screen=True,  # Outer card full-screen width
            )
        ),
        full_screen=True,  # Outer card full-screen width
        style="padding: 20px;"
    ),
    theme=shinyswatch.theme.lumen
)

def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.plot(alt="A histogram of flipper length from Palmer Penguins dataset")
    def penguin_flipper_histogram():
        plt.clf()
        selected_species = input.multi_choice_input()
        filtered_data = penguins[penguins['species'].isin(selected_species)] if selected_species else penguins

        colors = {"Adelie": "#386fa4", "Chinstrap": "#662e9b", "Gentoo": "#469d89"}
        for species in selected_species:
            species_data = filtered_data[filtered_data['species'] == species]['flipper_length_mm'].dropna()
            plt.hist(species_data, bins=input.selected_number_of_bins1(), 
                     density=True, alpha=0.5, color=colors[species], 
                     label=species)
        
        plt.xlabel("Flipper Length (mm)")
        plt.ylabel("Density")
        plt.title("Histogram of Flipper Length from Palmer Penguins Dataset")
        plt.legend(title="Penguin Species")
        
    @output
    @render.plot(alt="A histogram of body mass from Palmer Penguins dataset")
    def penguin_body_mass_histogram():
        plt.clf()
        selected_species = input.multi_choice_input()
        filtered_data = penguins[penguins['species'].isin(selected_species)] if selected_species else penguins
        
        plt.hist(filtered_data['body_mass_g'].dropna(), 
                 bins=input.selected_number_of_bins2(), density=True, 
                 color="#D95B43")
        plt.xlabel("Body Mass (g)")
        plt.ylabel("Density")
        plt.title("Histogram of Body Mass from Palmer Penguins Dataset")
    
    # Render the penguins data as a DataFrame
    @output
    @render.data_frame
    def penguins_df():
        return render.DataGrid(penguins)

    @output
    @render.data_frame  
    def penguins_dt():
        return render.DataTable(penguins) 

app = App(app_ui, server)
