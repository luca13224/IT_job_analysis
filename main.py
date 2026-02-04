"""
Main Pipeline - Run complete job market analysis
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from src.data_processing.processor import DataProcessor
from src.analysis.salary_analytics import SalaryAnalyzer
from src.nlp.skill_analyzer import SkillAnalyzer
from src.ml_models.salary_prediction import SalaryPredictor
from config.config import CLEAN_CSV_PATH, OUTPUTS_DIR


def run_data_processing():
    """Step 1: Process raw data"""
    print("\n" + "="*70)
    print("STEP 1: DATA PROCESSING")
    print("="*70)
    
    processor = DataProcessor()
    processor.process_pipeline()
    processor.get_summary()
    
    return processor.df


def run_salary_analysis(df):
    """Step 2: Analyze salary data"""
    print("\n" + "="*70)
    print("STEP 2: SALARY ANALYSIS")
    print("="*70)
    
    analyzer = SalaryAnalyzer(df)
    
    # Generate report
    report = analyzer.generate_report()
    print(report)
    
    # Save report
    report_path = OUTPUTS_DIR / "salary_analysis_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n✓ Report saved to {report_path}")
    
    # Create visualizations
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    analyzer.plot_salary_distribution(OUTPUTS_DIR / "salary_distribution.png")
    analyzer.plot_salary_trends(OUTPUTS_DIR / "salary_trends.png")
    
    print("\n✓ Salary analysis completed!")


def run_skill_analysis(df):
    """Step 3: Analyze skills"""
    print("\n" + "="*70)
    print("STEP 3: SKILL ANALYSIS")
    print("="*70)
    
    analyzer = SkillAnalyzer()
    
    # Analyze trends
    trends = analyzer.analyze_skill_trends(df)
    print("\n📈 Top 20 In-Demand Skills:")
    print(trends.head(20).to_string(index=False))
    
    # Save trends
    trends_path = OUTPUTS_DIR / "skill_trends.csv"
    trends.to_csv(trends_path, index=False, encoding='utf-8-sig')
    print(f"\n✓ Skill trends saved to {trends_path}")
    
    # Skill co-occurrence
    cooccur = analyzer.get_skill_cooccurrence(df)
    print("\n🔗 Top 10 Skill Pairs:")
    print(cooccur.head(10).to_string(index=False))
    
    # Save co-occurrence
    cooccur_path = OUTPUTS_DIR / "skill_cooccurrence.csv"
    cooccur.to_csv(cooccur_path, index=False, encoding='utf-8-sig')
    print(f"✓ Skill co-occurrence saved to {cooccur_path}")
    
    print("\n✓ Skill analysis completed!")


def run_ml_models(df):
    """Step 4: Train ML models"""
    print("\n" + "="*70)
    print("STEP 4: MACHINE LEARNING MODELS")
    print("="*70)
    
    # Compare models
    predictor = SalaryPredictor()
    comparison = predictor.compare_models(df)
    
    # Save comparison
    comparison_path = OUTPUTS_DIR / "model_comparison.csv"
    comparison.to_csv(comparison_path, index=False)
    print(f"\n✓ Model comparison saved to {comparison_path}")
    
    # Train final model
    final_predictor = SalaryPredictor()
    final_predictor.train_model(df, model_type='xgboost')
    final_predictor.save_model()
    final_predictor.plot_feature_importance(
        save_path=OUTPUTS_DIR / "feature_importance.png"
    )
    
    print("\n✓ ML models completed!")


def main():
    """Run complete pipeline"""
    print("\n" + "="*70)
    print("🚀 VIETNAM IT JOB MARKET ANALYSIS - COMPLETE PIPELINE")
    print("="*70)
    
    try:
        # Step 1: Data Processing
        df = run_data_processing()
        
        # Step 2: Salary Analysis
        run_salary_analysis(df)
        
        # Step 3: Skill Analysis
        run_skill_analysis(df)
        
        # Step 4: ML Models
        run_ml_models(df)
        
        print("\n" + "="*70)
        print("✅ ALL ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"\n📂 Results saved to: {OUTPUTS_DIR}")
        print("\n📊 To view interactive dashboard, run:")
        print("   streamlit run src/visualization/dashboard.py")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
