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
        model = genai.GenerativeModel('gemini-pro')
        
        results = []
        for q, s in zip(questions, solutions):
            prompt = f"""
            You are an evaluator tasked with scoring coding solutions for the problem described below. Your primary goal is to evaluate **logical correctness** and the ability of each solution to handle **edge cases** properly.

            Problem Description:
            {q['description']}

            Submitted Solution:
            {s[0]}

            Please provide a evaluation covering:
            **Evaluation Instructions:**
            1. Focus **only** on the **logical correctness** of the solution. Ignore minor syntax issues unless they **affect the logic**.
            2. Identify and **penalize** solutions that:
                - **Fail to meet the problem's requirements** as described.
                - **Do not handle edge cases** appropriately (e.g., empty input, large input, invalid values).
                - **Use incorrect algorithms** or **miss important steps** in solving the problem.
            3. score 0 to 10
            10 - Perfect Solution

            Completely correct logical implementation
            Handles ALL possible edge cases (empty inputs, null values, boundary conditions)
            Optimal time and space complexity for the given constraints
            Clean, well-structured, and maintainable code
            Includes proper input validation
            Follows best practices and coding standards
            Clear variable/function naming that reflects their purpose
            Includes helpful comments where necessary

            8-9 - Excellent Solution with Minor Issues

            9: Correct implementation with optimal complexity but missing one edge case OR slightly suboptimal but handles all cases
            8: Correct core logic but missing multiple minor edge cases OR using suboptimal approach
            Minor issues might include:

            Missing one or two edge cases that don't affect core functionality
            Slightly suboptimal time/space complexity
            Minor code style issues
            Lacking some input validation
            Some variable names could be more descriptive



            6-7 - Good Solution with Notable Flaws

            7: Working solution but with several edge cases missing OR notably suboptimal approach
            6: Core logic mostly correct but with significant gaps
            Issues at this level:

            Missing several important edge cases
            Significantly suboptimal time/space complexity
            Incomplete error handling
            Code structure needs improvement
            Limited input validation
            Some logical flaws that don't completely break the solution



            4-5 - Partial Solution with Major Issues

            5: Solution works for basic cases but fails for many edge cases
            4: Significant logical flaws but shows understanding of core concept
            Problems include:

            Major portions of requirements not addressed
            Solution works only for specific cases
            Critical edge cases not handled
            Poor code organization
            Incorrect algorithmic approach
            Major performance issues



            1-3 - Severely Flawed Solution

            3: Contains some correct elements but mostly incorrect
            2: Attempts to solve but fundamental misunderstanding
            1: Barely addresses the problem requirements
            Issues include:

            Fundamental logical errors
            Missing critical functionality
            Incorrect understanding of problem requirements
            Solution doesn't handle basic cases
            Major syntax or runtime errors
            Completely inappropriate algorithmic approach



            0 - Invalid Solution

            No working code provided
            Solution completely misses the problem requirements
            Code doesn't compile or run
            Solution solves a different problem
            Purely theoretical answer with no implementation
            Plagiarized or copied solution without understanding

            4. For each solution, provide **scores only**, separated by commas, in the exact order the solutions are provided. Do not include explanations, comments, or additional information.

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