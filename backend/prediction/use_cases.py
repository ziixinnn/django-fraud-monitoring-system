from .apps import get_model
from .models import Prediction
from .dataclass import ModelInputData, ModelPredictionOutput

def predict(transaction, snapshot):
    model_input_data = ModelInputData(
        timestamp=transaction.timestamp,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        oldBalanceOrig=snapshot["oldBalanceOrig"],
        newBalanceOrig=snapshot["newBalanceOrig"],
        oldBalanceDest=snapshot["oldBalanceDest"],
        newBalanceDest=snapshot["newBalanceDest"],
    ).to_model_input_format()

    model = get_model()

    risk_score = model.predict_proba(model_input_data)[0][1]

    fraud_label = ModelPredictionOutput.transform_to_fraud_label(
        risk_score
    )

    return Prediction.objects.create(
        transaction=transaction,
        risk_score=float(risk_score),
        fraud_label=fraud_label,
    )


