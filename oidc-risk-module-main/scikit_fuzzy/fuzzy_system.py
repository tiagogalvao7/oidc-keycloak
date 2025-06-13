import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def calculate_risk(impact_value, gdpr_compliance_value):
    # Define the input variables
    impact = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'impact')
    gdpr_compliance = ctrl.Antecedent(np.arange(0, 1.01, 0.01), 'gdpr_compliance')

    # Define the output variable
    risk = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'risk')

    # Define trapezoidal membership functions for 'impact'
    impact['none'] = fuzz.trimf(impact.universe, [0.0, 0.0, 0.0])
    impact['low'] = fuzz.trapmf(impact.universe, [0.1, 0.1, 0.2, 0.39])
    impact['medium'] = fuzz.trapmf(impact.universe, [0.3, 0.4, 0.54, 0.69])
    impact['high'] = fuzz.trapmf(impact.universe, [0.6, 0.7, 1.0, 1.0])

    # Define triangular membership functions for 'gdpr_compliance'
    gdpr_compliance['non_compliant'] = fuzz.trimf(gdpr_compliance.universe, [0.0, 0.0, 0.0])
    gdpr_compliance['compliant'] = fuzz.trimf(gdpr_compliance.universe, [1.0, 1.0, 1.0])
    gdpr_compliance['unknown'] = fuzz.trimf(gdpr_compliance.universe, [0.5, 0.5, 0.5])

    # Define trapezoidal membership functions for 'risk'
    risk['none'] = fuzz.trimf(risk.universe, [0.0, 0.0, 0.0])
    risk['low'] = fuzz.trapmf(risk.universe, [0.1, 0.1, 0.2, 0.39])
    risk['medium'] = fuzz.trapmf(risk.universe, [0.3, 0.4, 0.54, 0.69])
    risk['high'] = fuzz.trapmf(risk.universe, [0.6, 0.7, 0.8, 0.89])
    risk['critical'] = fuzz.trapmf(risk.universe, [0.8, 0.9, 1.0, 1.0])

    # Define fuzzy rules based on the new table
    rule0 = ctrl.Rule(impact['none'] & gdpr_compliance['compliant'], risk['none'])
    rule1 = ctrl.Rule(impact['none'] & gdpr_compliance['unknown'], risk['low'])
    rule2 = ctrl.Rule(impact['none'] & gdpr_compliance['non_compliant'], risk['low'])

    rule3 = ctrl.Rule(impact['low'] & gdpr_compliance['compliant'], risk['low'])
    rule4 = ctrl.Rule(impact['low'] & gdpr_compliance['unknown'], risk['medium'])
    rule5 = ctrl.Rule(impact['low'] & gdpr_compliance['non_compliant'], risk['medium'])

    rule6 = ctrl.Rule(impact['medium'] & gdpr_compliance['compliant'], risk['medium'])
    rule7 = ctrl.Rule(impact['medium'] & gdpr_compliance['unknown'], risk['medium'])
    rule8 = ctrl.Rule(impact['medium'] & gdpr_compliance['non_compliant'], risk['high'])

    rule9 = ctrl.Rule(impact['high'] & gdpr_compliance['compliant'], risk['high'])
    rule10 = ctrl.Rule(impact['high'] & gdpr_compliance['unknown'], risk['high'])
    rule11 = ctrl.Rule(impact['high'] & gdpr_compliance['non_compliant'], risk['critical'])

    # Create the control system and simulation
    risk_ctrl = ctrl.ControlSystem([rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11])
    risk_simulation = ctrl.ControlSystemSimulation(risk_ctrl)

    # Set input values
    risk_simulation.input['impact'] = impact_value
    risk_simulation.input['gdpr_compliance'] = gdpr_compliance_value

    # Compute the result
    risk_simulation.compute()

    # Get the calculated risk
    calculated_risk = risk_simulation.output['risk']
    
    # Determine the risk level
    if calculated_risk < 0.1:
        risk_level = 'None'
    elif 0.1 <= calculated_risk <= 0.39:
        risk_level = 'Low'
    elif 0.4 <= calculated_risk <= 0.69:
        risk_level = 'Medium'
    elif 0.7 <= calculated_risk <= 0.89:
        risk_level = 'High'
    elif 0.9 <= calculated_risk <= 1.0:
        risk_level = 'Critical'
    else:
        risk_level = 'Undefined'

    return calculated_risk, risk_level

def main():
    import sys
    # Check command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python fuzzy_system.py <impact> <gdpr_compliance>")
        sys.exit(1)

    try:
        impact_value = float(sys.argv[1])
        gdpr_compliance_value = float(sys.argv[2])
    except ValueError:
        print("Error: Impact and GDPR compliance values must be numeric.")
        sys.exit(1)

    # Call the compute_risk function
    calculated_risk, risk_level = calculate_risk(impact_value, gdpr_compliance_value)

    # Output the results
    print("Calculated Risk:", calculated_risk)
    print("Risk Level:", risk_level)

if __name__ == "__main__":
    main()
