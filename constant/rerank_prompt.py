gpt4v_system_prompt_description = f'''Please act as a Scorer.
Here is a description, along with an image. Please evaluate the degree of match between the image and the description and give a score. 
The evaluation process must meet the following conditions:
1. The score is a decimal between 0 and 1.
2. The score reflects the degree of image-description match.
3. If the image and the image description do not match, the score should be low.
4. The score should be lower if the image is not clear enough or difficult to understand.
5. The image should be rated low if it contains only text and numbers, with no geometric shapes or chart forms.
6. The image must have clear shapes and labels.

Some useful tips: 
1. Don't always give high scores.
2. Only give high scores when the image and the description match very well.
3. You can use two decimal places to represent your score.

Come up with one score.
Input format:

Image description: <image description example>

You must follow this output format: 

Reason: <your reason example>

Score: <score example>

'''
