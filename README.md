# Aerodynamic-Analysis-Tool
# DevOps-Integrated Aerodynamic Analysis Tool using Python

## 📌 Overview
This project is a Python-based aerodynamic analysis tool developed using DevOps principles. It provides an interactive interface to analyze airfoil and wing performance and compare multiple configurations.

The system integrates development and operations practices such as version control and continuous integration to ensure reliability and scalability.

---

## 🎯 Features

- Airfoil Analysis (NACA 4-digit airfoils)
- Wing Performance Analysis
- Comparison of Airfoils and Wings
- Interactive Graphical Visualization
- DevOps Integration using GitHub and CI

---

## 🛠️ Technologies Used

- Python
- Streamlit
- NumPy
- Matplotlib
- Git
- GitHub
- GitHub Actions (CI)

---

## ✈️ Modules

### 1. Airfoil Analysis
- Input NACA 4-digit airfoil
- Generates airfoil shape
- Calculates:
  - Lift coefficient (Cl)
  - Drag coefficient (Cd)
  - Lift-to-Drag ratio (L/D)

---

### 2. Wing Analysis
- Inputs:
  - Wingspan
  - Chord length
- Calculates:
  - Aspect Ratio (AR)
  - Lift and drag characteristics

---

### 3. Comparison Module
- Compare two airfoils
- Compare two wing configurations
- Visualize performance differences

---

## 📊 Aerodynamic Model

Lift:
Cl = 2π α

Drag:
Cd = 0.01 + Cl² / (πAR e)

---

## 🚀 How to Run the Project

1. Clone the repository:
