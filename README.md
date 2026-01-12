# Diet Optimization Using Linear Programming
This project formulates and solves a diet optimization problem using **linear programming** to identify the lowest-cost daily diet that satisfies nutritional requirements while respecting real-world selection constraints.

The model is implemented in **Python using PuLP** and demonstrates how optimization techniques can be applied to practical decision-making problems.

---

## Problem Overview
The goal is to minimize the total daily cost of food intake while meeting minimum and maximum nutritional requirements across multiple nutrients. Additional constraints are introduced to improve realism, such as minimum serving sizes, mutually exclusive food choices, and dietary variety requirements.

---

## Dataset
- **Source:** Diet problem dataset (`diet.xls`)
- **Contents:**
  - Food items with cost per serving
  - Nutritional values for 11 nutrients
  - Minimum and maximum daily nutrient requirements

---

## Optimization Model
### Objective Function
- Minimize total daily cost of selected foods

### Decision Variables
- Continuous variables for food serving quantities
- Binary variables indicating whether a food is selected

---

## Constraints Implemented
1. **Nutritional Constraints**
   - All 11 nutrients must fall within specified minimum and maximum bounds

2. **Minimum Serving Constraint**
   - If a food is selected, at least 0.1 servings must be chosen  
   - Implemented using binary variables and the Big-M method

3. **Mutually Exclusive Foods**
   - At most one of Celery or Frozen Broccoli can be selected

4. **Protein Variety Constraint**
   - Exactly 3 food items must be selected from the meat/poultry/fish/egg category

---

## Results Summary
- **Optimal daily cost:** \$4.51
- **Number of foods selected:** 8
- Nutritional constraints were fully satisfied
- Several nutrients reached their upper bounds, indicating binding constraints
- The solution highlights the need for additional realism constraints in real-world diet planning

---

## Key Takeaways
- Linear programming is effective for cost-based decision optimization
- Binary variables enable logical and selection-based constraints
- Purely mathematical optima may be impractical without domain-specific limits
- Model interpretability is essential when applying optimization in real contexts

---

## Technologies Used
- Python
- PuLP
- Pandas
- Excel data handling

---

## How to Run
1. Install dependencies:
   ```bash
   pip install pulp pandas
2. Run the optimization script:
   ```bash
    python diet_optimization.py
   
## Conclusion
This project demonstrates how optimization models can solve complex resource allocation problems while balancing cost, feasibility, and constraint design. It serves as a practical example of applying operations research techniques using Python.
