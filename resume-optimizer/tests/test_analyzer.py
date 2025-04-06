import unittest
from src.analyzer import analyze_resume

class TestAnalyzer(unittest.TestCase):

    def test_analyze_resume_valid(self):
        resume_data = {
            'name': 'John Doe',
            'experience': ['Software Engineer at Company A', 'Intern at Company B'],
            'education': 'Bachelor of Science in Computer Science',
            'skills': ['Python', 'JavaScript', 'Django']
        }
        result = analyze_resume(resume_data)
        self.assertIn('suggestions', result)
        self.assertIsInstance(result['suggestions'], list)

    def test_analyze_resume_empty(self):
        resume_data = {}
        result = analyze_resume(resume_data)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Resume data is empty')

    def test_analyze_resume_invalid_data(self):
        resume_data = 'Invalid data format'
        result = analyze_resume(resume_data)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Invalid resume data format')

if __name__ == '__main__':
    unittest.main()