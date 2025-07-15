import streamlit as st
import pandas as pd
import joblib

# Page config
st.set_page_config(page_title="Concrete Strength Predictor", layout="wide")

# Load Tailwind and custom styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        html, body {
            font-family: 'Inter', sans-serif;
            background-color: #f0f4f8;
        }

        .app-container {
            background: white;
            border-radius: 1rem;
            padding: 2rem;
            max-width: 1000px;
            margin: 2rem auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            transition: all 0.3s ease-in-out;
        }

        h1 {
            color: #1e3a8a;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 800;
        }

        .description {
            color: #334155;
            text-align: center;
            margin-bottom: 2rem;
        }

        .submit-button {
            background-color: #ef4444;
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            font-size: 1rem;
            border-radius: 0.5rem;
            transition: background-color 0.3s ease;
            font-weight: 600;
            margin-top: 1.5rem;
        }

        .submit-button:hover {
            background-color: #dc2626;
            cursor: pointer;
        }

        .results-table {
            background: #f9fafb;
            margin-top: 2rem;
            border-radius: 0.75rem;
            padding: 1.5rem;
            border: 1px solid #dbeafe;
        }

        .results-table h2 {
            color: #1e3a8a;
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 1rem;
        }

        th {
            background-color: #3b82f6;
            color: white;
            padding: 0.75rem;
        }

        td {
            border: 1px solid #e5e7eb;
            padding: 0.75rem;
            color: #1e293b;
        }

        tr:nth-child(even) {
            background-color: #f1f5f9;
        }

        tr:hover {
            background-color: #e0f2fe;
        }
    </style>
""", unsafe_allow_html=True)

# Load model
model = joblib.load('concrete_model.pkl')

# UI container
st.markdown('<div class="app-container">', unsafe_allow_html=True)

# Header
st.markdown("<h1>Concrete Strength Predictor</h1>", unsafe_allow_html=True)
st.markdown('<p class="description">Enter the concrete mix parameters to predict its strength properties</p>', unsafe_allow_html=True)

# Input form
with st.form(key='input_form'):
    col1, col2 = st.columns(2)

    with col1:
        cement = st.number_input("Cement Content (kg/m³)", min_value=300.0, max_value=500.0, value=400.0, step=0.1)
        fine_agg = st.number_input("Fine Aggregate (kg/m³)", min_value=600.0, max_value=800.0, value=700.0, step=0.1)
        coarse_agg = st.number_input("Coarse Aggregate (kg/m³)", min_value=800.0, max_value=1000.0, value=900.0, step=0.1)
        rubber_pct = st.number_input("Rubber Percentage (%)", min_value=0.0, max_value=20.0, value=10.0, step=0.01)
    
    with col2:
        water_pct = st.number_input("Water Percentage (%)", min_value=30.0, max_value=60.0, value=40.0, step=0.01)
        w_c_ratio = st.number_input("Water-to-Cement Ratio", min_value=0.4, max_value=0.7, value=0.5, step=0.01)
        rubber_shape = st.selectbox("Rubber Shape", options=['spherical', 'irregular', 'angular'])
        rubber_size = st.selectbox("Rubber Size", options=['<1mm', '1-2mm', '>2mm'])
        curing_days = st.number_input("Curing Days", min_value=7, max_value=90, value=28, step=1)

    submit_button = st.form_submit_button("Predict")

# Predict and show results
if submit_button:
    input_data = pd.DataFrame({
        'cement_kg_m3': [cement],
        'fine_aggregate_kg_m3': [fine_agg],
        'coarse_aggregate_kg_m3': [coarse_agg],
        'rubber_pct': [rubber_pct],
        'water_pct': [water_pct],
        'w_c_ratio': [w_c_ratio],
        'rubber_shape': [rubber_shape],
        'rubber_size': [rubber_size],
        'curing_days': [curing_days]
    })

    try:
        predictions = model.predict(input_data)[0]

        st.markdown(f"""
            <div class="results-table">
                <h2>Prediction Results</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Property</th>
                            <th>Predicted Value</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Compressive Strength (MPa)</td>
                            <td>{predictions[0]:.2f}</td>
                        </tr>
                        <tr>
                            <td>Flexural Strength (MPa)</td>
                            <td>{predictions[1]:.2f}</td>
                        </tr>
                        <tr>
                            <td>Tensile Strength (MPa)</td>
                            <td>{predictions[2]:.2f}</td>
                        </tr>
                        <tr>
                            <td>Modulus of Elasticity (GPa)</td>
                            <td>{predictions[3]:.2f}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Prediction error: {str(e)}")

# End container
st.markdown("</div>", unsafe_allow_html=True)
