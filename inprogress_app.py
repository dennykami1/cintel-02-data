from shiny import App, Inputs, Outputs, Session, ui, render
import matplotlib.pyplot as plt
import shinyswatch
import palmerpenguins  # This Package Provides the Palmer Penguin Dataset

# Load the Palmer Penguins dataset
penguins = palmerpenguins.load_penguins()

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
            /* Custom styling for outer cards */
            .custom-border-card {
                border: 12px solid #8ecae6; /* Border color for outer cards */
                border-radius: 12px;
                padding: 0; /* No padding in the card to avoid gap */
                margin-bottom: 10px;
            }
            .card-header {
                margin:-3px 0 0 0;
                padding: 10px; /* Maintain your padding */
                background-color: #8ecae6; /* Header background color */
                color: #14213d; /* Header text color */
                border-top: 3px solid #8ecae6; /* Header top border color */
                border-bottom: 3px solid #8ecae6; /* Header bottom border color */
            }
        """)
    ),
    ui.card(  # Outer card to encapsulate everything
        ui.layout_sidebar(
            ui.sidebar(
                ui.div(
                    ui.input_slider("selected_number_of_bins", "Number of Bins (Flipper Length)", 1, 50, 20),
                    ui.tags.hr(),
                    ui.input_checkbox_group(
                        "multi_choice_input",
                        "Select One or More Penguin Species to Display:", 
                        choices=["Adelie", "Chinstrap", "Gentoo"],
                        selected=["Adelie", "Chinstrap", "Gentoo"],
                        inline=False
                    ),
                    class_="sidebar-custom"  # Apply custom sidebar class
                )
            ),
            ui.div(
                ui.h2("Kami's take on the PyShiny App with Palmer Penguins Histograms"),
                class_="title-box"
            ),
            ui.page_fillable(
                ui.card(
                    ui.card_header("Histogram of Flipper Length from Palmer Penguins Dataset", style="background-color: #8ecae6; color: #14213d;"),
                    ui.layout_columns(
                        # Card for Histogram of Flipper Length
                        ui.card(
                            ui.h2("Histogram"),
                            ui.output_plot("penguin_flipper_histogram"),
                        ),
                        # Card for Histogram of Body Mass
                        ui.card(
                            ui.h2("Scatter Plot"),
                            ui.output_plot("penguin_body_mass_histogram"),
                            full_screen=True  # Make inner card full-screen width
                        )
                    ),
                    class_="custom-border-card"  # Apply custom border class to this card only
                ),
                full_screen=True  # Make inner card full-screen width
            ),
            # Card for Palmer Penguins Data Frame
            ui.card(
                ui.card_header("Palmer Penguins Data Frame & Data Grid", style="background-color: #8ecae6; color: #14213d;"),
                ui.layout_columns(
                    # Column for Data Frame
                    ui.card(
                        ui.column(
                            11, 
                            ui.h2("Data Frame"),
                            ui.output_data_frame("penguins_df")
                        )
                    ),
                    # Column for Data Table
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

def server(input: Inputs, output: Outputs, session: Session):
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
    @render.plot(alt="A histogram of body mass from Palmer Penguins dataset")
    def penguin_body_mass_histogram():
        plt.clf()
        selected_species = input.multi_choice_input()
        filtered_data = penguins[penguins['species'].isin(selected_species)] if selected_species else penguins
        
        plt.hist(filtered_data['body_mass_g'].dropna(), 
                 bins=input.selected_number_of_bins(), density=True, 
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
