import streamlit as st

st.title("My App")

# Appliance list with default wattage
appliances = {
    "LED Bulb": 10,
    "Tube Light": 20,
    "Ceiling Fan": 75,
    "Exhaust Fan": 40,
    "Refrigerator": 250,
    "Deep Freezer": 350,
    "LED TV": 120,
    "Desktop Computer": 250,
    "Laptop": 65,
    "Air Conditioner (1 Ton)": 1200,
    "Air Conditioner (1.5 Ton)": 1800,
    "Air Conditioner (2 Ton)": 2500,
    "Microwave Oven": 1200,
    "Electric Iron": 1000,
    "Electric Kettle": 1500,
    "Water Heater": 2000,
    "Water Pump": 750,
    "Washing Machine": 600,
    "Vacuum Cleaner": 1000,
    "Rice Cooker": 700
}


def calculate_load(
    bulb, tube, fan, exhaust, fridge, freezer, tv, desktop,
    laptop, ac1, ac15, ac2, microwave, iron, kettle,
    heater, pump, washing, vacuum, rice,
    voltage, power_factor
):

    quantities = [
        bulb, tube, fan, exhaust, fridge, freezer, tv, desktop,
        laptop, ac1, ac15, ac2, microwave, iron, kettle,
        heater, pump, washing, vacuum, rice
    ]

    records = []
    total_watts = 0

    for (name, watt), qty in zip(appliances.items(), quantities):
        load = qty * watt
        total_watts += load

        records.append([
            name,
            qty,
            watt,
            load
        ])

    total_kw = total_watts / 1000

    current = total_watts / (voltage * power_factor)

    generator = total_kw * 1.25

    breaker = current * 1.25

    df = pd.DataFrame(
        records,
        columns=[
            "Appliance",
            "Quantity",
            "Unit Watt",
            "Total Watt"
        ]
    )

    return (
        df,
        f"{total_watts:.0f} Watts",
        f"{total_kw:.2f} kW",
        f"{current:.2f} A",
        f"{generator:.2f} kW",
        f"{breaker:.0f} A"
    )


with gr.Blocks(title="Building Electrical Load Calculator") as demo:

    gr.Markdown("# ⚡ Building Electrical Load Calculator")

    gr.Markdown(
        "Enter the number of appliances to calculate the total electrical load."
    )

    with gr.Row():
        bulb = gr.Number(value=0, label="LED Bulbs")
        tube = gr.Number(value=0, label="Tube Lights")
        fan = gr.Number(value=0, label="Ceiling Fans")
        exhaust = gr.Number(value=0, label="Exhaust Fans")

    with gr.Row():
        fridge = gr.Number(value=0, label="Refrigerators")
        freezer = gr.Number(value=0, label="Deep Freezers")
        tv = gr.Number(value=0, label="LED TVs")
        desktop = gr.Number(value=0, label="Desktop PCs")

    with gr.Row():
        laptop = gr.Number(value=0, label="Laptops")
        ac1 = gr.Number(value=0, label="1 Ton AC")
        ac15 = gr.Number(value=0, label="1.5 Ton AC")
        ac2 = gr.Number(value=0, label="2 Ton AC")

    with gr.Row():
        microwave = gr.Number(value=0, label="Microwave")
        iron = gr.Number(value=0, label="Electric Iron")
        kettle = gr.Number(value=0, label="Electric Kettle")
        heater = gr.Number(value=0, label="Water Heater")

    with gr.Row():
        pump = gr.Number(value=0, label="Water Pump")
        washing = gr.Number(value=0, label="Washing Machine")
        vacuum = gr.Number(value=0, label="Vacuum Cleaner")
        rice = gr.Number(value=0, label="Rice Cooker")

    with gr.Row():
        voltage = gr.Dropdown(
            choices=[120, 220, 230, 240],
            value=230,
            label="Supply Voltage (V)"
        )

        power_factor = gr.Slider(
            0.5,
            1.0,
            value=0.9,
            step=0.01,
            label="Power Factor"
        )

    calculate = gr.Button("Calculate")

    table = gr.Dataframe()

    total_watts = gr.Textbox(label="Total Load (Watts)")

    total_kw = gr.Textbox(label="Total Load (kW)")

    current = gr.Textbox(label="Estimated Current (A)")

    generator = gr.Textbox(label="Recommended Generator")

    breaker = gr.Textbox(label="Recommended Breaker")

    calculate.click(
        calculate_load,
        inputs=[
            bulb, tube, fan, exhaust,
            fridge, freezer, tv, desktop,
            laptop, ac1, ac15, ac2,
            microwave, iron, kettle,
            heater, pump, washing,
            vacuum, rice,
            voltage, power_factor
        ],
        outputs=[
            table,
            total_watts,
            total_kw,
            current,
            generator,
            breaker
        ]
    )

demo.launch()
