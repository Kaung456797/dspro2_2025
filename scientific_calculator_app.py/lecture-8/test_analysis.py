from analysis import JobAnalyzer

def test_avg_salary_positive():
    analyzer = JobAnalyzer("東京")
    assert analyzer.avg_salary() is not None

def test_skill_count():
    analyzer = JobAnalyzer("東京")
    assert analyzer.skill_count("Python") >
