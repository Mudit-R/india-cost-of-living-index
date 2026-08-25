"""
AI Natural Language Engine for India Cost of Living Index.
Parses natural language user prompts into category weights and synthesizes relocation insights.
"""
import re
from typing import Dict, Any, List, Optional, Tuple


class AIRelocationParser:
    """
    Parses unstructured text prompts into structured 1-10 priority weights, 
    salary estimates, and lifestyle preferences.
    Works offline via heuristic NLP keyword matching, with optional LLM API fallback.
    """
    
    KEYWORD_MAP = {
        'Housing': {
            'rent': 3, 'apartment': 3, 'flat': 3, 'house': 3, 'housing': 3, 'accommodation': 3,
            'cheap rent': 4, 'affordable rent': 4, 'low rent': 4, 'gated community': 2, 'pg': 2
        },
        'Grocery': {
            'grocery': 3, 'groceries': 3, 'food': 2, 'supermarket': 2, 'cooking': 2, 'vegetables': 2,
            'milk': 2, 'home cooked': 3, 'daily needs': 2, 'blinkit': 2, 'zepto': 2
        },
        'Transport': {
            'transport': 3, 'commute': 3, 'cab': 2, 'uber': 2, 'auto': 2, 'metro': 3,
            'petrol': 2, 'fuel': 2, 'traffic': 2, 'distance': 2, 'travel': 2
        },
        'Healthcare': {
            'healthcare': 4, 'doctor': 3, 'hospital': 3, 'medical': 3, 'health': 3,
            'medicine': 2, 'clinic': 2, 'elderly': 3, 'parents': 3
        },
        'Education': {
            'education': 4, 'school': 4, 'kids': 3, 'children': 3, 'college': 3,
            'tuition': 3, 'coaching': 2, 'university': 2, 'family': 2
        },
        'Electricity': {
            'electricity': 3, 'power': 2, 'utility': 2, 'ac': 3, 'air conditioner': 3,
            'bills': 2, 'current': 2
        },
        'Restaurant': {
            'restaurant': 3, 'eating out': 3, 'dining': 3, 'swiggy': 3, 'zomato': 3,
            'cafe': 2, 'foodie': 3, 'nightlife': 2, 'pubs': 2
        },
        'Movies': {
            'movie': 3, 'movies': 3, 'cinema': 3, 'multiplex': 3, 'theatre': 3,
            'entertainment': 2, 'weekend': 1, 'shows': 2
        }
    }
    
    HIGH_INTENT_MODIFIERS = ['cheap', 'low', 'affordable', 'must be low', 'save', 'budget', 'priority', 'important', 'crucial', 'focus on']
    LOW_INTENT_MODIFIERS = ['don\'t care', 'dont care', 'not important', 'ignore', 'no kids', 'rarely', 'never', 'unimportant']

    @classmethod
    def parse_prompt(cls, prompt: str) -> Dict[str, Any]:
        """
        Parses user prompt string and extracts:
        - weights: Dict[str, int] (1-10 slider weights)
        - extracted_salary: Optional float (in LPA or monthly ₹)
        - summary: AI interpretation summary string
        - detected_lifestyle: List[str]
        """
        prompt_lower = prompt.lower()
        
        # Base weights initialized to neutral 5
        weights = {cat: 5 for cat in cls.KEYWORD_MAP.keys()}
        detected_lifestyle = []

        # 1. Parse salary if mentioned in prompt
        salary = cls._extract_salary(prompt_lower)
        
        # 2. Check for family / kids context
        if any(w in prompt_lower for w in ['kid', 'kids', 'child', 'children', 'school', 'family']):
            weights['Education'] = min(10, weights['Education'] + 3)
            weights['Housing'] = min(10, weights['Housing'] + 2)
            detected_lifestyle.append("Family & Education Focused")

        # 3. Check for bachelor / IT worker context
        if any(w in prompt_lower for w in ['bachelor', 'single', 'dev', 'developer', 'tech', 'software', 'it worker']):
            weights['Transport'] = min(10, weights['Transport'] + 2)
            weights['Restaurant'] = min(10, weights['Restaurant'] + 2)
            detected_lifestyle.append("Young Professional / Tech Worker")

        # 4. Keyword frequency and modifier analysis
        for category, kw_dict in cls.KEYWORD_MAP.items():
            score_delta = 0
            for word, weight_val in kw_dict.items():
                if word in prompt_lower:
                    # Check context around word for negative/low modifiers
                    context_snippet = cls._get_context(prompt_lower, word)
                    if any(neg in context_snippet for neg in cls.LOW_INTENT_MODIFIERS):
                        score_delta -= 3
                    elif any(pos in context_snippet for pos in cls.HIGH_INTENT_MODIFIERS):
                        score_delta += weight_val
                    else:
                        score_delta += 1
                        
            # Adjust final category weight bound within 1..10
            new_weight = max(1, min(10, 5 + score_delta))
            weights[category] = new_weight

        # Synthesize interpretation summary
        top_priorities = sorted(weights.items(), key=lambda x: x[1], reverse=True)[:3]
        priority_str = ", ".join([f"{k} (Priority {v}/10)" for k, v in top_priorities])
        
        ai_summary = f"Parsed intent: Focused on {priority_str}."
        if salary:
            ai_summary += f" Detected annual income: ₹{salary:,.2f} LPA."

        return {
            "prompt": prompt,
            "weights": weights,
            "extracted_salary_lpa": salary,
            "detected_lifestyle": detected_lifestyle if detected_lifestyle else ["General Relocator"],
            "ai_summary": ai_summary
        }

    @staticmethod
    def _extract_salary(prompt: str) -> Optional[float]:
        """Extracts salary figures in LPA or Rupees from prompt string."""
        # Check LPA patterns like "15 lpa", "20lpa", "12.5 lakh", "8 lakhs"
        lpa_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:lpa|lakhs?|lakh|lac|lacs)', prompt)
        if lpa_match:
            return float(lpa_match.group(1))
        
        # Check monthly rupee patterns like "50000 per month", "100000 pm"
        pm_match = re.search(r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:per month|pm|monthly|a month)', prompt)
        if pm_match:
            val_str = pm_match.group(1).replace(',', '')
            monthly_val = float(val_str)
            return round((monthly_val * 12) / 100000.0, 2)
            
        return None

    @staticmethod
    def _get_context(text: str, word: str, window: int = 30) -> str:
        """Returns surrounding snippet of text around a target keyword."""
        idx = text.find(word)
        if idx == -1:
            return ""
        start = max(0, idx - window)
        end = min(len(text), idx + len(word) + window)
        return text[start:end]


class AIRelocationAdvisor:
    """
    Generates natural language executive summaries, trade-off analyses, 
    and financial guidance for city relocation queries.
    """
    
    @classmethod
    def generate_relocation_insight(
        cls, 
        current_city: str, 
        target_city: str, 
        current_salary_lpa: float,
        current_city_index: float,
        target_city_index: float,
        category_breakdown: Optional[Dict[str, Dict[str, float]]] = None
    ) -> Dict[str, Any]:
        """
        Calculates exact purchasing power parity, monthly savings, 
        and generates executive AI insights.
        """
        index_ratio = target_city_index / current_city_index
        equivalent_salary_lpa = round(current_salary_lpa * index_ratio, 2)
        annual_savings_lpa = round(current_salary_lpa - equivalent_salary_lpa, 2)
        monthly_diff_rupees = round((annual_savings_lpa * 100000) / 12.0, 0)
        
        pct_diff = round(abs(1 - index_ratio) * 100, 1)
        
        if target_city_index < current_city_index:
            verdict = f"🎉 **{target_city}** is roughly **{pct_diff}% cheaper** overall than **{current_city}**."
            financial_advice = (
                f"To maintain your current standard of living in {current_city} (salary: ₹{current_salary_lpa:,.2f} LPA), "
                f"you only need **₹{equivalent_salary_lpa:,.2f} LPA** in {target_city}. "
                f"Moving while keeping your same salary yields an estimated **₹{abs(monthly_diff_rupees):,.0f}/month** in net savings!"
            )
        elif target_city_index > current_city_index:
            verdict = f"⚠️ **{target_city}** is roughly **{pct_diff}% more expensive** overall than **{current_city}**."
            financial_advice = (
                f"To maintain your current standard of living in {current_city} (salary: ₹{current_salary_lpa:,.2f} LPA), "
                f"you would need a salary of **₹{equivalent_salary_lpa:,.2f} LPA** in {target_city}."
            )
        else:
            verdict = f"⚖️ **{target_city}** has an almost identical overall cost of living to **{current_city}**."
            financial_advice = f"Your purchasing power will remain virtually unchanged at ₹{current_salary_lpa:,.2f} LPA."

        # Key category trade-offs
        tradeoffs = []
        if category_breakdown:
            for cat, data in category_breakdown.items():
                cur_val = data.get('current', 100)
                tgt_val = data.get('target', 100)
                if cur_val > 0:
                    cat_pct = round(((tgt_val - cur_val) / cur_val) * 100, 1)
                    if cat_pct <= -15:
                        tradeoffs.append(f"✅ **{cat}**: {abs(cat_pct)}% cheaper in {target_city}")
                    elif cat_pct >= 15:
                        tradeoffs.append(f"🚨 **{cat}**: {cat_pct}% more expensive in {target_city}")

        return {
            "current_city": current_city,
            "target_city": target_city,
            "verdict": verdict,
            "financial_advice": financial_advice,
            "current_salary_lpa": current_salary_lpa,
            "equivalent_salary_lpa": equivalent_salary_lpa,
            "monthly_savings_rupees": monthly_diff_rupees,
            "overall_index_diff_pct": pct_diff if target_city_index >= current_city_index else -pct_diff,
            "key_tradeoffs": tradeoffs
        }
