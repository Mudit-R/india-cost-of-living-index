"""
Purchasing Power Parity (PPP) & Salary Swap Calculator Engine.
Calculates equivalent salaries and monthly expense differences between Indian cities.
"""
from typing import Dict, Any, Optional
import pandas as pd


class SalarySwapCalculator:
    """
    Calculates exact salary equivalence and purchasing power parity between any two cities.
    """

    def __init__(self, cost_df: pd.DataFrame):
        self.df = cost_df.copy()

    def calculate_salary_swap(
        self,
        current_city: str,
        target_city: str,
        current_salary_lpa: float
    ) -> Dict[str, Any]:
        """
        Calculates equivalent salary in target city to maintain identical lifestyle.
        """
        cur_match = self.df[self.df['City'].str.lower() == current_city.lower()]
        tgt_match = self.df[self.df['City'].str.lower() == target_city.lower()]

        if cur_match.empty or tgt_match.empty:
            raise ValueError(f"One or both cities ('{current_city}', '{target_city}') not found in dataset.")

        cur_row = cur_match.iloc[0]
        tgt_row = tgt_match.iloc[0]

        cur_index = float(cur_row['cost_of_living_index'])
        tgt_index = float(tgt_row['cost_of_living_index'])

        ratio = tgt_index / cur_index
        equivalent_salary_lpa = round(current_salary_lpa * ratio, 2)
        annual_diff_lpa = round(current_salary_lpa - equivalent_salary_lpa, 2)
        monthly_diff_rupees = round((annual_diff_lpa * 100000.0) / 12.0, 0)
        pct_change = round(((tgt_index - cur_index) / cur_index) * 100.0, 1)

        category_breakdown = {}
        from website.recommender import CATEGORIES, CATEGORY_TO_COLUMN
        for cat in CATEGORIES:
            col = CATEGORY_TO_COLUMN[cat]
            cur_cat_val = float(cur_row[col])
            tgt_cat_val = float(tgt_row[col])
            cat_pct = round(((tgt_cat_val - cur_cat_val) / cur_cat_val) * 100.0, 1)
            category_breakdown[cat] = {
                "current_index": cur_cat_val,
                "target_index": tgt_cat_val,
                "diff_pct": cat_pct
            }

        return {
            "current_city": cur_row['City'],
            "target_city": tgt_row['City'],
            "current_salary_lpa": current_salary_lpa,
            "equivalent_salary_lpa": equivalent_salary_lpa,
            "annual_difference_lpa": annual_diff_lpa,
            "monthly_savings_rupees": monthly_diff_rupees,
            "cost_of_living_diff_pct": pct_change,
            "category_breakdown": category_breakdown
        }
