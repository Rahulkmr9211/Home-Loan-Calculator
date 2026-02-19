import runpy

sentense = """
Press Respective Number Based on your Requirement:
1. Basis Mode -> Inputs Required:Loan Amount, Interest Rate, Tenure, Loan Start Month -> Press 1
2. Lump Sum Payment Mode -> Press 2
3. Regular Payment Mode -> Press 3

Press Number & Enter your option Here: """
decide = int(input(sentense))
print(decide)
if decide == 1:
    print('Running Vanilla Calculator')
    runpy.run_path("vanilla_calculator.py")
elif decide == 2:
    print('Running Lump Sum Calculator')
    runpy.run_path("lumpSum_calculator.py")
elif decide == 3:
    print('Running Regular Interval Calculator')
    runpy.run_path("regular_interval_calculator.py")
