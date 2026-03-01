from dataclasses import dataclass
import numpy as np
import pandas as pd
from django.utils import timezone

SYSTEM_START = timezone.make_aware(
    timezone.datetime(2024, 1, 1, 0, 0, 0)
)

def compute_step(ts):
    delta = ts - SYSTEM_START
    return int(delta.total_seconds() // 3600)

@dataclass (frozen=True)
class ModelInputData:
    amount: float
    transaction_type: str
    oldBalanceOrig: float
    newBalanceOrig: float
    oldBalanceDest: float
    newBalanceDest: float
    timestamp: object

    def to_model_input_format(self) -> pd.DataFrame:

        if self.transaction_type == "TRANSFER":
            tx_type= 0
        elif self.transaction_type == "CASH_OUT":
            tx_type = 1
        
        amount = float(self.amount)
        obo= float(self.oldBalanceOrig)
        nbo = float(self.newBalanceOrig)
        obd = float(self.oldBalanceDest)
        nbd = float(self.newBalanceDest)

        if obd == 0 and nbd == 0 and amount != 0:
            obd, nbd = 1.0, -1.0

        if obo == 0 and nbo == 0 and amount != 0:
            obo, nbo = np.nan, np.nan

        errorBalanceOrig = (
            np.nan if np.isnan(obo) else nbo + amount - obo
        )
        errorBalanceDest = obd + amount - nbd

        step = compute_step(self.timestamp)

        return pd.DataFrame([{
            "step": step,
            "type": tx_type,
            "amount": amount,
            "oldBalanceOrig": obo,
            "newBalanceOrig": nbo,
            "oldBalanceDest": obd,
            "newBalanceDest": nbd,
            "errorBalanceOrig": errorBalanceOrig,
            "errorBalanceDest": errorBalanceDest,
        }])
    
@dataclass (frozen=True)
class ModelPredictionOutput:
    risk_score: float
    fraud_label: str

    def transform_to_fraud_label(risk_score: float) -> str:
        if risk_score is None:
            return "LEGIT" 

        return "FRAUD" if risk_score >= 0.5 else "LEGIT"
    