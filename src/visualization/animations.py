"""
Animated Dashboard Components
Real-time animations and interactive effects
"""
import streamlit as st
import time


def animated_counter(end_value, label, prefix="", suffix="", duration=1.0):
    """Animated counter effect"""
    placeholder = st.empty()
    
    steps = 30
    increment = end_value / steps
    current = 0
    
    for _ in range(steps):
        current += increment
        placeholder.metric(label, f"{prefix}{int(current):,}{suffix}")
        time.sleep(duration / steps)
    
    placeholder.metric(label, f"{prefix}{end_value:,}{suffix}")


def show_animated_metrics(df):
    """Display animated key metrics"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        animated_counter(len(df), "💼 Tổng việc làm", duration=0.8)
    
    with col2:
        animated_counter(df['company_names'].nunique(), "🏢 Công ty", duration=1.0)
    
    with col3:
        avg_salary = df[df['salary_numeric'].notna()]['salary_numeric'].mean() / 1_000_000
        animated_counter(int(avg_salary), "💰 Lương TB", suffix="M", duration=1.2)
    
    with col4:
        animated_counter(df['city'].nunique(), "📍 Thành phố", duration=0.6)


# JavaScript animations
ANIMATION_CSS = """
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-50px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(50px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.animate-fade-in {
    animation: fadeIn 0.6s ease-out;
}

.animate-slide-left {
    animation: slideInLeft 0.8s ease-out;
}

.animate-slide-right {
    animation: slideInRight 0.8s ease-out;
}

.animate-pulse {
    animation: pulse 2s infinite;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 12px rgba(0,0,0,0.2);
}

.loading-bar {
    width: 100%;
    height: 4px;
    background: #f0f0f0;
    border-radius: 2px;
    overflow: hidden;
    position: relative;
}

.loading-bar::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 30%;
    background: linear-gradient(90deg, #667eea, #764ba2);
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0% { left: -30%; }
    100% { left: 100%; }
}
</style>
"""
