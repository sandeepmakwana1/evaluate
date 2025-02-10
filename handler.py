import json
import os
import google.generativeai as genai

def evaluate(event, context):
    try:
        # Parse request body
        body = json.loads(event['body'])
        
        # Validate input
        if 'questions' not in body or 'solutions' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required fields: questions and solutions'
                })
            }

        questions = body['questions']  # List of dictionaries with 'description' key
        solutions = body['solutions']  # List of lists containing solution strings

        # Configure Google AI
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        
        # Initialize model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        results = []
        for q, s in zip(questions, solutions):
            prompt = f"""
                You are an evaluator tasked with scoring coding solutions for the problem described below. Your primary goal is to evaluate logical correctness without taking care of syntax and the ability of each solution to handle test cases properly.

                    | Problem Description                           | Submitted Solution                          |
                    |-----------------------------------------------|---------------------------------------------|
                    | {q['description']}                            | {s[0]}                                      |

                    ### Evaluation Instructions:

                    1. **Focus solely on logical correctness**
                    - Ignore minor syntax issues unless they impact logic.  
                    - Ignore case sensitivity in variable and method names.  
                    - Ignore import/include-related issues.

                    2. **Identify and penalize solutions that**
                    - Fail to meet the problem's requirements.  
                    - Use incorrect algorithms or miss important steps.  
                    - Provide irrelevant or empty solutions (e.g., a single character like v/V , incomplete code).

                    3. **Score from 1 to 10 based on the following criteria**
                    ------------------------------------------------------------------------------------------------------------------------------------
                    | **Rating** | **Description**                                 | **Details**                                                       |
                    |------------|-------------------------------------------------|-------------------------------------------------------------------|
                    | **10**     | **Perfect Solution**                            | - Completely correct logical implementation                       |
                    |            |                                                 | - Handles ALL possible edge cases (null values, boundary cases)  |
                    |            |                                                 | - Optimal time and space complexity                              |
                    | **8-9**    | **Excellent Solution with Minor Issues**        | - **9**: Correct, optimal but missing one edge case OR slightly suboptimal |
                    |            |                                                 | - **8**: Correct core logic but missing multiple minor edge cases OR suboptimal |
                    |            |                                                 | - Missing one or two edge cases that don’t affect core logic     |
                    |            |                                                 | - Slightly suboptimal time/space complexity                      |
                    | **6-7**    | **Partial Solution with Notable Flaws**         | - **7**: Working solution but missing several edge cases OR suboptimal |
                    |            |                                                 | - **6**: Core logic mostly correct but with significant gaps     |
                    |            |                                                 | - Missing several important edge cases                           |
                    |            |                                                 | - Significantly suboptimal time/space complexity                 |
                    |            |                                                 | - Some logical flaws that don’t completely break the solution    |
                    | **4-5**    | **Partial Solution with Major Issues**          | - **5**: Works for basic cases but fails for many edge cases     |
                    |            |                                                 | - **4**: Significant logical flaws but shows understanding       |
                    |            |                                                 | - Major portions of requirements not addressed                   |
                    |            |                                                 | - Solution works only for specific cases                         |
                    |            |                                                 | - Critical edge cases not handled                                |
                    |            |                                                 | - Major performance issues                                       |
                    | **1-3**    | **Severely Flawed Solution**                    | - **3**: Some correct elements but mostly incorrect              |
                    |            |                                                 | - **2**: Attempt made but fundamental misunderstanding           |
                    |            |                                                 | - **1**: Barely addresses the problem                           |
                    |            |                                                 | - Incorrect algorithmic approach                                 |
                    |            |                                                 | - Fundamental logical errors                                     |
                    |            |                                                 | - Missing critical functionality                                 |
                    |            |                                                 | - Solution doesn't handle basic cases                           |
                    |            |                                                 | - Major syntax or runtime errors                                |
                    |            |                                                 | - Completely inappropriate algorithmic approach                 |
                    |            |                                                 | - containing a single character such as where whole code length is 1 e.g., V/v |
                    --------------------------------------------------------------------------------------------------------------------------------------

                    4. **Output Format**  
                    - always Provide JSON string output with the following structure:  
                        "Score": "<Numeric score from 1-10>",
                        "Explanation": [
                            "<Bullet point explanations of why the solution is incorrect or flawed>"
                        ]

"""
            
            response = model.generate_content(prompt)
            results.append({
                # 'question_description': q['description'],
                # 'submitted_solution': s[0],
                'evaluation': response.text
            })

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': True,
            },
            'body': json.dumps({
                'results': results
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }