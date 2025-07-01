import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt

data = pd.read_csv('data/train.csv')
df = data.copy()
df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'], inplace=True)
df.dropna(inplace=True)
df = pd.get_dummies(df, columns=['Sex', 'Embarked'])
X = df.drop('Survived', axis=1)
y = df['Survived']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm_model.fit(X_train_scaled, y_train)

knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train_scaled, y_train)

rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_model.fit(X_train, y_train)

def evaluate_model(model, X_train, X_test, y_train, y_test, model_name, scaled=True):
    if scaled:
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
    else:
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
    
    metrics = {
        '训练集准确率': accuracy_score(y_train, y_train_pred),
        '测试集准确率': accuracy_score(y_test, y_test_pred),
        '测试集精确率': precision_score(y_test, y_test_pred),
        '测试集召回率': recall_score(y_test, y_test_pred),
        '测试集F1分数': f1_score(y_test, y_test_pred),
        '混淆矩阵': confusion_matrix(y_test, y_test_pred)
    }
    
    print(f"\n{model_name} 性能:")
    print(f"训练集准确率: {metrics['训练集准确率']:.4f}")
    print(f"测试集准确率: {metrics['测试集准确率']:.4f}")
    print(f"测试集精确率: {metrics['测试集精确率']:.4f}")
    print(f"测试集召回率: {metrics['测试集召回率']:.4f}")
    print(f"测试集F1分数: {metrics['测试集F1分数']:.4f}")
    print("混淆矩阵:")
    print(metrics['混淆矩阵'])
    
    return metrics

svm_metrics = evaluate_model(svm_model, X_train_scaled, X_test_scaled, 
                             y_train, y_test, "SVM模型")
knn_metrics = evaluate_model(knn_model, X_train_scaled, X_test_scaled, 
                             y_train, y_test, "KNN模型")
rf_metrics = evaluate_model(rf_model, X_train, X_test, 
                            y_train, y_test, "随机森林模型", scaled=False)

print("\n=== 模型性能比较 ===")
print(f"模型\t\t测试集准确率\tF1分数")
print(f"SVM\t\t{svm_metrics['测试集准确率']:.4f}\t\t{svm_metrics['测试集F1分数']:.4f}")
print(f"KNN\t\t{knn_metrics['测试集准确率']:.4f}\t\t{knn_metrics['测试集F1分数']:.4f}")
print(f"随机森林\t{rf_metrics['测试集准确率']:.4f}\t\t{rf_metrics['测试集F1分数']:.4f}")

feature_importances = rf_model.feature_importances_
features = X.columns
importance_df = pd.DataFrame({
    '特征': features,
    '重要性': feature_importances
}).sort_values('重要性', ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(importance_df['特征'], importance_df['重要性'])
plt.xlabel('特征重要性')
plt.title('随机森林特征重要性分析')
plt.gca().invert_yaxis()
plt.show()