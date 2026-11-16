import csv
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


ROOT = Path(__file__).resolve().parents[2]
rows = list(csv.DictReader((ROOT / "data/router_samples.csv").open(encoding="utf-8", newline=""), skipinitialspace=True))
X = [row["text"] for row in rows]
y = [row["label"] for row in rows]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, stratify=y, random_state=30
)
model = Pipeline([
    ("tfid", TfidfVectorizer(ngram_range=(1,2), min_df=1)),
    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
])
model.fit(X_train, y_train)
pred = model.predict(X_test)
print(classification_report(y_test, pred, zero_division=0))
print("Confusion matrix:", confusion_matrix(y_test,pred))
output = ROOT / "models/intent_router.joblib"
output.parent.mkdir(exist_ok=True)
joblib.dump(model, output)
print("Saved", output)
