导入pandas为pd
导入 numpy 为 np
从 sklearn.model_selection 导入 train_test_split
从 sklearn.preprocessing 导入 StandardScaler
从 sklearn.svm 导入 SVC
从 sklearn.neighbors 导入 KNeighborsClassifier
从 sklearn.ensemble 导入 随机森林分类器
从 sklearn.metrics 导入 accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
导入 matplotlib.pyplot 为 plt

data = pd.read_csv('data/train.csv')
df = 数据.复制()
df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'], inplace=True)
df.dropna(inplace=True)
df = pd.get_dummies(df, columns=['Sex', 'Embarked'])
X = df.drop('Survived', axis=1)
y = df['幸存者'输入：]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
输入：）
scaler = 标准缩放器()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm_model = SVC(kernel='rbf', C=1.0, gamma='scale', random_state=42)
svm_model.拟合(X_train_scaled, y_train)

knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.拟合(X_train_scaled, y_train)

rf_model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf_model.拟合(X_train, y_train)

def evaluate_model(model, X_train, X_test, y_train, y_test, model_name, scaled=True):
    如果 缩放：
        y_train_pred = model.预测(X_train)
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
