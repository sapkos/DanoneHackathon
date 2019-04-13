import numpy as np
import pandas as pd

def fit_model_with_changed_values(model, values_to_change, df):
    """
    values_to_change - dictionary with all variables used in model
        if we do not want to change value of variable it should be nan
    """

    values_to_change_copy = values_to_change.copy()
    for key, value in values_to_change.items():
        if np.isnan(value):
            values_to_change_copy[key] = df[key].sample(n=1).values[0]
    return model.predict(pd.DataFrame(values_to_change_copy, index=[0])), values_to_change_copy


MAX_EFF = 110
MIN_EFF = 98

def find_values_model_eff(model, values_to_change, df):
  """
  params:
      model -
      values_to_change - dictionary with all variables used in model
          if we do not want to change value of variable it should be nan
      df -
  return: optimal values of variables and efficiency
  """
  eff = 0
  i = 0
  while (MIN_EFF > eff or eff > MAX_EFF) and i < 100:
      eff, new_values = fit_model_with_changed_values(model, values_to_change, df)
      i = i + 1


  return new_values, eff
