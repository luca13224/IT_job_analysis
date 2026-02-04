"""
Machine Learning Models for Salary Prediction
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import lightgbm as lgb
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(str(Path(__file__).parent.parent.parent))
from config.config import CLEAN_CSV_PATH, MODELS_DIR, OUTPUTS_DIR


class SalaryPredictor:
    """Machine Learning model for predicting IT job salaries"""
    
    def __init__(self):
        self.model = None
        self.feature_columns = []
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_importance = None
        
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for ML model"""
        print("🔧 Preparing features...")
        
        # Filter rows with salary data
        df_ml = df[df['salary_numeric'].notna()].copy()
        
        if len(df_ml) == 0:
            raise ValueError("No salary data available for training")
        
        # Basic features
        features = df_ml[['job_group', 'level', 'city']].copy()
        
        # Encode categorical variables
        for col in ['job_group', 'level', 'city']:
            le = LabelEncoder()
            features[f'{col}_encoded'] = le.fit_transform(features[col].astype(str))
            self.label_encoders[col] = le
        
        # Count skills
        import ast
        def count_skills(skills_str):
            try:
                skills = ast.literal_eval(skills_str) if isinstance(skills_str, str) else []
                return len(skills) if isinstance(skills, list) else 0
            except:
                return 0
        
        if 'array_skills' in df_ml.columns:
            features['skill_count'] = df_ml['array_skills'].apply(count_skills)
        else:
            features['skill_count'] = 0
        
        # Has specific high-value skills
        high_value_skills = ['aws', 'kubernetes', 'machine learning', 'ai', 'golang', 
                             'react', 'vue', 'docker', 'python', 'java']
        
        for skill in high_value_skills:
            features[f'has_{skill.replace(" ", "_")}'] = df_ml['array_skills'].apply(
                lambda x: 1 if skill in str(x).lower() else 0
            )
        
        # Target variable
        features['salary'] = df_ml['salary_numeric']
        
        # Store feature columns (excluding target)
        self.feature_columns = [col for col in features.columns if col not in 
                               ['salary', 'job_group', 'level', 'city']]
        
        print(f"✓ Prepared {len(features)} samples with {len(self.feature_columns)} features")
        
        return features
    
    def train_model(self, df: pd.DataFrame, model_type='xgboost'):
        """Train salary prediction model"""
        print(f"\n🚀 Training {model_type} model...")
        
        # Prepare features
        features = self.prepare_features(df)
        
        # Split features and target
        X = features[self.feature_columns]
        y = features['salary']
        
        # Train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"Training set: {len(X_train)} samples")
        print(f"Test set: {len(X_test)} samples")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model based on type
        if model_type == 'random_forest':
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_train, y_train)
            
        elif model_type == 'gradient_boosting':
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
            self.model.fit(X_train, y_train)
            
        elif model_type == 'xgboost':
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=7,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_train, y_train)
            
        elif model_type == 'lightgbm':
            self.model = lgb.LGBMRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=7,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
            self.model.fit(X_train, y_train)
        
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Predictions
        y_train_pred = self.model.predict(X_train)
        y_test_pred = self.model.predict(X_test)
        
        # Evaluate
        train_metrics = self._evaluate(y_train, y_train_pred, "Training")
        test_metrics = self._evaluate(y_test, y_test_pred, "Test")
        
        # Feature importance
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importance = pd.DataFrame({
                'feature': self.feature_columns,
                'importance': self.model.feature_importances_
            }).sort_values('importance', ascending=False)
        
        print("\n✅ Model training completed!")
        
        return {
            'train_metrics': train_metrics,
            'test_metrics': test_metrics,
            'feature_importance': self.feature_importance
        }
    
    def _evaluate(self, y_true, y_pred, dataset_name):
        """Evaluate model performance"""
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        print(f"\n📊 {dataset_name} Metrics:")
        print(f"  RMSE: {rmse/1_000_000:.2f}M VND")
        print(f"  MAE:  {mae/1_000_000:.2f}M VND")
        print(f"  R² Score: {r2:.4f}")
        
        return {
            'rmse': rmse,
            'mae': mae,
            'r2': r2
        }
    
    def predict_salary(self, job_group: str, level: str, city: str, 
                      skills: list = None) -> dict:
        """Predict salary for a job configuration"""
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model() first.")
        
        # Prepare input
        input_data = pd.DataFrame({
            'job_group_encoded': [self.label_encoders['job_group'].transform([job_group])[0]],
            'level_encoded': [self.label_encoders['level'].transform([level])[0]],
            'city_encoded': [self.label_encoders['city'].transform([city])[0]],
            'skill_count': [len(skills) if skills else 0],
        })
        
        # Add skill flags
        high_value_skills = ['aws', 'kubernetes', 'machine learning', 'ai', 'golang',
                            'react', 'vue', 'docker', 'python', 'java']
        
        skills_lower = [s.lower() for s in skills] if skills else []
        for skill in high_value_skills:
            input_data[f'has_{skill.replace(" ", "_")}'] = 1 if skill in skills_lower else 0
        
        # Ensure all features are present
        for col in self.feature_columns:
            if col not in input_data.columns:
                input_data[col] = 0
        
        input_data = input_data[self.feature_columns]
        
        # Predict
        predicted_salary = self.model.predict(input_data)[0]
        
        return {
            'predicted_salary': predicted_salary,
            'predicted_salary_m': predicted_salary / 1_000_000,
            'job_group': job_group,
            'level': level,
            'city': city,
            'skills': skills
        }
    
    def plot_feature_importance(self, top_n=15, save_path=None):
        """Plot feature importance"""
        if self.feature_importance is None:
            print("⚠️  No feature importance available")
            return
        
        plt.figure(figsize=(10, 6))
        top_features = self.feature_importance.head(top_n)
        
        plt.barh(top_features['feature'], top_features['importance'])
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        plt.title(f'Top {top_n} Most Important Features')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved plot to {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def save_model(self, filename='salary_predictor.pkl'):
        """Save trained model"""
        model_path = MODELS_DIR / filename
        
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_importance': self.feature_importance
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"✓ Model saved to {model_path}")
    
    def load_model(self, filename='salary_predictor.pkl'):
        """Load trained model"""
        model_path = MODELS_DIR / filename
        
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.feature_columns = model_data['feature_columns']
        self.label_encoders = model_data['label_encoders']
        self.scaler = model_data['scaler']
        self.feature_importance = model_data['feature_importance']
        
        print(f"✓ Model loaded from {model_path}")
    
    def compare_models(self, df: pd.DataFrame):
        """Compare different ML models"""
        print("\n🔬 Comparing multiple models...\n")
        
        models = {
            'Random Forest': 'random_forest',
            'Gradient Boosting': 'gradient_boosting',
            'XGBoost': 'xgboost',
            'LightGBM': 'lightgbm'
        }
        
        results = []
        
        for name, model_type in models.items():
            print(f"\n{'='*60}")
            print(f"Training {name}...")
            print('='*60)
            
            predictor = SalaryPredictor()
            metrics = predictor.train_model(df, model_type=model_type)
            
            results.append({
                'Model': name,
                'Train R²': metrics['train_metrics']['r2'],
                'Test R²': metrics['test_metrics']['r2'],
                'Test RMSE (M VND)': metrics['test_metrics']['rmse'] / 1_000_000,
                'Test MAE (M VND)': metrics['test_metrics']['mae'] / 1_000_000,
            })
        
        # Create comparison DataFrame
        comparison_df = pd.DataFrame(results)
        
        print("\n" + "="*60)
        print("📊 MODEL COMPARISON RESULTS")
        print("="*60)
        print(comparison_df.to_string(index=False))
        
        # Plot comparison
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # R² comparison
        comparison_df.plot(
            x='Model', 
            y=['Train R²', 'Test R²'],
            kind='bar',
            ax=axes[0],
            title='R² Score Comparison'
        )
        axes[0].set_ylabel('R² Score')
        axes[0].set_xlabel('')
        axes[0].legend(['Train', 'Test'])
        axes[0].set_ylim([0, 1])
        
        # Error comparison
        comparison_df.plot(
            x='Model',
            y='Test RMSE (M VND)',
            kind='bar',
            ax=axes[1],
            title='Test Error Comparison',
            legend=False,
            color='orange'
        )
        axes[1].set_ylabel('RMSE (Million VND)')
        axes[1].set_xlabel('')
        
        plt.tight_layout()
        
        save_path = OUTPUTS_DIR / "model_comparison.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\n✓ Comparison plot saved to {save_path}")
        
        plt.close()
        
        return comparison_df


if __name__ == "__main__":
    # Load data
    print("📂 Loading data...")
    df = pd.read_csv(CLEAN_CSV_PATH)
    print(f"✓ Loaded {len(df)} records")
    
    # Create output directories
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Compare models
    predictor = SalaryPredictor()
    comparison = predictor.compare_models(df)
    
    # Train best model (typically XGBoost or LightGBM)
    print("\n" + "="*60)
    print("Training final model...")
    print("="*60)
    
    final_predictor = SalaryPredictor()
    final_predictor.train_model(df, model_type='xgboost')
    
    # Save model
    final_predictor.save_model()
    
    # Plot feature importance
    final_predictor.plot_feature_importance(
        save_path=OUTPUTS_DIR / "feature_importance.png"
    )
    
    # Example predictions
    print("\n" + "="*60)
    print("🎯 Example Predictions")
    print("="*60)
    
    examples = [
        {
            'job_group': 'Backend Developer',
            'level': 'senior',
            'city': 'Ho Chi Minh',
            'skills': ['python', 'django', 'aws', 'docker', 'kubernetes']
        },
        {
            'job_group': 'Data / AI',
            'level': 'mid',
            'city': 'Ha Noi',
            'skills': ['python', 'machine learning', 'tensorflow', 'sql']
        },
        {
            'job_group': 'Frontend Developer',
            'level': 'junior',
            'city': 'Da Nang',
            'skills': ['react', 'javascript', 'html', 'css']
        }
    ]
    
    for example in examples:
        prediction = final_predictor.predict_salary(**example)
        print(f"\n{example['job_group']} ({example['level']}) in {example['city']}")
        print(f"Skills: {', '.join(example['skills'])}")
        print(f"💰 Predicted Salary: {prediction['predicted_salary_m']:.2f} Million VND")
    
    print("\n✅ All done!")
