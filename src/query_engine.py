import re
from typing import Dict, Optional, Tuple, List, Any
import pandas as pd

# --------------------------------
# State abbrev ↔ full name mapping
# --------------------------------
US_ABBR_TO_STATE = {
    "AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado",
    "CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho",
    "IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana",
    "ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi",
    "MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey",
    "NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma",
    "OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota",
    "TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington",
    "WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming","DC":"District Of Columbia"
}

# -------------------------------
# Robust CSV Loader + Normalizer
# -------------------------------
def _load_sales(csv_path: str) -> pd.DataFrame:
    """Load Superstore-like CSV with fallback encodings and normalized columns."""
    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin1"]
    df = None
    for enc in encodings:
        try:
            df = pd.read_csv(csv_path, encoding=enc)
            break
        except Exception:
            continue
    if df is None:
        raise ValueError("Could not read CSV file with common encodings.")

    # Clean headers
    df.columns = [c.strip() for c in df.columns]

    # Canonical rename map
    rename_map = {
        "Order Date": "OrderDate",
        "OrderDate": "OrderDate",
        "Region": "Region",
        "State": "State",
        "Category": "Category",
        "Sales": "Sales",
        "Profit": "Profit",
        "Sub-Category": "Sub-Category",
        "Product Name": "Product",
        "Product": "Product",
    }
    for src, dst in rename_map.items():
        if src in df.columns:
            df = df.rename(columns={src: dst})

    # Build product name fallback
    if "Product" not in df.columns:
        if "Sub-Category" in df.columns:
            df["Product"] = df["Sub-Category"]

    # Numeric coercion
    for col in ["Sales", "Profit"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Parse date
    if "OrderDate" in df.columns:
        parsed = pd.to_datetime(df["OrderDate"], errors="coerce", dayfirst=True)
        mask_nat = parsed.isna()
        if mask_nat.any():
            parsed2 = pd.to_datetime(df.loc[mask_nat, "OrderDate"], errors="coerce", dayfirst=False)
            parsed.loc[mask_nat] = parsed2
        df["OrderDate"] = parsed

        df["Year"] = df["OrderDate"].dt.year
        df["Month"] = df["OrderDate"].dt.month
        df["MonthName"] = df["OrderDate"].dt.strftime("%b")
        df["MonthIndex"] = df["OrderDate"].dt.month

    return df


# -------------------------------
# Query Engine
# -------------------------------
class SalesQueryEngine:
    def __init__(self, csv_path: str = "data/Sample - Superstore.csv"):
        self.csv_path = csv_path
        self.df = _load_sales(csv_path)
        if self.df.empty:
            raise ValueError("Loaded dataset is empty.")
        if "OrderDate" in self.df.columns:
            self.today = self.df["OrderDate"].max().normalize()
        else:
            self.today = pd.Timestamp.today().normalize()

    # --------- NLP DETECTORS ---------
    @staticmethod
    def _detect_metric(q: str) -> str:
        return "Profit" if "profit" in q.lower() else "Sales"

    def _detect_time_window(self, q: str) -> Optional[Tuple[pd.Timestamp, pd.Timestamp]]:
        ql = q.lower()
        today = self.today

        if "last month" in ql:
            first_this = today.replace(day=1)
            start = (first_this - pd.offsets.MonthBegin(1)).normalize()
            end = (first_this - pd.offsets.Day(1)).normalize()
            return start, end

        if "this year" in ql or "ytd" in ql:
            start = pd.Timestamp(year=today.year, month=1, day=1)
            return start, today

        if "last year" in ql:
            y = today.year - 1
            return pd.Timestamp(year=y, month=1, day=1), pd.Timestamp(year=y, month=12, day=31)

        m = re.search(r"(?:in|for)?\s*(20\d{2}|19\d{2})", ql)
        if m:
            y = int(m.group(1))
            return pd.Timestamp(year=y, month=1, day=1), pd.Timestamp(year=y, month=12, day=31)
        return None

    @staticmethod
    def _detect_dimension(q: str) -> Optional[str]:
        ql = q.lower()
        if " by region" in ql: return "Region"
        if " by state" in ql: return "State"
        if " by category" in ql or "categories" in ql: return "Category"
        if " by product" in ql or "sub category" in ql: return "Product"
        if " by month" in ql or "month-wise" in ql or "monthly" in ql: return "MonthName"
        return None

    @staticmethod
    def _detect_topn(q: str) -> Optional[Tuple[int, str]]:
        m = re.search(r"top\s+(\d+)\s+(categories|category|products|product|regions|states)", q.lower())
        if not m: return None
        n = int(m.group(1))
        word = m.group(2)
        if "region" in word: return n, "Region"
        if "state" in word: return n, "State"
        if "category" in word: return n, "Category"
        return n, "Product"

    @staticmethod
    def _detect_filters(q: str) -> Dict[str, str]:
        ql = q.lower()
        filters = {}
        found_state = False

        # Abbreviation first
        m_abbr = re.search(r"\bin\s+([a-z]{2})(?=\b|[^\w])", ql, flags=re.IGNORECASE)
        if m_abbr:
            abbr = m_abbr.group(1).upper()
            if abbr in US_ABBR_TO_STATE:
                filters["State"] = US_ABBR_TO_STATE[abbr]
                found_state = True

        # Full state only if abbreviation not found
        if not found_state:
            m_full = re.search(r"\bin\s+([a-z][a-z\s\-]+?)(?=\b|[^\w]|$)", ql, flags=re.IGNORECASE)
            if m_full:
                s = re.sub(r"[^\w\s\-]", "", m_full.group(1)).strip().title()
                if s:
                    filters["State"] = s

        # Category filter
        m_cat = re.search(r"\bcategory\s+([a-z][a-z\s\-]+)", ql, flags=re.IGNORECASE)
        if m_cat:
            cat = re.sub(r"[^\w\s\-]", "", m_cat.group(1)).strip().title()
            if cat:
                filters["Category"] = cat
        return filters

    # --------- CORE FUNCTIONS ---------
    def parse(self, q: str) -> Dict[str, Any]:
        return {
            "metric": self._detect_metric(q),
            "time_window": self._detect_time_window(q),
            "group_dim": self._detect_dimension(q),
            "topn": self._detect_topn(q),
            "filters": self._detect_filters(q)
        }

    def _apply_time(self, df: pd.DataFrame, t: Optional[Tuple[pd.Timestamp, pd.Timestamp]]) -> pd.DataFrame:
        if not t or "OrderDate" not in df.columns: return df
        start, end = t
        return df.loc[(df["OrderDate"] >= start) & (df["OrderDate"] <= end)]

    def _apply_filters(self, df: pd.DataFrame, filters: Dict[str, str]) -> pd.DataFrame:
        for col, val in filters.items():
            if col in df.columns:
                df = df[df[col].astype(str).str.lower() == val.lower()]
        return df

    def run(self, params: Dict[str, Any]) -> pd.DataFrame:
        df = self.df.copy()
        df = self._apply_time(df, params["time_window"])
        df = self._apply_filters(df, params["filters"])
        if df.empty: return df

        metric = params["metric"]
        group_dim = params["group_dim"]
        topn = params["topn"]

        if topn:
            n, dim = topn
            agg = df.groupby(dim, as_index=False)[metric].sum()
            return agg.sort_values(metric, ascending=False).head(n)

        if group_dim:
            agg = df.groupby(group_dim, as_index=False)[metric].sum()
            if group_dim == "MonthName" and "MonthIndex" in df.columns:
                month_map = df[["MonthName", "MonthIndex"]].drop_duplicates()
                agg = agg.merge(month_map, on="MonthName", how="left")
                agg = agg.sort_values("MonthIndex").drop(columns=["MonthIndex"])
            else:
                agg = agg.sort_values(metric, ascending=False)
            return agg.reset_index(drop=True)

        return pd.DataFrame({metric: [df[metric].sum()]})

    @staticmethod
    def _fmt_currency(x: float) -> str:
        return f"${x:,.2f}"

    def format_answer(self, params: Dict[str, Any], result: pd.DataFrame) -> str:
        metric, t, group_dim, topn, filters = (
            params["metric"], params["time_window"], params["group_dim"], params["topn"], params["filters"]
        )

        prefix = "Profit" if metric == "Profit" else "Sales"
        if "State" in filters: prefix += f" in {filters['State']}"
        if "Category" in filters: prefix += f" for {filters['Category']}"
        if t:
            prefix += f" ({t[0].date()} → {t[1].date()})"

        if result.empty:
            return f"{prefix}: no matching data."

        if group_dim or topn:
            dim = topn[1] if topn else group_dim
            parts = [f"{r[dim]}: {self._fmt_currency(r[metric])}" for _, r in result.iterrows()]
            return f"{prefix} by {dim} — " + "; ".join(parts) + "."
        return f"{prefix} — {self._fmt_currency(result.iloc[0][metric])}."


def ask_question(question: str, csv_path: str = "data/Sample - Superstore.csv") -> str:
    eng = SalesQueryEngine(csv_path)
    p = eng.parse(question)
    r = eng.run(p)
    return eng.format_answer(p, r)
